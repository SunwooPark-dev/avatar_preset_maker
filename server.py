# server.py - PersonaFit Studio Backend
import os
import sys
import json
import base64
import subprocess
import threading
import uuid
import time
import re
import shutil
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

PORT = 8080

def find_codex_cli():
    import glob
    base_dir = r"C:\Users\sunwo\AppData\Local\OpenAI\Codex\bin"
    if not os.path.exists(base_dir):
        return "codex"
    exe_files = glob.glob(os.path.join(base_dir, "**", "codex.exe"), recursive=True)
    if exe_files:
        exe_files.sort(key=os.path.getmtime, reverse=True)
        return exe_files[0]
    return "codex"

CODEX_CLI = find_codex_cli()

login_process = None


def get_clean_env() -> dict:
    """Return os.environ copy with BOM stripped from OPENAI_API_KEY.
    
    Root cause: Windows saves env vars with UTF-8 BOM (\\xef\\xbb\\xbf) when set
    via certain tools. Codex CLI reads OPENAI_API_KEY directly from the process
    environment, causing '401 Incorrect API key' due to the BOM prefix in
    the Authorization header. Stripping it here fixes all subprocess calls.
    """
    env = os.environ.copy()
    key = env.get("OPENAI_API_KEY", "")
    if key.startswith("\ufeff"):  # U+FEFF BOM
        env["OPENAI_API_KEY"] = key.lstrip("\ufeff").strip()
    return env


# Pre-compute clean env at startup so it's always ready
_CLEAN_ENV = get_clean_env()

# ── Async job store ──────────────────────────────────────────────────────────
# jobs[job_id] = { "status": "pending"|"done"|"error", "image": "data:...", "error": "..." }
jobs = {}
jobs_lock = threading.Lock()

# ── Preset-specific generation prompts ──────────────────────────────────────
PRESET_PROMPTS = {
    "professional": (
        "Corporate professional headshot. "
        "Clean studio gradient background (light gray or white). "
        "Professional studio soft lighting, Rembrandt lighting setup. "
        "Business attire — suit jacket, button-up shirt. "
        "Sharp focus on face, slight shallow depth of field on shoulders. "
        "Photorealistic 8K portrait, squared centered composition."
    ),
    "travel": (
        "Famous world landmark travel photography background — choose from: "
        "Eiffel Tower Paris, London Tower Bridge, NYC Manhattan skyline, "
        "Santorini Greece white buildings, Tokyo Shibuya crossing, or Colosseum Rome. "
        "Bright natural daylight, golden hour warm tones. "
        "Travel lifestyle portrait, bokeh background, vibrant colors, "
        "wide aperture lens, cinematic color grading."
    ),
    "cinematic": (
        "Epic movie protagonist cinematic portrait. "
        "Dramatic side-rim lighting, moody atmospheric haze. "
        "Hollywood blockbuster poster aesthetic. "
        "Anamorphic lens flare, film grain texture, teal and orange color grade. "
        "Intense focused gaze, heroic posture, dark dramatic background. "
        "large format cinematic quality, 8K ultra detail."
    ),
}


def _run_generation_job(
    job_id: str,
    prompt_str: str,
    gender_str: str,
    work_dir: str,
    style_key: str = "professional",
    closeness: int = 80,
    weight: float = 7.5,
):
    """Background thread: face-preserving generation via Codex exec in work_dir."""
    import shutil

    src_name = f"source_{job_id}.png"
    src_path = os.path.join(work_dir, src_name)
    out_name = f"output_{job_id}.png"
    out_path = os.path.join(work_dir, out_name)

    # Preserve logs
    logs_dir = os.path.join(work_dir, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    log_out = os.path.join(logs_dir, f"gen_{job_id}_out.log")
    log_err = os.path.join(logs_dir, f"gen_{job_id}_err.log")

    # Auto-cleanup source file after 30 minutes (regardless of success/failure)
    def _cleanup_source():
        try:
            if os.path.exists(src_path):
                os.remove(src_path)
        except Exception:
            pass
    cleanup_timer = threading.Timer(1800, _cleanup_source)
    cleanup_timer.daemon = True
    cleanup_timer.start()

    gender_prefix = ""
    if gender_str == "male":
        gender_prefix = "Male "
    elif gender_str == "female":
        gender_prefix = "Female "

    # Build style description: use preset if no custom prompt
    clean_custom = prompt_str.replace("'", "").replace('"', "").strip()
    preset_desc = PRESET_PROMPTS.get(style_key, PRESET_PROMPTS["professional"])
    
    if style_key == "today":
        try:
            style_path = os.path.join(work_dir, "today-style.json")
            if os.path.exists(style_path):
                with open(style_path, "r", encoding="utf-8") as f:
                    today_data = json.load(f)
                    preset_desc = today_data.get("prompt", PRESET_PROMPTS["professional"])
        except Exception:
            pass

    if clean_custom and clean_custom not in ("professional", "travel", "cinematic", "today"):
        # User typed a custom prompt — use it as the style
        style_desc = clean_custom
    else:
        style_desc = preset_desc

    # Closeness → identity preservation strength
    if closeness >= 85:
        identity_strength = (
            "The person's exact identity MUST be strictly preserved: "
            "identical face shape, skin tone, eye color, hair style and color, "
            "glasses/beard/freckles if present, facial proportions, full silhouette. "
            "Zero deviation from the original person's appearance is acceptable."
        )
    elif closeness >= 60:
        identity_strength = (
            "Preserve the person's core identity: same face, same hair, same distinctive features "
            "such as glasses or beard. Overall silhouette and proportions must match closely."
        )
    else:
        identity_strength = (
            "Keep the general resemblance to the original person — same ethnicity, "
            "approximate hair color and length, same gender presentation."
        )

    # Weight → style intensity instruction
    if weight >= 10:
        style_intensity = "Apply a highly dramatic and vivid style transformation."
    elif weight >= 6:
        style_intensity = "Apply a balanced, professional style transformation."
    else:
        style_intensity = "Apply a subtle, understated style enhancement."

    model_instruction = (
        "Model Preference: Generate the image using the ChatGPT Image 2.0 (DALL-E 3) model by default. "
        "If DALL-E 3 is blocked (e.g. by safety/content filters) or fails, "
        "fall back (rollback) to the Google Nano Banana (Gemini Image Generation / Google Image 2.0) model as the sub/secondary option."
    )

    codex_prompt = (
        f"I have attached the source image via -i flag. "
        f"This is a {gender_prefix}portrait photograph. "
        f"{identity_strength} "
        f"Using the attached image as the DIRECT INPUT reference, apply this style: {style_desc}. "
        f"{style_intensity} "
        f"{model_instruction} "
        f"Technical rendering: photorealistic skin textures, depth of field, 8K resolution, "
        f"professional centered square composition, no borders, no text, no watermarks. "
        f"Use your generate_image tool with the attached image as the face reference base. "
        f"Save the output to {out_name} in the current directory."
    )

    # CRITICAL: prompt BEFORE -i flag, run in work_dir (not tmp)
    cmd = [
        CODEX_CLI,
        "exec",
        codex_prompt,
        "-i", src_name,
        "-c", "model_reasoning_effort=low",
        "--dangerously-bypass-approvals-and-sandbox",
    ]

    proc = None
    start_time = time.time()
    success = False
    session_id = None
    session_pattern = re.compile(r"session id:\s*([a-f0-9\-]+)", re.IGNORECASE)
    session_lock = threading.Lock()

    def image_polling_worker(sid):
        nonlocal success
        gen_dir = os.path.join(r"C:\Users\sunwo\.codex\generated_images", sid)
        img_poll_start = time.time()
        while time.time() - img_poll_start < 240:
            # First check if output_job_id.png was copied to work_dir by codex itself
            if os.path.exists(out_path) and os.path.getsize(out_path) > 1024:
                success = True
                if proc and proc.poll() is None:
                    proc.terminate()
                break
            # Also check generated_images dir
            if os.path.isdir(gen_dir):
                png_files = [os.path.join(gen_dir, f) for f in os.listdir(gen_dir) if f.endswith('.png')]
                if png_files:
                    png_files.sort(key=os.path.getmtime, reverse=True)
                    target_img = png_files[0]
                    try:
                        if os.path.getsize(target_img) > 1024:
                            shutil.copy(target_img, out_path)
                            success = True
                            if proc and proc.poll() is None:
                                proc.terminate()
                            break
                    except OSError:
                        pass
            time.sleep(2)

    try:
        with open(log_out, "w", encoding="utf-8") as fout, \
             open(log_err, "w", encoding="utf-8") as ferr:
            proc = subprocess.Popen(
                cmd,
                cwd=work_dir,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                env=_CLEAN_ENV,  # BOM-stripped OPENAI_API_KEY — root fix
            )

        poll_thread = None

        # Reopen log_err in append for line-by-line logging
        with open(log_err, "a", encoding="utf-8") as lf:
            while True:
                line = proc.stdout.readline()
                if not line:
                    if proc.poll() is not None:
                        break
                    time.sleep(0.1)
                    continue

                lf.write(line)
                lf.flush()

                if not session_id:
                    match = session_pattern.search(line)
                    with session_lock:
                        if match and not session_id:
                            session_id = match.group(1)
                            poll_thread = threading.Thread(
                                target=image_polling_worker,
                                args=(session_id,),
                                daemon=True
                            )
                            poll_thread.start()

        if poll_thread:
            poll_thread.join(timeout=240)

        # Final direct check in work_dir
        if not success and os.path.exists(out_path) and os.path.getsize(out_path) > 1024:
            success = True

        if success and os.path.exists(out_path):
            with open(out_path, 'rb') as f:
                encoded = base64.b64encode(f.read()).decode('utf-8')
            with jobs_lock:
                jobs[job_id] = {
                    "status": "done",
                    "image": f"data:image/png;base64,{encoded}"
                }
        else:
            err_text = "Failed to generate image."
            if os.path.exists(log_err):
                try:
                    with open(log_err, 'r', encoding='utf-8', errors='replace') as f:
                        err_text += "\n" + f.read()[-1200:]
                except Exception:
                    pass
            with jobs_lock:
                jobs[job_id] = {
                    "status": "error",
                    "error": f"Image generation failed.\n{err_text}"
                }

    except Exception as e:
        with jobs_lock:
            jobs[job_id] = {"status": "error", "error": f"Exception: {str(e)}"}
    finally:
        if proc and proc.poll() is None:
            try:
                proc.terminate()
                proc.wait(timeout=5)
            except Exception:
                try:
                    proc.kill()
                except Exception:
                    pass

# ─────────────────────────────────────────────────────────────────────────────

class PersonaFitHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def do_GET(self):
        path_only = self.path.split('?')[0]
        if path_only == '/api/status':
            self.handle_status()
        elif path_only == '/api/today-style':
            self.handle_today_style()
        elif path_only.startswith('/api/generate/'):
            job_id = path_only.split('/api/generate/')[-1]
            self.handle_poll(job_id)
        else:
            super().do_GET()

    def do_POST(self):
        path_only = self.path.split('?')[0]
        if path_only == '/api/generate':
            self.handle_generate()
        elif path_only == '/api/analyze-image':
            self.handle_analyze_image()
        elif path_only == '/api/login':
            self.handle_login()
        elif path_only == '/api/login/cancel':
            self.handle_login_cancel()
        else:
            self.send_error(404, "Not Found")

    def handle_status(self):
        try:
            res = subprocess.run(
                [CODEX_CLI, 'login', 'status'],
                capture_output=True,
                text=True,
                timeout=5
            )
            combined_out = res.stdout + res.stderr
            is_connected = res.returncode == 0 and "Logged in" in combined_out
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            response = {
                "status": "connected" if is_connected else "disconnected",
                "details": combined_out.strip()
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))

    def handle_today_style(self):
        try:
            work_dir = os.path.dirname(os.path.abspath(__file__))
            style_path = os.path.join(work_dir, "today-style.json")
            if os.path.exists(style_path):
                with open(style_path, "r", encoding="utf-8") as f:
                    content = f.read()
            else:
                default_style = {
                    "theme": "Y2K Retro Camcorder",
                    "description": "2000년대 Y2K 감성 저화질 디카 플래시 뷰티",
                    "prompt": "Authentic Y2K early 2000s digital camera flash photography style portrait. High-contrast harsh direct flash, slightly soft focus, subtle lens glare, chromatic aberration, minor digital noise. Cool tone-balancing, pale blue and silver color grading. Wearing metallic puffer jacket and oversized futuristic sunglasses. Background: dark neon street alley at night. Expression: confident, playful look. Mood: nostalgic pop culture, Myspace era aesthetic.",
                    "thumbnail": "/assets/today_style_preview.png"
                }
                content = json.dumps(default_style, ensure_ascii=False)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))


    def handle_login(self):
        global login_process
        try:
            if login_process and login_process.poll() is None:
                try:
                    login_process.terminate()
                    login_process.wait(timeout=2)
                except Exception:
                    pass
            
            login_process = subprocess.Popen(
                [CODEX_CLI, 'login'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                env=_CLEAN_ENV,  # BOM-stripped env
            )
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "initiated"}).encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))

    def handle_login_cancel(self):
        global login_process
        try:
            if login_process and login_process.poll() is None:
                try:
                    login_process.terminate()
                    login_process.wait(timeout=2)
                except Exception:
                    pass
                login_process = None
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "cancelled"}).encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))

    def handle_analyze_image(self):
        """POST /api/analyze-image — runs image analysis via Codex, returns JSON analysis results."""
        import tempfile
        tmp_dir = None
        src_path = None
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            params = json.loads(post_data.decode('utf-8'))

            user_img_b64 = params.get('image')
            if not user_img_b64:
                self.send_error(400, "Missing image")
                return

            work_dir = os.path.dirname(os.path.abspath(__file__))
            job_id = uuid.uuid4().hex[:12]
            tmp_dir = os.path.join(work_dir, f"analyze_{job_id}")
            os.makedirs(tmp_dir, exist_ok=True)
            src_path = os.path.join(tmp_dir, "source.png")

            # Decode and save uploaded image
            header, encoded = user_img_b64.split(",", 1) if "," in user_img_b64 else ("", user_img_b64)
            with open(src_path, 'wb') as f:
                f.write(base64.b64decode(encoded))

            cmd = [
                CODEX_CLI,
                "exec",
                "-i", "source.png",
                "-c", "model_reasoning_effort=low",
                "--disable", "hooks",
                "--disable", "plugin_hooks",
                "--disable", "codex_hooks",
                "--ephemeral",
                "--ignore-rules",
                "--skip-git-repo-check",
                "--dangerously-bypass-approvals-and-sandbox",
                "Analyze the uploaded image source.png. Detect the person's face if present. Reply ONLY in raw JSON format with three keys: 'gender' ('male'/'female'/'unknown'), 'type' ('person'/'animal'/'object'), and 'bbox' (an array [ymin, xmin, ymax, xmax] of face bounding box coordinates in percentage 0-100, or null if no face is detected). Do not output markdown code blocks or wrapping text."
            ]

            res = subprocess.run(
                cmd,
                cwd=tmp_dir,
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
                timeout=35,
                env=_CLEAN_ENV,  # BOM-stripped env
            )

            stdout_text = res.stdout.strip()
            # Try to extract JSON from the output (in case there's markdown wrapper code blocks)
            start_idx = stdout_text.find('{')
            end_idx = stdout_text.rfind('}')
            
            result_data = {"gender": "unknown", "type": "person", "bbox": None}
            if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                json_str = stdout_text[start_idx:end_idx+1]
                try:
                    parsed = json.loads(json_str)
                    gender = str(parsed.get("gender", "unknown")).lower()
                    img_type = str(parsed.get("type", "person")).lower()
                    bbox = parsed.get("bbox", None)
                    if gender not in ["male", "female", "unknown"]:
                        gender = "unknown"
                    if img_type not in ["person", "animal", "object"]:
                        img_type = "person"
                    if not isinstance(bbox, list) or len(bbox) != 4:
                        bbox = None
                    result_data = {"gender": gender, "type": img_type, "bbox": bbox}
                except Exception:
                    pass

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result_data).encode('utf-8'))

        except Exception as e:
            self.send_response(200) # Graceful fallback even on server error
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"gender": "unknown", "type": "person", "error": str(e)}).encode('utf-8'))
        finally:
            if tmp_dir and os.path.exists(tmp_dir):
                shutil.rmtree(tmp_dir, ignore_errors=True)

    def handle_generate(self):
        """POST /api/generate — starts async generation, returns {job_id} immediately."""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            params = json.loads(post_data.decode('utf-8'))

            user_img_b64 = params.get('image')
            prompt_str = params.get('prompt', '')
            gender_str = params.get('gender', 'random')
            style_key = params.get('style', 'professional')
            closeness = int(params.get('closeness', 80))
            weight = float(params.get('weight', 7.5))

            if not user_img_b64:
                self.send_error(400, "Missing image")
                return

            # Generate unique job ID
            job_id = uuid.uuid4().hex[:12]
            work_dir = os.path.dirname(os.path.abspath(__file__))
            src = os.path.join(work_dir, f"source_{job_id}.png")

            # Decode and save uploaded image with unique name
            header, encoded = user_img_b64.split(",", 1) if "," in user_img_b64 else ("", user_img_b64)
            with open(src, 'wb') as f:
                f.write(base64.b64decode(encoded))

            # Register job as pending
            with jobs_lock:
                jobs[job_id] = {"status": "pending"}

            # Fire background thread
            t = threading.Thread(
                target=_run_generation_job,
                args=(job_id, prompt_str, gender_str, work_dir),
                kwargs=dict(style_key=style_key, closeness=closeness, weight=weight),
                daemon=True
            )
            t.start()

            self.send_response(202)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "success": True,
                "job_id": job_id,
                "status": "pending"
            }).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "success": False,
                "error": str(e)
            }).encode('utf-8'))

    def handle_poll(self, job_id: str):
        """GET /api/generate/{job_id} — polls job status."""
        with jobs_lock:
            job = jobs.get(job_id)

        if job is None:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "not_found"}).encode('utf-8'))
            return

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        if job["status"] == "done":
            resp = {
                "success": True,
                "status": "done",
                "image": job["image"]
            }
            # Remove from store after delivery
            with jobs_lock:
                jobs.pop(job_id, None)
        elif job["status"] == "error":
            resp = {
                "success": False,
                "status": "error",
                "error": job.get("error", "Unknown error")
            }
            with jobs_lock:
                jobs.pop(job_id, None)
        else:
            resp = {"success": True, "status": "pending"}

        self.wfile.write(json.dumps(resp).encode('utf-8'))



if __name__ == '__main__':
    # Ensure serving from the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    server = ThreadingHTTPServer(('0.0.0.0', PORT), PersonaFitHandler)
    print(f"Starting server on port {PORT} at {script_dir}...")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
