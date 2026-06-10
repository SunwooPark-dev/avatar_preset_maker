// app.js - PersonaFit Studio

document.addEventListener('DOMContentLoaded', () => {
  // Global Translation Dictionary
  const I18N = {
    ko: {
      app_title: "PersonaFit Studio",
      app_subtitle: "아티스틱 프로필 에디터. 파라미터를 조절하여 나만의 비주얼 아이덴티티를 설정하세요.",
      check_connection: "Codex 연결 상태 확인",
      codex_offline: "Codex 연동 오프라인",
      codex_connected: "Codex 연결됨",
      codex_checking: "연결 확인 중...",
      codex_error: "연결 오류",
      login: "로그인",
      reconnect: "재연결",
      source_photo_title: "원본 사진",
      upload_text: "스타일 변환할 사진 업로드",
      upload_info: "여기에 파일을 끌어다 놓으세요",
      remove_image: "사진 제거",
      privacy_shield_text: "원본 사진은 스타일 변환 분석 완료 즉시 완전히 파기되며 서버에 저장되지 않습니다. 안심하고 사용하세요.",
      style_presets_title: "스타일 프리셋",
      shuffle_btn_title: "1,800개 중 무작위 스타일 적용",
      shuffle_btn_text: "셔플",
      library_btn_text: "스타일 라이브러리",
      preset_corporate_name: "증명사진",
      preset_corporate_desc: "스튜디오 증명사진 테마",
      preset_travel_name: "여행 테마",
      preset_travel_desc: "유명 관광지 배경 테마",
      preset_cinematic_name: "시네마틱",
      preset_cinematic_desc: "영화 속 주인공 테마",
      preset_today_name: "오늘의 밈",
      preset_today_desc: "로딩 중...",
      custom_prompt_title: "커스텀 프롬프트",
      gender_label: "성별 필터",
      gender_random: "임의",
      gender_male: "남성",
      gender_female: "여성",
      custom_prompt_placeholder: "적용하고 싶은 커스텀 스타일이나 배경 변수를 입력하세요 (예: 흑백 필름 필터, 유화, 네온 조명)...",
      detail_tuning_title: "세부 매개변수 튜닝",
      slider_weight_title: "프롬프트 반영 강도",
      slider_weight_tip: "지시사항 프롬프트를 이미지에 얼마나 강하게 반영할지 결정하는 세기입니다.",
      slider_closeness_title: "얼굴 보존율",
      slider_closeness_tip: "수치가 높을수록 본래 얼굴의 특징과 이목구비를 더 가깝게 유지합니다.",
      slider_detail_title: "세부 표현 선명도",
      slider_detail_tip: "피부 질감 표현과 얼굴 외곽선의 선명도 및 디테일 레벨을 결정합니다.",
      render_btn_text: "스타일 렌더링 시작",
      render_btn_mock: "스타일 렌더링 (시뮬레이션)",
      render_btn_codex: "스타일 렌더링 (이미지 2.0)",
      output_canvas_title: "출력 캔버스",
      empty_workspace_title: "빈 작업 영역",
      empty_workspace_desc: "왼쪽에서 원본 사진을 업로드하고 설정을 진행해 주세요.",
      empty_workspace_ready: "렌더링 준비 완료",
      empty_workspace_ready_desc: "스타일을 고르고 아래의 생성하기 버튼을 누르세요.",
      rendering_title: "AI 아트 렌더링 중 (약 1분 소요)...",
      rendering_status: "색상 채널 분석 중...",
      tab_memory: "카드 뒤집기",
      tab_tictactoe: "틱택토",
      game_memory_title: "🎮 카드 매치 게임",
      game_restart: "🔄 다시 시작",
      game_ttt_title: "❌ 틱택토 게임 ⭕",
      game_ttt_status_your: "회원님 차례 (X)",
      game_ttt_status_ai: "AI 생각 중 (O)...",
      game_ttt_status_win: "회원님 승리! 🎉",
      game_ttt_status_lose: "AI 승리! 🤖",
      game_ttt_status_draw: "무승부! 🤝",
      label_source: "원본 이미지",
      label_styled_output: "스타일 변환 결과",
      control_contrast: "대비",
      control_brightness: "밝기",
      control_saturation: "채도",
      sns_export_title: "SNS 내보내기 설정",
      sns_format_label: "SNS 규격 비율",
      sns_opt_original: "원본 비율 (1:1 정사각형)",
      sns_opt_x_profile: "X 프로필 (400x400)",
      sns_opt_x_post: "X 포스트 (1200x675, 16:9)",
      sns_opt_linkedin_profile: "링크드인 프로필 (400x400)",
      sns_opt_linkedin_post: "링크드인 포스트 (1200x627, 1.91:1)",
      sns_opt_threads_profile: "스레드 프로필 (320x320)",
      sns_opt_threads_post: "스레드 포스트 (1080x1350, 4:5)",
      sns_opt_facebook_profile: "페이스북 프로필 (170x170)",
      sns_opt_facebook_post: "페이스북 포스트 (1200x630, 1.91:1)",
      sns_opt_instagram_story: "인스타그램 스토리 (1080x1920, 9:16)",
      sns_crop_info_template: "<strong>{name}</strong> 비율로 크롭 편집하여 저장합니다.",
      sns_crop_info_pad: "블러 배경 패딩을 추가하여 <strong>{name}</strong> ({w}x{h}, 비율 {aspect}) 규격으로 저장합니다.",
      btn_add_collection: "컬렉션에 보관",
      btn_add_collection_done: "보관 완료!",
      btn_share_card: "공유 카드 생성",
      btn_download_image: "다운로드",
      history_collection_title: "컬렉션 히스토리",
      history_collection_empty: "저장된 히스토리가 없습니다. 스타일 변환 후 보관해 보세요.",
      login_modal_title: "Codex CLI 로그인 인증",
      login_modal_desc: "새 브라우저 탭에서 ChatGPT OAuth 로그인을 진행해 주세요.",
      login_modal_hint: "로그인이 확인되면 이 화면이 자동으로 닫힙니다.",
      btn_cancel: "취소",
      library_modal_title: "스타일 템플릿 라이브러리",
      library_loading: "로딩 중...",
      library_search_placeholder: "스타일 명칭 검색...",
      category_all: "전체",
      category_today: "오늘의 밈 🔥",
      category_portrait: "인물/화보",
      category_illustration: "일러스트",
      category_cosplay: "코스프레",
      category_photo: "감성사진",
      category_food: "음식/카페",
      category_product: "제품/광고",
      category_character: "캐릭터",
      category_sticker: "스티커",
      category_poster: "포스터",
      category_other: "기타",
      btn_close: "닫기",
      
      toast_connected: "Codex 연동이 완료되었습니다!",
      toast_gender_auto: "프롬프트 성별 표현이 [{gender}]형으로 자동 조정되었습니다.",
      toast_gender_detect: "💡 사진 인식 결과: [{gender}] 프로필로 자동 설정되었습니다.",
      toast_crop_complete: "📸 최적의 이미지 구도 조정을 위해 얼굴 중심 줌-크롭을 완료했습니다.",
      toast_animal_detect: "🐾 인식 결과: 반려동물/동물 프로필로 감지되었습니다. 셔플 시 관련 일러스트 스타일이 우선 적용됩니다.",
      toast_upload_error: "이미지 파일만 업로드할 수 있습니다.",
      toast_timeout: "⚠️ 생성 시간 초과 (5분). 다시 시도해 주세요.",
      toast_gen_error: "⚠️ 이미지 생성 실패. 다시 시도해 주세요.",
      toast_network_error: "⚠️ 네트워크 오류: {msg}",
      toast_img_load_error: "이미지 로딩 실패",
      toast_library_applied: "스타일 프롬프트가 적용되었습니다. 매개변수도 자동 튜닝 완료!",
      toast_library_loading: "프롬프트 DB 로딩 중입니다. 잠시 후 다시 시도해 주세요.",
      toast_unsupported_crop: "크롭 기능을 지원하지 않는 이미지 파일입니다.",
      
      gender_name_male: "남성",
      gender_name_female: "여성",
      gender_adj_male: "남성형",
      gender_adj_female: "여성형",
      
      rolling_status_0: "얼굴 윤곽 및 이목구비 랜드마크 분석 중...",
      rolling_status_1: "선택하신 스타일 프리셋 붓터치 맵핑 중...",
      rolling_status_2: "색조 매트릭스 보정 및 입체적 쉐이딩 적용 중...",
      rolling_status_3: "얼굴 피부 결 보존 및 미세 텍스처 업스케일링 중...",
      rolling_status_4: "최종 아티스틱 합성 및 SNS 내보내기 셋팅 준비 중...",
      
      moves_count: "{moves}회 이동",
      no_search_results: "검색 결과가 없습니다.",
      no_title: "(제목 없음)",
      custom_style: "커스텀 스타일",
      delete_avatar: "아바타 삭제",
      unknown_error: "알 수 없는 오류",
      alert_login_init_failed: "로그인 초기화 실패: ",
      alert_login_error: "로그인 요청 중 오류 발생: ",
      start_job_failed: "작업 시작 실패",
      library_badge_text: "{count}개 프롬프트",
      toast_shuffle_applied: "🎲 랜덤 스타일 적용: 태그 [{tags}]"
    },
    en: {
      app_title: "PersonaFit Studio",
      app_subtitle: "Art-directed profile editor. Adjust parameters to configure your visual identity.",
      check_connection: "Check Codex Link Status",
      codex_offline: "Codex Link Offline",
      codex_connected: "Codex Connected",
      codex_checking: "Checking Link...",
      codex_error: "Connection Error",
      login: "Login",
      reconnect: "Reconnect",
      source_photo_title: "Source Photo",
      upload_text: "Upload photo to style",
      upload_info: "Drag and drop files here",
      remove_image: "Remove photo",
      privacy_shield_text: "Your source photo is destroyed immediately after style analysis and is never stored on the server.",
      style_presets_title: "Style Presets",
      shuffle_btn_title: "Apply a random style from 1,800 presets",
      shuffle_btn_text: "Shuffle",
      library_btn_text: "Style Library",
      preset_corporate_name: "Corporate",
      preset_corporate_desc: "Studio ID Portrait",
      preset_travel_name: "Travel",
      preset_travel_desc: "Famous Landmarks",
      preset_cinematic_name: "Cinematic",
      preset_cinematic_desc: "Movie Main Character",
      preset_today_name: "Today's Style",
      preset_today_desc: "Loading...",
      custom_prompt_title: "Custom Prompt",
      gender_label: "Gender Filter",
      gender_random: "Random",
      gender_male: "Male",
      gender_female: "Female",
      custom_prompt_placeholder: "Enter custom style instructions or background details (e.g., retro black and white, oil painting, neon lights)...",
      detail_tuning_title: "Detail Tuning",
      slider_weight_title: "Prompt Weight",
      slider_weight_tip: "Determines how strongly the text prompt influences the transformed image.",
      slider_closeness_title: "Closeness to original",
      slider_closeness_tip: "Higher values retain more of your original facial structure and features.",
      slider_detail_title: "Detailing strength",
      slider_detail_tip: "Controls skin texture detail and edge sharpness in the generated portrait.",
      render_btn_text: "Render Style",
      render_btn_mock: "Render Style (Mock)",
      render_btn_codex: "Render Image (Image 2.0)",
      output_canvas_title: "Output Canvas",
      empty_workspace_title: "Empty Workspace",
      empty_workspace_desc: "Upload a source photo to begin style configuration.",
      empty_workspace_ready: "Ready to Render",
      empty_workspace_ready_desc: "Select a style preset or write a custom prompt, then click Render Style below.",
      rendering_title: "AI Art Rendering (approx. 1 min)...",
      rendering_status: "Analyzing color channels...",
      tab_memory: "Memory Match",
      tab_tictactoe: "Tic-Tac-Toe",
      game_memory_title: "🎮 Memory Match Game",
      game_restart: "🔄 Restart",
      game_ttt_title: "❌ Tic-Tac-Toe ⭕",
      game_ttt_status_your: "Your turn (X)",
      game_ttt_status_ai: "AI thinking (O)...",
      game_ttt_status_win: "You win! 🎉",
      game_ttt_status_lose: "AI wins! 🤖",
      game_ttt_status_draw: "It's a draw! 🤝",
      label_source: "Source Image",
      label_styled_output: "Styled Output",
      control_contrast: "Contrast",
      control_brightness: "Brightness",
      control_saturation: "Saturation",
      sns_export_title: "SNS Export Settings",
      sns_format_label: "SNS Ratio",
      sns_opt_original: "Original (1:1 Square)",
      sns_opt_x_profile: "X Profile (400x400)",
      sns_opt_x_post: "X Post (1200x675, 16:9)",
      sns_opt_linkedin_profile: "LinkedIn Profile (400x400)",
      sns_opt_linkedin_post: "LinkedIn Post (1200x627, 1.91:1)",
      sns_opt_threads_profile: "Threads Profile (320x320)",
      sns_opt_threads_post: "Threads Post (1080x1350, 4:5)",
      sns_opt_facebook_profile: "Facebook Profile (170x170)",
      sns_opt_facebook_post: "Facebook Post (1200x630, 1.91:1)",
      sns_opt_instagram_story: "Instagram Story (1080x1920, 9:16)",
      sns_crop_info_template: "Will export cropped as <strong>{name}</strong>.",
      sns_crop_info_pad: "Will export as <strong>{name}</strong> ({w}x{h}, Aspect {aspect}) with blurred background padding.",
      btn_add_collection: "Add to Collection",
      btn_add_collection_done: "Saved!",
      btn_share_card: "Share Card",
      btn_download_image: "Download",
      history_collection_title: "Collection History",
      history_collection_empty: "Collection empty. Save your transformed profiles here.",
      login_modal_title: "Codex CLI Authentication",
      login_modal_desc: "Please proceed with ChatGPT OAuth login in the new browser tab.",
      login_modal_hint: "This screen will automatically close once authenticated.",
      btn_cancel: "Cancel",
      library_modal_title: "Style Template Library",
      library_loading: "Loading...",
      library_search_placeholder: "Search style templates...",
      category_all: "All",
      category_today: "Today's Trend 🔥",
      category_portrait: "Portrait",
      category_illustration: "Illustration",
      category_cosplay: "Cosplay",
      category_photo: "Photo",
      category_food: "Food & Cafe",
      category_product: "Product Ad",
      category_character: "Character",
      category_sticker: "Sticker",
      category_poster: "Poster",
      category_other: "Other",
      btn_close: "Close",
      
      toast_connected: "Codex integration successful!",
      toast_gender_auto: "Prompt gender phrasing auto-adjusted to [{gender}].",
      toast_gender_detect: "💡 Photo Analysis: Automatically set to [{gender}] profile.",
      toast_crop_complete: "📸 Auto-zoomed and centered on face for optimal composition.",
      toast_animal_detect: "🐾 Pet detected: Shuffle will prioritize animal illustration styles.",
      toast_upload_error: "Only image files can be uploaded.",
      toast_timeout: "⚠️ Rendering timed out (5 mins). Please try again.",
      toast_gen_error: "⚠️ Image generation failed. Please try again.",
      toast_network_error: "⚠️ Network error: {msg}",
      toast_img_load_error: "Failed to load image",
      toast_library_applied: "Style preset applied. Parameters auto-tuned!",
      toast_library_loading: "Prompt database is loading. Please try again in a moment.",
      toast_unsupported_crop: "Image format does not support cropping.",
      
      gender_name_male: "male",
      gender_name_female: "female",
      gender_adj_male: "masculine",
      gender_adj_female: "feminine",
      
      rolling_status_0: "Analyzing face landmarks and contours...",
      rolling_status_1: "Mapping brushstrokes for the selected style...",
      rolling_status_2: "Correcting color matrices and applying shading...",
      rolling_status_3: "Preserving facial details and upscaling textures...",
      rolling_status_4: "Finalizing artistic render and preparing export...",
      
      moves_count: "{moves} moves",
      no_search_results: "No search results found.",
      no_title: "(No Title)",
      custom_style: "Custom Style",
      delete_avatar: "Delete Avatar",
      unknown_error: "Unknown error",
      alert_login_init_failed: "Login initialization failed: ",
      alert_login_error: "Error during login request: ",
      start_job_failed: "Failed to start job",
      library_badge_text: "{count} prompts",
      toast_shuffle_applied: "🎲 Applied random style: Tags [{tags}]"
    },
    es: {
      app_title: "PersonaFit Studio",
      app_subtitle: "Editor de perfiles artísticos. Ajuste los parámetros para configurar su identidad visual.",
      check_connection: "Comprobar estado del enlace Codex",
      codex_offline: "Enlace Codex Desconectado",
      codex_connected: "Codex Conectado",
      codex_checking: "Comprobando enlace...",
      codex_error: "Error de conexión",
      login: "Iniciar sesión",
      reconnect: "Reconectar",
      source_photo_title: "Foto de Origen",
      upload_text: "Subir foto para aplicar estilo",
      upload_info: "Arrastre y suelte archivos aquí",
      remove_image: "Eliminar foto",
      privacy_shield_text: "Su foto de origen se destruye inmediatamente tras el análisis de estilo y nunca se almacena en el servidor.",
      style_presets_title: "Ajustes de Estilo",
      shuffle_btn_title: "Aplicar un estilo aleatorio de 1.800 preajustes",
      shuffle_btn_text: "Aleatorio",
      library_btn_text: "Biblioteca de Estilos",
      preset_corporate_name: "Corporativo",
      preset_corporate_desc: "Retrato para Identificación",
      preset_travel_name: "Viaje",
      preset_travel_desc: "Lugares Famosos",
      preset_cinematic_name: "Cinemático",
      preset_cinematic_desc: "Héroe de Película",
      preset_today_name: "Estilo del Día",
      preset_today_desc: "Cargando...",
      custom_prompt_title: "Indicación Personalizada",
      gender_label: "Filtro de Género",
      gender_random: "Aleatorio",
      gender_male: "Masculino",
      gender_female: "Femenino",
      custom_prompt_placeholder: "Escriba directrices de estilo o fondo (ej. blanco y negro retro, pintura al óleo, luces de neón)...",
      detail_tuning_title: "Ajuste de Detalles",
      slider_weight_title: "Fuerza de Indicación",
      slider_weight_tip: "Determina qué tan fuerte influye el texto de indicación en la imagen resultante.",
      slider_closeness_title: "Fidelidad al original",
      slider_closeness_tip: "Los valores más altos retienen más rasgos e hidratación de su cara original.",
      slider_detail_title: "Intensidad de detalle",
      slider_detail_tip: "Controla el realismo de la piel y la nitidez de los bordes del retrato.",
      render_btn_text: "Renderizar Estilo",
      render_btn_mock: "Renderizar Estilo (Mock)",
      render_btn_codex: "Renderizar Imagen (Imagen 2.0)",
      output_canvas_title: "Lienzo de Salida",
      empty_workspace_title: "Lienzo Vacío",
      empty_workspace_desc: "Suba una foto de origen para comenzar la configuración de estilo.",
      empty_workspace_ready: "Listo para Renderizar",
      empty_workspace_ready_desc: "Elija un ajuste de estilo o escriba una indicación, luego haga clic en Renderizar abajo.",
      rendering_title: "Renderizando Arte IA (aprox. 1 min)...",
      rendering_status: "Analizando canales de color...",
      tab_memory: "Emparejar Tarjetas",
      tab_tictactoe: "Tres en Raya",
      game_memory_title: "🎮 Juego de Emparejar Tarjetas",
      game_restart: "🔄 Reiniciar",
      game_ttt_title: "❌ Tres en Raya ⭕",
      game_ttt_status_your: "Tu turno (X)",
      game_ttt_status_ai: "AI pensando (O)...",
      game_ttt_status_win: "¡Ganaste! 🎉",
      game_ttt_status_lose: "¡Ganó la IA! 🤖",
      game_ttt_status_draw: "¡Empate! 🤝",
      label_source: "Imagen de Origen",
      label_styled_output: "Resultado Estilizado",
      control_contrast: "Contraste",
      control_brightness: "Brillo",
      control_saturation: "Saturación",
      sns_export_title: "Ajustes de Exportación SNS",
      sns_format_label: "Formato SNS",
      sns_opt_original: "Tamaño Original (1:1 Cuadrado)",
      sns_opt_x_profile: "Perfil de X (400x400)",
      sns_opt_x_post: "Publicación de X (1200x675, 16:9)",
      sns_opt_linkedin_profile: "Perfil de LinkedIn (400x400)",
      sns_opt_linkedin_post: "Publicación de LinkedIn (1200x627, 1.91:1)",
      sns_opt_threads_profile: "Perfil de Threads (320x320)",
      sns_opt_threads_post: "Publicación de Threads (1080x1350, 4:5)",
      sns_opt_facebook_profile: "Perfil de Facebook (170x170)",
      sns_opt_facebook_post: "Publicación de Facebook (1200x630, 1.91:1)",
      sns_opt_instagram_story: "Historia de Instagram (1080x1920, 9:16)",
      sns_crop_info_template: "Se exportará recortado como <strong>{name}</strong>.",
      sns_crop_info_pad: "Se exportará como <strong>{name}</strong> ({w}x{h}, Proporción {aspect}) con relleno de fondo desenfocado.",
      btn_add_collection: "Guardar en Colección",
      btn_add_collection_done: "¡Guardado!",
      btn_share_card: "Tarjeta de Compartir",
      btn_download_image: "Descargar",
      history_collection_title: "Historial de Colección",
      history_collection_empty: "Colección vacía. Guarde sus perfiles estilizados aquí.",
      login_modal_title: "Autenticación Codex CLI",
      login_modal_desc: "Complete el inicio de sesión OAuth de ChatGPT en la nueva pestaña.",
      login_modal_hint: "Esta pantalla se cerrará automáticamente al autenticarse.",
      btn_cancel: "Cancelar",
      library_modal_title: "Biblioteca de Plantillas de Estilo",
      library_loading: "Cargando...",
      library_search_placeholder: "Buscar plantillas de estilo...",
      category_all: "Todos",
      category_today: "Tendencia del Día 🔥",
      category_portrait: "Retrato",
      category_illustration: "Ilustración",
      category_cosplay: "Cosplay",
      category_photo: "Fotografía",
      category_food: "Comida y Café",
      category_product: "Anuncio de Producto",
      category_character: "Personaje",
      category_sticker: "Sticker",
      category_poster: "Póster",
      category_other: "Otro",
      btn_close: "Cerrar",
      
      toast_connected: "¡Integración con Codex exitosa!",
      toast_gender_auto: "Frase de género ajustada automáticamente a [{gender}].",
      toast_gender_detect: "💡 Análisis de foto: Ajustado automáticamente a perfil [{gender}].",
      toast_crop_complete: "📸 Recortado y centrado en la cara para una composición óptima.",
      toast_animal_detect: "🐾 Mascota detectada: Se priorizarán estilos de ilustración de animales.",
      toast_upload_error: "Solo se pueden subir archivos de imagen.",
      toast_timeout: "⚠️ Tiempo de renderizado agotado (5 min). Inténtelo de nuevo.",
      toast_gen_error: "⚠️ Error al generar imagen. Inténtelo de nuevo.",
      toast_network_error: "⚠️ Error de red: {msg}",
      toast_img_load_error: "Error al cargar la imagen",
      toast_library_applied: "¡Ajuste de estilo aplicado y parámetros optimizados!",
      toast_library_loading: "La base de datos se está cargando. Intente de nuevo en un momento.",
      toast_unsupported_crop: "El formato de imagen no admite recorte.",
      
      gender_name_male: "masculino",
      gender_name_female: "femenino",
      gender_adj_male: "masculino",
      gender_adj_female: "femenino",
      
      rolling_status_0: "Analizando contornos y rasgos faciales...",
      rolling_status_1: "Mapeando pinceladas para el estilo seleccionado...",
      rolling_status_2: "Corrigiendo matrices de color y sombreado...",
      rolling_status_3: "Preservando detalles de piel y escalando texturas...",
      rolling_status_4: "Finalizando el render artístico y preparando exportación...",
      
      moves_count: "{moves} movimientos",
      no_search_results: "No se encontraron resultados de búsqueda.",
      no_title: "(Sin Título)",
      custom_style: "Estilo Personalizado",
      delete_avatar: "Eliminar Avatar",
      unknown_error: "Error desconocido",
      alert_login_init_failed: "Error al iniciar sesión: ",
      alert_login_error: "Error durante la solicitud de inicio de sesión: ",
      start_job_failed: "Error al iniciar la tarea de renderizado",
      library_badge_text: "{count} estilos",
      toast_shuffle_applied: "🎲 Estilo aleatorio aplicado: Etiquetas [{tags}]"
    },
    zh: {
      app_title: "PersonaFit Studio",
      app_subtitle: "艺术轮廓编辑器。调整参数以配置您的视觉身份。",
      check_connection: "检查 Codex 连接状态",
      codex_offline: "Codex 未连接",
      codex_connected: "Codex 已连接",
      codex_checking: "正在检查连接...",
      codex_error: "连接错误",
      login: "登录",
      reconnect: "重新连接",
      source_photo_title: "源照片",
      upload_text: "上传需要转换风格的照片",
      upload_info: "将文件拖放到此处",
      remove_image: "删除照片",
      privacy_shield_text: "风格分析完成后，源照片将立即被完全销毁，绝不存储在服务器上。",
      style_presets_title: "风格预设",
      shuffle_btn_title: "从 1800 个风格中随机应用",
      shuffle_btn_text: "随机",
      library_btn_text: "风格库",
      preset_corporate_name: "证件照",
      preset_corporate_desc: "精致工作证件照风格",
      preset_travel_name: "旅行足迹",
      preset_travel_desc: "著名景点背景风格",
      preset_cinematic_name: "电影风情",
      preset_cinematic_desc: "电影女主角/男主角风格",
      preset_today_name: "今日风潮",
      preset_today_desc: "载入中...",
      custom_prompt_title: "自定义提示词",
      gender_label: "性别筛选",
      gender_random: "随机",
      gender_male: "男性",
      gender_female: "女性",
      custom_prompt_placeholder: "输入自定义风格指令或背景元素（例如：复古黑白、油画、霓虹灯光）...",
      detail_tuning_title: "细节参数调整",
      slider_weight_title: "提示词权重",
      slider_weight_tip: "决定提示词文本对最终生成图像的影响强度。",
      slider_closeness_title: "面部保真度",
      slider_closeness_tip: "数值越高，越能保留您原本的面部结构和五官特征。",
      slider_detail_title: "细节清晰度",
      slider_detail_tip: "控制皮肤质感的精细度和肖像边缘的清晰度。",
      render_btn_text: "生成风格",
      render_btn_mock: "生成风格 (Mock)",
      render_btn_codex: "生成图像 (图像 2.0)",
      output_canvas_title: "输出画布",
      empty_workspace_title: "空白工作区",
      empty_workspace_desc: "请先上传一张源照片以开始风格配置。",
      empty_workspace_ready: "准备生成",
      empty_workspace_ready_desc: "选择风格预设或输入自定义提示词，然后点击下方生成按钮。",
      rendering_title: "AI 艺术渲染中 (约需 1 分钟)...",
      rendering_status: "分析颜色通道中...",
      tab_memory: "卡片匹配",
      tab_tictactoe: "井字棋",
      game_memory_title: "🎮 记忆卡片匹配",
      game_restart: "🔄 重新开始",
      game_ttt_title: "❌ 井字棋游戏 ⭕",
      game_ttt_status_your: "您的回合 (X)",
      game_ttt_status_ai: "AI 思考中 (O)...",
      game_ttt_status_win: "您赢了! 🎉",
      game_ttt_status_lose: "AI 赢了! 🤖",
      game_ttt_status_draw: "平局! 🤝",
      label_source: "原始照片",
      label_styled_output: "风格效果图",
      control_contrast: "对比度",
      control_brightness: "亮度",
      control_saturation: "饱和度",
      sns_export_title: "SNS 导出规格设置",
      sns_format_label: "SNS 规格比例",
      sns_opt_original: "原始尺寸 (1:1 正方形)",
      sns_opt_x_profile: "X 头像 (400x400)",
      sns_opt_x_post: "X 配图 (1200x675, 16:9)",
      sns_opt_linkedin_profile: "LinkedIn 头像 (400x400)",
      sns_opt_linkedin_post: "LinkedIn 配图 (1200x627, 1.91:1)",
      sns_opt_threads_profile: "Threads 头像 (320x320)",
      sns_opt_threads_post: "Threads 配图 (1080x1350, 4:5)",
      sns_opt_facebook_profile: "Facebook 头像 (170x170)",
      sns_opt_facebook_post: "Facebook 配图 (1200x630, 1.91:1)",
      sns_opt_instagram_story: "Instagram 故事 (1080x1920, 9:16)",
      sns_crop_info_template: "将裁剪为 <strong>{name}</strong> 尺寸并导出。",
      sns_crop_info_pad: "将添加模糊背景边距并按 <strong>{name}</strong> ({w}x{h}, 比例 {aspect}) 规格导出。",
      btn_add_collection: "保存到收藏夹",
      btn_add_collection_done: "保存成功!",
      btn_share_card: "生成分享卡",
      btn_download_image: "下载照片",
      history_collection_title: "收藏历史",
      history_collection_empty: "暂无收藏。请在此处保存您转换后的精美头像。",
      login_modal_title: "Codex CLI 登录认证",
      login_modal_desc: "请在新开启的浏览器标签页中完成 ChatGPT OAuth 登录。",
      login_modal_hint: "登录成功后此窗口将自动关闭。",
      btn_cancel: "取消",
      library_modal_title: "风格模板库",
      library_loading: "载入中...",
      library_search_placeholder: "搜索风格模板...",
      category_all: "全部",
      category_today: "今日风潮 🔥",
      category_portrait: "人像",
      category_illustration: "插画",
      category_cosplay: "角色扮演",
      category_photo: "感性写真",
      category_food: "美食/咖啡",
      category_product: "产品广告",
      category_character: "角色设计",
      category_sticker: "贴纸",
      category_poster: "海报",
      category_other: "其他",
      btn_close: "关闭",
      
      toast_connected: "Codex 连接成功！",
      toast_gender_auto: "提示词性别词汇已自动调整为 [{gender}] 型。",
      toast_gender_detect: "💡 照片分析：自动设定为 [{gender}] 型个人资料。",
      toast_crop_complete: "📸 已自动将面部居中并裁剪，以获得最佳构图。",
      toast_animal_detect: "🐾 检测到宠物：随机选择时将优先适用动物插画风格。",
      toast_upload_error: "只能上传图像文件。",
      toast_timeout: "⚠️ 渲染超时 (5分钟)。请重试。",
      toast_gen_error: "⚠️ 图像生成失败。请重试。",
      toast_network_error: "⚠️ 网络错误: {msg}",
      toast_img_load_error: "照片加载失败",
      toast_library_applied: "风格模板已应用，参数亦已自动优化！",
      toast_library_loading: "提示词数据库正在载入中，请稍后再试。",
      toast_unsupported_crop: "该图片格式不支持自动裁剪。",
      
      gender_name_male: "男性",
      gender_name_female: "女性",
      gender_adj_male: "男性化",
      gender_adj_female: "女性化",
      
      rolling_status_0: "分析面部轮廓及五官特征点中...",
      rolling_status_1: "为所选风格映射笔触线条中...",
      rolling_status_2: "校正色彩矩阵并应用立体阴影效果中...",
      rolling_status_3: "保留面部皮肤细节并进行超分辨率处理中...",
      rolling_status_4: "正在进行最终艺术合成并准备 SNS 导出...",
      
      moves_count: "{moves} 步",
      no_search_results: "没有找到相关搜索结果。",
      no_title: "(无标题)",
      custom_style: "自定义风格",
      delete_avatar: "删除头像",
      unknown_error: "未知错误",
      alert_login_init_failed: "登录初始化失败: ",
      alert_login_error: "登录请求中出错: ",
      start_job_failed: "启动渲染任务失败",
      library_badge_text: "{count} 个预设",
      toast_shuffle_applied: "🎲 已应用随机风格：标签 [{tags}]"
    },
    ja: {
      app_title: "PersonaFit Studio",
      app_subtitle: "アートディレクションされたプロフィールエディタ。パラメータを調整してビジュアルアイデンティティを構成します。",
      check_connection: "Codexの接続状態を確認",
      codex_offline: "Codex リンク オフライン",
      codex_connected: "Codex 接続済み",
      codex_checking: "接続を確認中...",
      codex_error: "接続エラー",
      login: "ログイン",
      reconnect: "再接続",
      source_photo_title: "元の写真",
      upload_text: "スタイル変換する写真をアップロード",
      upload_info: "ここにファイルをドラッグ＆ドロップ",
      remove_image: "写真を削除",
      privacy_shield_text: "元の写真はスタイル分析が完了次第ただちに完全に破棄され、サーバーに保存されません。安心してお使いください。",
      style_presets_title: "スタイルプリセット",
      shuffle_btn_title: "1,800種類のスタイルからランダム適用",
      shuffle_btn_text: "シャッフル",
      library_btn_text: "スタイルライブラリ",
      preset_corporate_name: "証明写真",
      preset_corporate_desc: "スタジオ証明写真テーマ",
      preset_travel_name: "旅行テーマ",
      preset_travel_desc: "有名観光地背景テーマ",
      preset_cinematic_name: "シ네마틱",
      preset_cinematic_desc: "映画の主人公テーマ",
      preset_today_name: "本日のトレンド",
      preset_today_desc: "読み込み中...",
      custom_prompt_title: "カスタムプロンプト",
      gender_label: "性別フィルター",
      gender_random: "ランダム",
      gender_male: "男性",
      gender_female: "女性",
      custom_prompt_placeholder: "適用したいカスタムスタイルや背景の指示を入力してください (例: レトロ白黒フィルム、油絵、ネオン照明)...",
      detail_tuning_title: "パラメータ詳細チューニング",
      slider_weight_title: "プロンプト反映度",
      slider_weight_tip: "指示プロンプトの内容を画像にどれだけ強く反映するかを決定する強度です。",
      slider_closeness_title: "顔의再現度",
      slider_closeness_tip: "値が高いほど、元の顔の特徴や目鼻立ちを忠実に維持します。",
      slider_detail_title: "ディテール鮮明度",
      slider_detail_tip: "肌の質感や顔의輪郭のシャープさ、微細な表現力を決定します。",
      render_btn_text: "スタイルレンダリング",
      render_btn_mock: "スタイルレンダリング (Mock)",
      render_btn_codex: "スタイルレンダリング (画像 2.0)",
      output_canvas_title: "出力キャンバス",
      empty_workspace_title: "空のワークスペース",
      empty_workspace_desc: "左側のパネルから写真をアップロードして設定を開始してください。",
      empty_workspace_ready: "レンダリング準備完了",
      empty_workspace_ready_desc: "スタイルを選び、下の生成ボタンをクリックしてください。",
      rendering_title: "AIアートレンダリング中 (約1分かかります)...",
      rendering_status: "カラーチャネルを分析中...",
      tab_memory: "神経衰弱",
      tab_tictactoe: "三目並べ",
      game_memory_title: "🎮 カード合わせゲーム",
      game_restart: "🔄 再スタート",
      game_ttt_title: "❌ 三目並べゲーム ⭕",
      game_ttt_status_your: "あなたのターン (X)",
      game_ttt_status_ai: "AI思考中 (O)...",
      game_ttt_status_win: "あなたの勝ち! 🎉",
      game_ttt_status_lose: "AIの勝ち! 🤖",
      game_ttt_status_draw: "引き分け! 🤝",
      label_source: "元の画像",
      label_styled_output: "スタイル適用後",
      control_contrast: "コントラスト",
      control_brightness: "明るさ",
      control_saturation: "彩度",
      sns_export_title: "SNSエクスポート設定",
      sns_format_label: "SNS形式比率",
      sns_opt_original: "オリジナルサイズ (1:1 正方形)",
      sns_opt_x_profile: "X プロフィール (400x400)",
      sns_opt_x_post: "X 投稿 (1200x675, 16:9)",
      sns_opt_linkedin_profile: "LinkedIn プロフィール (400x400)",
      sns_opt_linkedin_post: "LinkedIn 投稿 (1200x627, 1.91:1)",
      sns_opt_threads_profile: "Threads プロフィール (320x320)",
      sns_opt_threads_post: "Threads 投稿 (1080x1350, 4:5)",
      sns_opt_facebook_profile: "Facebook プロフィール (170x170)",
      sns_opt_facebook_post: "Facebook 投稿 (1200x630, 1.91:1)",
      sns_opt_instagram_story: "Instagram ストーリー (1080x1920, 9:16)",
      sns_crop_info_template: "<strong>{name}</strong> サイズにクロップして保存します。",
      sns_crop_info_pad: "ぼかし背景を追加し、<strong>{name}</strong> ({w}x{h}, 比率 {aspect}) 規格で保存されます。",
      btn_add_collection: "コレクションに保存",
      btn_add_collection_done: "保存完了!",
      btn_share_card: "シェアカードを生成",
      btn_download_image: "ダウンロード",
      history_collection_title: "コレクション履歴",
      history_collection_empty: "コレクションが空です。変換後にここに保存されます。",
      login_modal_title: "Codex CLI ログイン認証",
      login_modal_desc: "新しいブラウザタブで ChatGPT OAuth ログインを完了させてください。",
      login_modal_hint: "ログインが確認されると、この画面は自動的に閉じます。",
      btn_cancel: "キャンセル",
      library_modal_title: "スタイルテンプレートライブラリ",
      library_loading: "読み込み中...",
      library_search_placeholder: "スタイル名で検索...",
      category_all: "すべて",
      category_today: "本日のトレンド 🔥",
      category_portrait: "人物/ポートレート",
      category_illustration: "イラスト",
      category_cosplay: "コスプレ",
      category_photo: "エモーショナル写真",
      category_food: "食べ物/カフェ",
      category_product: "商品/広告",
      category_character: "キャラクター",
      category_sticker: "ステッカー",
      category_poster: "ポスター",
      category_other: "その他",
      btn_close: "閉じる",
      
      toast_connected: "Codexの連動に成功しました！",
      toast_gender_auto: "プロンプトの性別表現が [{gender}] 型に自動調整されました。",
      toast_gender_detect: "💡 分析結果: 自動的に [{gender}] プロフィールに設定されました。",
      toast_crop_complete: "📸 最適な構図調整のため、顔中心のズーム＆クロップを完了しました。",
      toast_animal_detect: "🐾 ペット検出: シャッフル時に動物イラストスタイルが優先適用されます。",
      toast_upload_error: "画像ファイルのみアップロード可能です。",
      toast_timeout: "⚠️ 生成タイムアウト (5分)。もう一度お試しください。",
      toast_gen_error: "⚠️ 画像生成に失敗しました。もう一度お試しください。",
      toast_network_error: "⚠️ ネットワークエラー: {msg}",
      toast_img_load_error: "画像読み込み失敗",
      toast_library_applied: "スタイルプロンプトが適用され、パラメータが自動調整されました！",
      toast_library_loading: "データベースを読み込み中です。しばらくしてから再度お試しください。",
      toast_unsupported_crop: "画像の形式がクロップをサポートしていません。",
      
      gender_name_male: "男性",
      gender_name_female: "女性",
      gender_adj_male: "男性型",
      gender_adj_female: "女性型",
      
      rolling_status_0: "顔の輪郭および目鼻立ちのランドマークを分析中...",
      rolling_status_1: "選択されたスタイルプリセットのブラシタッチをマッピング中...",
      rolling_status_2: "色調マトリックス補正および立体シェーディングを適用中...",
      rolling_status_3: "顔の肌の質感を維持し、テクスチャをアップスケーリング中...",
      rolling_status_4: "最終的な芸術的合成およびSNSエクスポート設定を準備中...",
      
      moves_count: "{moves}回移動",
      no_search_results: "検索結果が見つかりませんでした。",
      no_title: "(タイトルなし)",
      custom_style: "カスタムスタイル",
      delete_avatar: "アバターを削除",
      unknown_error: "不明なエラー",
      alert_login_init_failed: "ログイン初期化失敗: ",
      alert_login_error: "ログイン要求中にエラーが発生しました: ",
      start_job_failed: "レンダリング処理の開始に失敗しました",
      library_badge_text: "{count} 個のスタイル",
      toast_shuffle_applied: "🎲 ランダムスタイル適用：タグ [{tags}]"
    }
  };

  const TODAY_STYLE_LOCALIZATION = {
    ko: {
      "Y2K Retro Camcorder": {
        theme: "Y2K 레트로 캠코더",
        description: "2000년대 Y2K 감성 저화질 디카 플래시 뷰티"
      },
      "90s Yearbook Photo": {
        theme: "90년대 졸업 앨범",
        description: "90년대 감성 레트로 미국 고등학교 졸업앨범 스타일"
      },
      "Barbiecore Pink Fantasy": {
        theme: "바비코어 핑크 판타지",
        description: "화려한 핫핑크 톤의 플라스틱 판타지 스타일"
      },
      "Old Money Quiet Luxury": {
        theme: "올드 머니 클래식",
        description: "크림과 베이지 톤의 클래식 테니스 클럽 룩"
      },
      "Cyberpunk Neon Hologram": {
        theme: "사이버펑크 네온 홀로그램",
        description: "네온 컬러와 자줏빛 글리치 홀로그램 사이버 테크웨어"
      },
      "Coquette Ribbon & Lace": {
        theme: "코케트 리본 & 레이스",
        description: "로맨틱 빈티지 리본 앤 레이스 핑크 무드"
      },
      "3D Clay Toy Model": {
        theme: "3D 클레이 클레이메이션",
        description: "귀여운 점토 애니메이션 스타일의 3D 아바타"
      },
      "Retro Classic Anime Screen": {
        theme: "레트로 고전 애니메이션",
        description: "80-90년대 클래식 셀 채색 애니메이션 뷰"
      },
      "Pixar 3D Animation Style": {
        theme: "픽사 3D 애니메이션",
        description: "입체적이고 생생한 디즈니 픽사 애니메이션 스타일"
      },
      "Zombie Apocalypse Survivor": {
        theme: "좀비 서바이벌",
        description: "종말을 해치고 살아남은 거칠고 영화적인 생존자 프로필"
      }
    },
    en: {
      "Y2K Retro Camcorder": {
        theme: "Y2K Retro Camcorder",
        description: "Y2K aesthetic early 2000s low-res flash digital camera photography"
      },
      "90s Yearbook Photo": {
        theme: "90s Yearbook Photo",
        description: "90s aesthetic retro American high school yearbook style"
      },
      "Barbiecore Pink Fantasy": {
        theme: "Barbiecore Pink Fantasy",
        description: "Vibrant hot pink plastic fantasy style portrait"
      },
      "Old Money Quiet Luxury": {
        theme: "Old Money Quiet Luxury",
        description: "Cream and beige toned classic tennis club luxury look"
      },
      "Cyberpunk Neon Hologram": {
        theme: "Cyberpunk Neon Hologram",
        description: "Neon colors and purple glitch hologram cybernetic techwear"
      },
      "Coquette Ribbon & Lace": {
        theme: "Coquette Ribbon & Lace",
        description: "Romantic vintage pink ribbon and lace aesthetic portrait"
      },
      "3D Clay Toy Model": {
        theme: "3D Clay Toy Model",
        description: "Adorable clay animation style 3D personalized avatar"
      },
      "Retro Classic Anime Screen": {
        theme: "Retro Classic Anime Screen",
        description: "80s-90s classic cell-shaded retro anime screencap view"
      },
      "Pixar 3D Animation Style": {
        theme: "Pixar 3D Animation Style",
        description: "Three-dimensional vivid Disney Pixar style 3D character render"
      },
      "Zombie Apocalypse Survivor": {
        theme: "Zombie Apocalypse Survivor",
        description: "Gritty movie poster style post-apocalyptic survivor profile"
      }
    },
    es: {
      "Y2K Retro Camcorder": {
        theme: "Videocámara Retro Y2K",
        description: "Estética flash de cámara digital de baja resolución de los 2000"
      },
      "90s Yearbook Photo": {
        theme: "Foto del Anuario de los 90",
        description: "Estilo retro americano del anuario escolar de los años 90"
      },
      "Barbiecore Pink Fantasy": {
        theme: "Fantasía Rosa Barbiecore",
        description: "Estilo plástico de fantasía con tonos rosa brillante"
      },
      "Old Money Quiet Luxury": {
        theme: "Lujo Silencioso Old Money",
        description: "Look de club de tenis clásico en tonos crema y beige"
      },
      "Cyberpunk Neon Hologram": {
        theme: "Holograma de Neón Cyberpunk",
        description: "Ropa techwear cibernética con hologramas de glitch y colores de neón"
      },
      "Coquette Ribbon & Lace": {
        theme: "Lazo y Encaje Coquette",
        description: "Ambiente romántico rosa con lazos y encaje vintage"
      },
      "3D Clay Toy Model": {
        theme: "Modelo de Juguete de Arcilla 3D",
        description: "Lindo avatar 3D en estilo de animación de plastilina"
      },
      "Retro Classic Anime Screen": {
        theme: "Pantalla de Anime Clásico Retro",
        description: "Vista de animación clásica de celdas pintadas de los años 80 y 90"
      },
      "Pixar 3D Animation Style": {
        theme: "Estilo de Animación 3D Pixar",
        description: "Estilo de animación 3D vívido y tridimensional al estilo Disney Pixar"
      },
      "Zombie Apocalypse Survivor": {
        theme: "Sobreviviente de Apocalipsis Zombie",
        description: "Perfil rudo y cinematográfico de sobreviviente en el fin del mundo"
      }
    },
    zh: {
      "Y2K Retro Camcorder": {
        theme: "Y2K复古DV风",
        description: "2000年代低像素数码相机闪光灯美学"
      },
      "90s Yearbook Photo": {
        theme: "90年代校园复古毕业照",
        description: "90年代怀旧美式高中毕业纪念册风格"
      },
      "Barbiecore Pink Fantasy": {
        theme: "芭比粉红幻想",
        description: "亮粉色调的摩登塑料玩具世界风格"
      },
      "Old Money Quiet Luxury": {
        theme: "老钱风静奢主义",
        description: "奶白与米色调的经典网球俱乐部穿搭"
      },
      "Cyberpunk Neon Hologram": {
        theme: "赛博朋克霓虹全息",
        description: "霓虹色彩与紫红故障全息的科幻机能风"
      },
      "Coquette Ribbon & Lace": {
        theme: "少女感丝带与蕾丝",
        description: "浪漫复古粉红丝带与白色蕾丝情调"
      },
      "3D Clay Toy Model": {
        theme: "3D粘土玩具模型",
        description: "可爱粘土动画风格的3D个人化头像"
      },
      "Retro Classic Anime Screen": {
        theme: "复古经典动漫画面",
        description: "80-90年代手绘传统赛璐珞动画截图风"
      },
      "Pixar 3D Animation Style": {
        theme: "皮克斯3D动画风格",
        description: "皮克斯和迪士尼风格的3D人像画质"
      },
      "Zombie Apocalypse Survivor": {
        theme: "末日丧尸生存者",
        description: "历经劫难的粗犷电影海报级幸存者写照"
      }
    },
    ja: {
      "Y2K Retro Camcorder": {
        theme: "Y2K レトロビデオカメラ",
        description: "2000年代のY2K感性 低画質デジカメフラッシュビューティ"
      },
      "90s Yearbook Photo": {
        theme: "90年代 卒業アルバム写真",
        description: "90年代感性のレトロな米国高校のイヤーブック風"
      },
      "Barbiecore Pink Fantasy": {
        theme: "バービーコア ピンクファンタジー",
        description: "華やかなホットピンクのプラスチックファンタジースタイル"
      },
      "Old Money Quiet Luxury": {
        theme: "オールドマネー 静かなるラグジュアリー",
        description: "クリームとベージュトーン의클래식한테니스크럽풍룩"
      },
      "Cyberpunk Neon Hologram": {
        theme: "サイバーパンク ネオンホログラム",
        description: "ネオンカラーと紫のグリッチホログラム 사이버테크웨어"
      },
      "Coquette Ribbon & Lace": {
        theme: "コケット リボン＆レース",
        description: "ロマンチックなビンテージリボンとレースのピンクムード"
      },
      "3D Clay Toy Model": {
        theme: "3D クレイ粘土トイモデル",
        description: "かわいいクレイアニメ風の3Dアバター"
      },
      "Retro Classic Anime Screen": {
        theme: "レトロ クラシックアニメラスト",
        description: "80〜90年代のクラシックセル画アニメ風スクリーンショット"
      },
      "Pixar 3D Animation Style": {
        theme: "ピクサー 3D アニメスタイル",
        description: "立体的で生き生きとしたディズニー・ピクサーアニメ風"
      },
      "Zombie Apocalypse Survivor": {
        theme: "ゾンビサバイバー",
        description: "終末世界を生き抜いたタフでシ네마틱한생존자프로필"
      }
    }
  };

  let currentLang = localStorage.getItem('personafit_lang') || 'ko';
  let cachedTodayStyleData = null;
  let memoryTimerInterval = null;
  let memoryTime = 0;
  let memoryMoves = 0;
  let firstFlippedCard = null;
  let secondFlippedCard = null;
  let memoryMatchedCount = 0;
  let isCheckingMatch = false;
  let tttBoard = Array(9).fill('');
  let tttActive = true;
  let isAiThinking = false;
  let allPrompts = [];

  const snsPresets = {
    original: { name: 'Original Size (1:1)', w: null, h: null, aspect: '1:1' },
    'x-profile': { name: 'X Profile', w: 400, h: 400, aspect: '1:1' },
    'x-post': { name: 'X Post', w: 1200, h: 675, aspect: '16:9' },
    'linkedin-profile': { name: 'LinkedIn Profile', w: 400, h: 400, aspect: '1:1' },
    'linkedin-post': { name: 'LinkedIn Post', w: 1200, h: 627, aspect: '1.91:1' },
    'threads-profile': { name: 'Threads Profile', w: 320, h: 320, aspect: '1:1' },
    'threads-post': { name: 'Threads Post', w: 1080, h: 1350, aspect: '4:5' },
    'facebook-profile': { name: 'Facebook Profile', w: 170, h: 170, aspect: '1:1' },
    'facebook-post': { name: 'Facebook Post', w: 1200, h: 630, aspect: '1.91:1' },
    'instagram-story': { name: 'Instagram Story', w: 1080, h: 1920, aspect: '9:16' }
  };

  // UI Elements - Left Panel
  const uploadZone = document.getElementById('upload-zone');
  const fileInput = document.getElementById('file-input');
  const uploadPlaceholder = document.getElementById('upload-content-placeholder');
  const uploadPreviewContainer = document.getElementById('upload-preview-container');
  const uploadPreviewImg = document.getElementById('upload-preview-img');
  const removeImgBtn = document.getElementById('remove-img-btn');
  
  const presetItems = document.querySelectorAll('.preset-item');
  const customPrompt = document.getElementById('custom-prompt');
  const charCount = document.getElementById('char-count');
  const genderSelect = document.getElementById('gender-select');
  
  const sliderWeight = document.getElementById('slider-weight');
  const sliderWeightVal = document.getElementById('slider-weight-val');
  const sliderCloseness = document.getElementById('slider-closeness');
  const sliderClosenessVal = document.getElementById('slider-closeness-val');
  const sliderDetail = document.getElementById('slider-detail');
  const sliderDetailVal = document.getElementById('slider-detail-val');
  
  const generateBtn = document.getElementById('generate-btn');

  // UI Elements - Right Panel
  const displayFrame = document.getElementById('display-frame');
  const stateUploadRequired = document.getElementById('state-upload-required');
  const stateProcessing = document.getElementById('state-processing');
  const stateReady = document.getElementById('state-ready');
  
  const processingTitle = document.getElementById('processing-title');
  const progressBarFill = document.getElementById('progress-bar-fill');
  const processingStatus = document.getElementById('processing-status');
  
  const comparisonContainer = document.getElementById('comparison-container');
  const beforePanel = document.getElementById('before-panel');
  const afterPanel = document.getElementById('after-panel');
  const imgOriginal = document.getElementById('img-original');
  const imgTransformed = document.getElementById('img-transformed');
  const splitSliderBar = document.getElementById('split-slider-bar');
  
  const canvasControls = document.getElementById('canvas-controls-section');
  const filterContrast = document.getElementById('filter-contrast');
  const filterBrightness = document.getElementById('filter-brightness');
  const filterSaturation = document.getElementById('filter-saturation');

  const snsPresetSelect = document.getElementById('sns-preset-select');
  const snsCropInfo = document.getElementById('sns-crop-info');
  const snsDownloadSection = document.getElementById('sns-download-section');
  
  const actionTools = document.getElementById('action-tools');
  const saveHistoryBtn = document.getElementById('save-history-btn');
  const shareCardBtn = document.getElementById('share-card-btn');
  const downloadLink = document.getElementById('download-link');
  
  const galleryGrid = document.getElementById('gallery-grid');
  const galleryEmpty = document.getElementById('gallery-empty');

  // Header connection components
  const checkConnectionBtn = document.getElementById('check-connection-btn');
  const codexStatusBadge = document.getElementById('codex-status-badge');
  const connectCodexBtn = document.getElementById('connect-codex-btn');
  const loginModal = document.getElementById('login-modal');
  const cancelLoginBtn = document.getElementById('cancel-login-btn');

  // Style Library Elements
  const openLibraryBtn = document.getElementById('open-library-btn');
  const closeLibraryBtn = document.getElementById('close-library-btn');
  const libraryModal = document.getElementById('library-modal');
  const librarySearch = document.getElementById('library-search');
  const libraryGrid = document.getElementById('library-grid');
  const sidebarTabs = document.querySelectorAll('.sidebar-tab');

  // State Variables
  let isImageUploaded = false;
  let userImageSrc = null; // Original source uploaded by user
  let activeStyle = 'professional';
  let isDraggingSlider = false;
  let collection = [];
  let isCodexConnected = false;
  let pollingInterval = null;
  let activeCategory = 'all';
  let detectedImageType = 'person'; // 'person', 'animal', 'object'
  let isAnalyzingImage = false;
  let todayPrompt = '';
  let processingStatusInterval = null;

  // Initialize App
  init();

  function init() {
    loadCollectionFromStorage();
    setupEventListeners();
    
    // Initialize Language Selector
    const savedLang = localStorage.getItem('personafit_lang') || 'ko';
    applyLanguage(savedLang);
    
    checkCodexStatus();
    initLibrary();
    initMinigames();
    fetchTodayStyle();
  }

  // Load collection from localStorage
  function loadCollectionFromStorage() {
    const saved = localStorage.getItem('personafit_collection');
    if (saved) {
      try {
        collection = JSON.parse(saved);
        
        // Sanitize old data: if any item has a massive base64 imgSrc, prune or clean it to free storage!
        let hasLargeItems = false;
        collection = collection.map(item => {
          if (item.imgSrc && item.imgSrc.startsWith('data:') && item.imgSrc.length > 200000) {
            hasLargeItems = true;
            return {
              ...item,
              imgSrc: 'assets/default.png', // fallback placeholder to free up 2-3MB instantly!
              fullImgSrc: null
            };
          }
          return item;
        });

        if (hasLargeItems) {
          localStorage.setItem('personafit_collection', JSON.stringify(collection));
          console.log('Sanitized large items from local storage collection to prevent quota errors.');
        }

        renderGallery();
      } catch (e) {
        console.error('Failed to parse collection', e);
      }
    }
  }

  // Check backend link to Codex CLI doctor status
  function checkCodexStatus() {
    const urlParams = new URLSearchParams(window.location.search);
    const forceMock = urlParams.get('mock') === 'true';

    const icon = checkConnectionBtn ? checkConnectionBtn.querySelector('i') : null;
    if (icon) icon.classList.add('spinning');
    
    const translations = I18N[currentLang] || I18N['en'];
    if (codexStatusBadge) {
      codexStatusBadge.className = 'status-badge checking';
      codexStatusBadge.textContent = translations.codex_checking;
    }

    if (forceMock) {
      if (icon) icon.classList.remove('spinning');
      if (codexStatusBadge) {
        codexStatusBadge.className = 'status-badge disconnected';
        codexStatusBadge.textContent = translations.codex_offline;
      }
      isCodexConnected = false;
      if (generateBtn) {
        const btnText = generateBtn.querySelector('span');
        if (btnText) btnText.textContent = translations.render_btn_mock;
      }
      if (connectCodexBtn) {
        connectCodexBtn.classList.remove('hidden', 'btn-dimmed');
        const lbl = document.getElementById('connect-btn-label');
        if (lbl) lbl.textContent = translations.login;
      }
      return;
    }

    fetch('/api/status?_t=' + Date.now())
      .then(res => res.json())
      .then(data => {
        if (icon) icon.classList.remove('spinning');
        if (data.status === 'connected') {
          if (codexStatusBadge) {
            codexStatusBadge.className = 'status-badge connected';
            codexStatusBadge.textContent = translations.codex_connected;
          }
          isCodexConnected = true;
          if (generateBtn) {
            const btnText = generateBtn.querySelector('span');
            if (btnText) btnText.textContent = translations.render_btn_codex;
          }
          // 버튼은 항상 표시 - 연결됨 시 Reconnect으로 표시
          if (connectCodexBtn) {
            connectCodexBtn.classList.remove('hidden');
            connectCodexBtn.classList.add('btn-dimmed');
            const lbl = document.getElementById('connect-btn-label');
            if (lbl) lbl.textContent = translations.reconnect;
          }
        } else {
          if (codexStatusBadge) {
            codexStatusBadge.className = 'status-badge disconnected';
            codexStatusBadge.textContent = translations.codex_offline;
          }
          isCodexConnected = false;
          if (generateBtn) {
            const btnText = generateBtn.querySelector('span');
            if (btnText) btnText.textContent = translations.render_btn_mock;
          }
          if (connectCodexBtn) {
            connectCodexBtn.classList.remove('hidden', 'btn-dimmed');
            const lbl = document.getElementById('connect-btn-label');
            if (lbl) lbl.textContent = translations.login;
          }
        }
      })
      .catch(() => {
        if (icon) icon.classList.remove('spinning');
        if (codexStatusBadge) {
          codexStatusBadge.className = 'status-badge disconnected';
          codexStatusBadge.textContent = translations.codex_error;
        }
        isCodexConnected = false;
        if (generateBtn) {
          const btnText = generateBtn.querySelector('span');
          if (btnText) btnText.textContent = translations.render_btn_mock;
        }
        if (connectCodexBtn) {
          connectCodexBtn.classList.remove('hidden', 'btn-dimmed');
          const lbl = document.getElementById('connect-btn-label');
          if (lbl) lbl.textContent = translations.login;
        }
      });
  }

  // Start Codex OAuth Login Flow
  function startCodexLogin() {
    if (loginModal) loginModal.classList.remove('hidden');
    
    // Call backend login API to start process and open browser
    fetch('/api/login', { method: 'POST' })
      .then(res => res.json())
      .then(data => {
        const translations = I18N[currentLang] || I18N['en'];
        if (data.status === 'initiated') {
          startPollingStatus();
        } else {
          alert(translations.alert_login_init_failed + (data.message || translations.unknown_error));
          closeLoginModal();
        }
      })
      .catch(err => {
        const translations = I18N[currentLang] || I18N['en'];
        alert(translations.alert_login_error + err.message);
        closeLoginModal();
      });
  }

  // Cancel login flow
  function cancelCodexLogin() {
    fetch('/api/login/cancel', { method: 'POST' })
      .then(() => {
        closeLoginModal();
      })
      .catch(() => {
        closeLoginModal();
      });
  }

  // Close Login Modal
  function closeLoginModal() {
    if (loginModal) loginModal.classList.add('hidden');
    stopPollingStatus();
    checkCodexStatus();
  }

  function startPollingStatus() {
    if (pollingInterval) clearInterval(pollingInterval);
    
    pollingInterval = setInterval(() => {
      fetch('/api/status?_t=' + Date.now())
        .then(res => res.json())
        .then(data => {
          if (data.status === 'connected') {
            stopPollingStatus();
            if (loginModal) loginModal.classList.add('hidden');
            checkCodexStatus();
            const translations = I18N[currentLang] || I18N['en'];
            showToast(translations.toast_connected, 'success');
          }
        })
        .catch(err => console.error('Polling status failed', err));
    }, 1500);
  }

  function stopPollingStatus() {
    if (pollingInterval) {
      clearInterval(pollingInterval);
      pollingInterval = null;
    }
  }

  // Simple Toast Helper
  function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
      <i data-lucide="check-circle" style="width: 16px; height: 16px; color: #10b981;"></i>
      <span>${message}</span>
    `;
    document.body.appendChild(toast);
    lucide.createIcons();
    
    setTimeout(() => {
      toast.classList.add('show');
    }, 10);

    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => toast.remove(), 300);
    }, 3000);
  }

  // Set up all events
  function setupEventListeners() {
    // Header connection check click
    if (checkConnectionBtn) checkConnectionBtn.addEventListener('click', checkCodexStatus);
    
    // Codex login / connect clicks
    if (connectCodexBtn) connectCodexBtn.addEventListener('click', startCodexLogin);
    if (cancelLoginBtn) cancelLoginBtn.addEventListener('click', cancelCodexLogin);

    // Style Library triggers
    if (openLibraryBtn) openLibraryBtn.addEventListener('click', openLibrary);
    if (closeLibraryBtn) closeLibraryBtn.addEventListener('click', closeLibrary);
    if (librarySearch) librarySearch.addEventListener('input', filterLibrary);

    sidebarTabs.forEach(tab => {
      tab.addEventListener('click', () => {
        sidebarTabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        activeCategory = tab.dataset.category;
        filterLibrary();
      });
    });

    // File Upload Setup
    if (uploadZone) {
      uploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadZone.classList.add('dragover');
      });

      uploadZone.addEventListener('dragleave', () => {
        uploadZone.classList.remove('dragover');
      });

      uploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadZone.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
          handleFile(files[0]);
        }
      });
    }

    if (fileInput) {
      fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
          handleFile(e.target.files[0]);
        }
      });
    }

    if (removeImgBtn) {
      removeImgBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        resetUploader();
      });
    }

    presetItems.forEach(item => {
      item.addEventListener('click', () => {
        presetItems.forEach(p => p.classList.remove('active'));
        item.classList.add('active');
        activeStyle = item.dataset.style;
        
        // Populate custom prompt with description if preset selected
        if (customPrompt) {
          if (activeStyle === 'professional') {
            customPrompt.value = 'Professional corporate headshot, dark navy blazer, soft office lighting';
          } else if (activeStyle === 'travel') {
            customPrompt.value = 'Famous global landmark background, beautiful soft lighting, travel photography, highly detailed face, realistic background';
          } else if (activeStyle === 'cinematic') {
            customPrompt.value = 'Dramatic cinematic movie protagonist portrait, moody ambient lighting, highly detailed, film grain, anamorphic lens flare';
          } else if (activeStyle === 'today') {
            customPrompt.value = todayPrompt;
          } else {
            customPrompt.value = '';
          }
          updateCharCount();
        }
      });
    });

    // Prompt Char Counter
    if (customPrompt) {
      customPrompt.addEventListener('input', () => {
        updateCharCount();
      });
    }

    // Slider text bindings
    if (sliderWeight && sliderWeightVal) {
      sliderWeight.addEventListener('input', (e) => {
        sliderWeightVal.textContent = e.target.value;
      });
    }
    if (sliderCloseness && sliderClosenessVal) {
      sliderCloseness.addEventListener('input', (e) => {
        sliderClosenessVal.textContent = `${e.target.value}%`;
      });
    }
    if (sliderDetail && sliderDetailVal) {
      sliderDetail.addEventListener('input', (e) => {
        sliderDetailVal.textContent = `${e.target.value}%`;
      });
    }

    // Generate Button Click
    if (generateBtn) {
      generateBtn.addEventListener('click', () => {
        if (isImageUploaded) {
          runTransformation();
        }
      });
    }

    // Image Split Slider Interactions
    if (splitSliderBar) {
      splitSliderBar.addEventListener('mousedown', (e) => {
        isDraggingSlider = true;
        e.preventDefault();
      });

      splitSliderBar.addEventListener('touchstart', (e) => {
        isDraggingSlider = true;
      });
    }

    window.addEventListener('mouseup', () => {
      isDraggingSlider = false;
    });

    window.addEventListener('mousemove', (e) => {
      if (!isDraggingSlider) return;
      adjustSplitSlider(e.clientX);
    });

    window.addEventListener('touchend', () => {
      isDraggingSlider = false;
    });

    window.addEventListener('touchmove', (e) => {
      if (!isDraggingSlider || e.touches.length === 0) return;
      adjustSplitSlider(e.touches[0].clientX);
    });

    // Filter Controls
    [filterContrast, filterBrightness, filterSaturation].forEach(filter => {
      if (filter) {
        filter.addEventListener('input', applyPostFilters);
      }
    });

    // Save/Collection Actions
    if (saveHistoryBtn) {
      saveHistoryBtn.addEventListener('click', saveToCollection);
    }

    if (shareCardBtn) {
      shareCardBtn.addEventListener('click', generateShareCard);
    }

    if (snsPresetSelect) {
      snsPresetSelect.addEventListener('change', () => {
        updateSnsCropDescription();
        setupDownloadLink();
      });
    }

    // Language Dropdown Event Binding
    const langSelect = document.getElementById('lang-select');
    if (langSelect) {
      langSelect.addEventListener('change', (e) => {
        applyLanguage(e.target.value);
      });
    }

    if (genderSelect) {
      genderSelect.addEventListener('change', () => {
        const val = genderSelect.value;
        if (val !== 'random' && customPrompt && customPrompt.value.trim() !== '') {
          const adapted = adaptPromptGender(customPrompt.value, val);
          if (adapted !== customPrompt.value) {
            customPrompt.value = adapted;
            updateCharCount();
            showToast(`프롬프트의 성별 표현이 [${val === 'male' ? '남성형' : '여성형'}]으로 자동 조정되었습니다.`, 'success');
          }
        }
      });
    }
  }

  // Handle uploaded file
  function handleFile(file) {
    if (!file.type.startsWith('image/')) {
      alert('이미지 파일만 업로드할 수 있습니다.');
      return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
      userImageSrc = e.target.result;
      uploadPreviewImg.src = userImageSrc;
      
      // Update state
      isImageUploaded = true;
      uploadPlaceholder.classList.add('hidden');
      uploadPreviewContainer.classList.remove('hidden');
      generateBtn.disabled = false;

      // Update right side panel message to prompt instructions
      stateUploadRequired.querySelector('h3').textContent = '셋팅 준비 완료';
      stateUploadRequired.querySelector('p').textContent = '스타일을 선택하거나 프롬프트를 작성하고 아래 생성하기 버튼을 클릭하세요.';

      // Async Image Analysis Trigger
      runImageAnalysis(userImageSrc);
    };
    reader.readAsDataURL(file);
  }

  // Asynchronously query backend to detect gender & image type
  function runImageAnalysis(base64Image) {
    if (!genderSelect) return;
    
    isAnalyzingImage = true;
    detectedImageType = 'person'; // default

    // UI Feedback: disable genderSelect and show indicator
    genderSelect.disabled = true;
    const genderLabel = document.querySelector('.gender-label');
    const originalLabelText = genderLabel ? genderLabel.textContent : 'Gender';
    if (genderLabel) {
      genderLabel.innerHTML = '<span class="status-pulse-dot" style="display:inline-block;width:6px;height:6px;background:#3b82f6;border-radius:50%;margin-right:5px;animation:pulse 1s infinite;"></span>스캔중...';
    }

    fetch('/api/analyze-image', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ image: base64Image })
    })
    .then(res => res.json())
    .then(data => {
      isAnalyzingImage = false;
      genderSelect.disabled = false;
      if (genderLabel) genderLabel.textContent = originalLabelText;

      if (data.type) {
        detectedImageType = data.type;
      }

      // Auto-set gender if the user has not manually changed it yet (currently on 'random')
      if (genderSelect.value === 'random' && data.gender && data.gender !== 'unknown') {
        genderSelect.value = data.gender;
        showToast(`💡 사진 인식 결과: [${data.gender === 'male' ? '남성' : '여성'}] 프로필로 자동 설정되었습니다.`, 'success');
        
        // If there's already a prompt, convert it immediately
        if (customPrompt && customPrompt.value.trim() !== '') {
          const adapted = adaptPromptGender(customPrompt.value, data.gender);
          if (adapted !== customPrompt.value) {
            customPrompt.value = adapted;
            updateCharCount();
          }
        }
      }

      // Face Focus & Auto Crop
      if (data.bbox) {
        cropImageToFace(base64Image, data.bbox, (croppedSrc) => {
          userImageSrc = croppedSrc;
          if (uploadPreviewImg) {
            uploadPreviewImg.src = croppedSrc;
          }
          showToast('📸 최적의 이미지 구도 조정을 위해 얼굴 중심 줌-크롭을 완료했습니다.', 'success');
        });
      }

      if (detectedImageType === 'animal') {
        showToast(`🐾 인식 결과: 반려동물/동물 프로필로 감지되었습니다. 셔플 시 관련 일러스트 스타일이 우선 적용됩니다.`, 'success');
      }
    })
    .catch(err => {
      console.warn('Image analysis failed', err);
      isAnalyzingImage = false;
      genderSelect.disabled = false;
      if (genderLabel) genderLabel.textContent = originalLabelText;
    });
  }

  // Reset Uploader state
  function resetUploader() {
    if (fileInput) fileInput.value = '';
    if (uploadPreviewImg) uploadPreviewImg.src = '';
    userImageSrc = null;
    isImageUploaded = false;
    if (uploadPlaceholder) uploadPlaceholder.classList.remove('hidden');
    if (uploadPreviewContainer) uploadPreviewContainer.classList.add('hidden');
    if (generateBtn) generateBtn.disabled = true;

    // Reset right display states
    if (stateUploadRequired) {
      stateUploadRequired.classList.remove('hidden');
      const h3 = stateUploadRequired.querySelector('h3');
      const p = stateUploadRequired.querySelector('p');
      if (h3) h3.textContent = '업로드된 사진 없음';
      if (p) p.textContent = '왼쪽 패널에서 사진을 먼저 업로드하고 설정을 진행해 주세요.';
    }
    if (stateProcessing) stateProcessing.classList.add('hidden');
    if (stateReady) stateReady.classList.add('hidden');
    
    // Disable controls
    if (canvasControls) canvasControls.classList.add('disabled');
    if (actionTools) actionTools.classList.add('disabled');
    if (snsDownloadSection) snsDownloadSection.classList.add('disabled');
  }

  // Update char counter
  function updateCharCount() {
    if (!customPrompt || !charCount) return;
    const len = customPrompt.value.length;
    if (len > 200) {
      customPrompt.value = customPrompt.value.substring(0, 200);
    }
    charCount.textContent = customPrompt.value.length;
  }

  // Disable / Enable Left Panel Inputs during Rendering
  function setInputState(disabled) {
    if (fileInput) fileInput.disabled = disabled;
    if (customPrompt) customPrompt.disabled = disabled;
    if (genderSelect) genderSelect.disabled = disabled;
    if (sliderWeight) sliderWeight.disabled = disabled;
    if (sliderCloseness) sliderCloseness.disabled = disabled;
    if (sliderDetail) sliderDetail.disabled = disabled;
    if (generateBtn) generateBtn.disabled = disabled || !isImageUploaded;

    const shuffleBtnEl = document.getElementById('shuffle-prompt-btn');
    if (shuffleBtnEl) {
      shuffleBtnEl.disabled = disabled;
      if (disabled) shuffleBtnEl.classList.add('disabled-state');
      else shuffleBtnEl.classList.remove('disabled-state');
    }

    if (removeImgBtn) {
      removeImgBtn.disabled = disabled;
      if (disabled) removeImgBtn.classList.add('disabled-state');
      else removeImgBtn.classList.remove('disabled-state');
    }

    if (openLibraryBtn) {
      openLibraryBtn.disabled = disabled;
      if (disabled) openLibraryBtn.classList.add('disabled-state');
      else openLibraryBtn.classList.remove('disabled-state');
    }

    if (uploadZone) {
      if (disabled) uploadZone.classList.add('disabled-state');
      else uploadZone.classList.remove('disabled-state');
    }

    presetItems.forEach(item => {
      if (disabled) {
        item.classList.add('disabled-state');
      } else {
        item.classList.remove('disabled-state');
      }
    });
  }

  function startStatusRolling() {
    if (processingStatusInterval) clearInterval(processingStatusInterval);
    const translations = I18N[currentLang] || I18N['en'];
    const processingMessages = [
      translations.rolling_status_0,
      translations.rolling_status_1,
      translations.rolling_status_2,
      translations.rolling_status_3,
      translations.rolling_status_4
    ];
    let index = 0;
    processingStatus.textContent = processingMessages[index];
    
    processingStatusInterval = setInterval(() => {
      index = (index + 1) % processingMessages.length;
      processingStatus.textContent = processingMessages[index];
    }, 2000);
  }

  function stopStatusRolling() {
    if (processingStatusInterval) {
      clearInterval(processingStatusInterval);
      processingStatusInterval = null;
    }
  }

  // Simulator Processing Pipeline
  function runTransformation() {
    setInputState(true);
    stateUploadRequired.classList.add('hidden');
    stateReady.classList.add('hidden');
    stateProcessing.classList.remove('hidden');
    
    // Smooth scroll to output canvas to improve mobile usability
    if (displayFrame) {
      displayFrame.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
    
    startMinigames();
    startStatusRolling();

    // Reset progress fill
    progressBarFill.style.width = '0%';
    
    if (isCodexConnected) {
      // Real API generation using Codex CLI (async job mode)
      processingTitle.textContent = 'Generating with Image 2.0...';
      processingStatus.textContent = 'Initializing Codex CLI session (Image 2.0)...';
      progressBarFill.style.width = '10%';

      // Slowly increment progress bar while Image 2.0 is generating
      let progress = 10;
      const progressInterval = setInterval(() => {
        if (progress < 90) {
          progress += Math.floor(Math.random() * 4) + 1;
          if (progress > 90) progress = 90;
          progressBarFill.style.width = `${progress}%`;
        }
      }, 700);

      // Step 1: POST to start async job
      fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          image: userImageSrc,
          prompt: customPrompt.value || activeStyle,
          style: activeStyle,
          gender: genderSelect ? genderSelect.value : 'random',
          closeness: sliderCloseness ? parseInt(sliderCloseness.value) : 80,
          weight: sliderWeight ? parseFloat(sliderWeight.value) : 7.5
        })
      })
      .then(res => res.json())
      .then(startData => {
        const translations = I18N[currentLang] || I18N['en'];
        if (!startData.success || !startData.job_id) {
          throw new Error(startData.error || translations.start_job_failed);
        }

        const jobId = startData.job_id;
        processingStatus.textContent = translations.job_started_polling.replace('{id}', jobId);

        // Step 2: Poll GET /api/generate/{job_id} until done or error
        let attempts = 0;
        const maxAttempts = 100; // 100 × 3s = 5 minutes max

        const pollTimer = setInterval(() => {
          attempts++;
          if (attempts > maxAttempts) {
            clearInterval(pollTimer);
            clearInterval(progressInterval);
            const translations = I18N[currentLang] || I18N['en'];
            showToast(translations.toast_timeout, 'error');
            resetProgressState();
            setInputState(false);
            return;
          }

          fetch(`/api/generate/${jobId}?_t=${Date.now()}`)
            .then(r => r.json())
            .then(pollData => {
              if (pollData.status === 'pending') {
                return; // still running — keep polling
              }

              clearInterval(pollTimer);
              clearInterval(progressInterval);
              const translations = I18N[currentLang] || I18N['en'];

              if (pollData.success && pollData.status === 'done') {
                progressBarFill.style.width = '100%';
                processingStatus.textContent = translations.generation_complete;
                stopStatusRolling();
                setTimeout(() => {
                  stopMinigames();
                  stateProcessing.classList.add('hidden');
                  stateReady.classList.remove('hidden');
                  imgOriginal.src = userImageSrc;
                  imgTransformed.src = pollData.image;

                  afterPanel.style.width = '50%';
                  splitSliderBar.style.left = '50%';

                  filterContrast.value = 100;
                  filterBrightness.value = 100;
                  filterSaturation.value = 100;
                  imgTransformed.style.filter = 'none';

                  canvasControls.classList.remove('disabled');
                  actionTools.classList.remove('disabled');
                  if (snsDownloadSection) snsDownloadSection.classList.remove('disabled');
                  setupDownloadLink();
                  setInputState(false);
                }, 400);
              } else {
                const errMsg = pollData.error || translations.unknown_error;
                stopMinigames();
                resetProgressState();
                setInputState(false);
                showToast(translations.toast_gen_error, 'error');
                console.error('Generation error:', errMsg);
              }
            })
            .catch(err => {
              console.warn('Poll attempt failed, retrying...', err);
              // don't stop — next interval will retry
            });
        }, 3000); // poll every 3 seconds
      })
      .catch(err => {
        clearInterval(progressInterval);
        const translations = I18N[currentLang] || I18N['en'];
        showToast(translations.toast_network_error.replace('{msg}', err.message), 'error');
        resetProgressState();
        setInputState(false);
      });



    } else {
      // Mock / Offline Filter Transformation
      const translations = I18N[currentLang] || I18N['en'];
      processingTitle.textContent = translations.mock_rendering_title;
      const steps = [
        { prg: 25 },
        { prg: 50 },
        { prg: 80 },
        { prg: 100 }
      ];

      let currentStepIdx = 0;
      const interval = setInterval(() => {
        if (currentStepIdx < steps.length) {
          const step = steps[currentStepIdx];
          progressBarFill.style.width = `${step.prg}%`;
          currentStepIdx++;
        } else {
          clearInterval(interval);
          setTimeout(() => {
            finalizeTransformation();
            setInputState(false);
          }, 300);
        }
      }, 1500); // 1.5 seconds per step, 6s total
    }
  }

  function resetProgressState() {
    stopStatusRolling();
    stopMinigames();
    stateProcessing.classList.add('hidden');
    stateUploadRequired.classList.remove('hidden');
    canvasControls.classList.add('disabled');
    actionTools.classList.add('disabled');
    if (snsDownloadSection) snsDownloadSection.classList.add('disabled');
  }

  // Render & setup transformed results for Mock settings
  function finalizeTransformation() {
    stopStatusRolling();
    stopMinigames();
    stateProcessing.classList.add('hidden');
    stateReady.classList.remove('hidden');
    
    // Configure Comparison original image
    imgOriginal.src = userImageSrc;

    // Apply Transformation Logic
    // If user uses default sample avatar face, show pre-generated templates
    const isUsingDefaultMock = userImageSrc.includes('default_avatar') || userImageSrc.startsWith('data:image');
    
    if (isUsingDefaultMock && activeStyle === 'professional') {
      imgTransformed.src = 'assets/professional.png';
    } else {
      applyCanvasStyleTransformation();
    }

    // Reset slider split back to 50%
    afterPanel.style.width = '50%';
    splitSliderBar.style.left = '50%';

    // Reset filters
    filterContrast.value = 100;
    filterBrightness.value = 100;
    filterSaturation.value = 100;
    imgTransformed.style.filter = 'none';

    // Enable panels
    canvasControls.classList.remove('disabled');
    actionTools.classList.remove('disabled');
    if (snsDownloadSection) snsDownloadSection.classList.remove('disabled');

    // Bind Download Trigger
    setupDownloadLink();
  }

  // Core Canvas Engine - transforms custom uploaded photos on client side
  function applyCanvasStyleTransformation() {
    const img = new Image();
    img.src = userImageSrc;
    img.onload = () => {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      canvas.width = img.naturalWidth;
      canvas.height = img.naturalHeight;
      
      // Draw base photo
      ctx.drawImage(img, 0, 0);

      // Perform Style Adjustments
      if (activeStyle === 'professional') {
        // Business look: Soft corporate glow and subtle lighting warm gradient
        ctx.globalCompositeOperation = 'source-over';
        ctx.fillStyle = 'rgba(255, 235, 210, 0.08)'; // Warm corporate tint
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // Add subtle radial white vignette to center lighting
        const gradient = ctx.createRadialGradient(
          canvas.width / 2, canvas.height / 2, 50,
          canvas.width / 2, canvas.height / 2, canvas.width / 1.2
        );
        gradient.addColorStop(0, 'rgba(255, 255, 255, 0.15)');
        gradient.addColorStop(1, 'rgba(0, 0, 0, 0.15)');
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, canvas.width, canvas.height);

      } else if (activeStyle === 'travel') {
        // Travel: Sunny warmth and enhanced exposure
        ctx.globalCompositeOperation = 'source-over';
        ctx.fillStyle = 'rgba(255, 220, 160, 0.06)'; // Warm sunlight tint
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // Soft gradient overlay to brighten details
        const grad = ctx.createLinearGradient(0, 0, 0, canvas.height);
        grad.addColorStop(0, 'rgba(255, 255, 255, 0.12)'); // Sunny sky glow
        grad.addColorStop(1, 'rgba(0, 0, 0, 0.05)');
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, canvas.width, canvas.height);

      } else if (activeStyle === 'cinematic') {
        // Cinematic: Movie moody gradient (teal and orange tones)
        ctx.globalCompositeOperation = 'multiply';
        ctx.fillStyle = 'rgba(25, 45, 55, 0.15)'; // Deep blue-teal shade mapping
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.globalCompositeOperation = 'screen';
        const cinemGrad = ctx.createRadialGradient(
          canvas.width / 2, canvas.height / 2, 20,
          canvas.width / 2, canvas.height / 2, canvas.width / 1.1
        );
        cinemGrad.addColorStop(0, 'rgba(255, 175, 110, 0.28)'); // Warm cinematic spotlight
        cinemGrad.addColorStop(1, 'rgba(10, 30, 45, 0.2)');     // Dark teal vignetting
        ctx.fillStyle = cinemGrad;
        ctx.fillRect(0, 0, canvas.width, canvas.height);
      }

      imgTransformed.src = canvas.toDataURL('image/png');
      setTimeout(setupDownloadLink, 100);
    };
  }

  // Adjust Comparison Split drag position
  function adjustSplitSlider(clientX) {
    const rect = comparisonContainer.getBoundingClientRect();
    let position = clientX - rect.left;
    
    // Clamp values
    if (position < 0) position = 0;
    if (position > rect.width) position = rect.width;

    const percentage = (position / rect.width) * 100;
    afterPanel.style.width = `${percentage}%`;
    splitSliderBar.style.left = `${percentage}%`;
  }

  // Apply Brightness/Contrast/Saturation filter adjustments
  function applyPostFilters() {
    const contrastVal = filterContrast.value;
    const brightnessVal = filterBrightness.value;
    const saturationVal = filterSaturation.value;

    imgTransformed.style.filter = `contrast(${contrastVal}%) brightness(${brightnessVal}%) saturate(${saturationVal}%)`;
    setupDownloadLink();
  }


  // Render transformed image on high-quality canvas and bind to download tag
  function setupDownloadLink() {
    const presetKey = snsPresetSelect ? snsPresetSelect.value : 'original';
    const preset = snsPresets[presetKey] || snsPresets.original;

    const img = new Image();
    img.src = imgTransformed.src;
    img.onload = () => {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      
      const contrastVal = filterContrast.value;
      const brightnessVal = filterBrightness.value;
      const saturationVal = filterSaturation.value;

      // Determine dimensions
      let targetW = preset.w;
      let targetH = preset.h;
      
      if (!targetW || !targetH) {
        targetW = img.naturalWidth || 600;
        targetH = img.naturalHeight || 600;
      }

      canvas.width = targetW;
      canvas.height = targetH;

      const filterStr = `contrast(${contrastVal}%) brightness(${brightnessVal}%) saturate(${saturationVal}%)`;

      if (preset.aspect === '1:1') {
        ctx.filter = filterStr;
        ctx.drawImage(img, 0, 0, targetW, targetH);
      } else {
        // Blurred background cover
        ctx.filter = `${filterStr} blur(30px) brightness(0.35)`;
        
        const imgAspect = img.naturalWidth / img.naturalHeight;
        const targetAspect = targetW / targetH;
        let bgW, bgH, bgX, bgY;
        
        if (imgAspect > targetAspect) {
          bgH = targetH;
          bgW = targetH * imgAspect;
          bgX = (targetW - bgW) / 2;
          bgY = 0;
        } else {
          bgW = targetW;
          bgH = targetW / imgAspect;
          bgX = 0;
          bgY = (targetH - bgH) / 2;
        }
        ctx.drawImage(img, bgX, bgY, bgW, bgH);

        // Center original square avatar
        ctx.filter = filterStr;
        let size = Math.min(targetW, targetH);
        
        if (presetKey === 'instagram-story') {
          size = Math.floor(targetW * 0.65);
        } else {
          size = Math.min(targetW, targetH) - 40;
        }
        
        const cX = (targetW - size) / 2;
        const cY = (targetH - size) / 2;
        
        ctx.drawImage(img, cX, cY, size, size);
      }

      downloadLink.href = canvas.toDataURL('image/png');
      downloadLink.download = `persona-avatar-${presetKey}.png`;
    };
  }

  // Generates a high-quality 1200x600 Before/After share card with vertical split and watermark branding
  function generateShareCard() {
    const imgOrig = new Image();
    imgOrig.crossOrigin = "anonymous";
    imgOrig.src = imgOriginal.src;
    
    const imgTrans = new Image();
    imgTrans.crossOrigin = "anonymous";
    imgTrans.src = imgTransformed.src;

    let loadedCount = 0;
    const onImgLoad = () => {
      loadedCount++;
      if (loadedCount === 2) {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = 1200;
        canvas.height = 600;

        // 1. Draw Original (Before) on the Left
        ctx.filter = 'none';
        ctx.drawImage(imgOrig, 0, 0, 600, 600);

        // 2. Draw Transformed (After) on the Right
        const contrastVal = filterContrast.value;
        const brightnessVal = filterBrightness.value;
        const saturationVal = filterSaturation.value;
        ctx.filter = `contrast(${contrastVal}%) brightness(${brightnessVal}%) saturate(${saturationVal}%)`;
        ctx.drawImage(imgTrans, 600, 0, 600, 600);

        // 3. Draw vertical divider down the center
        ctx.filter = 'none';
        ctx.strokeStyle = '#121316';
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.moveTo(600, 0);
        ctx.lineTo(600, 600);
        ctx.stroke();

        // 4. Draw premium branding bar at the bottom
        ctx.fillStyle = 'rgba(12, 13, 15, 0.82)';
        ctx.fillRect(0, 540, 1200, 60);

        // Text - Left side (Branding logo)
        ctx.font = '600 15px Outfit, sans-serif';
        ctx.fillStyle = '#ffffff';
        ctx.textAlign = 'left';
        ctx.textBaseline = 'middle';
        ctx.fillText('PERSONAFIT STUDIO', 40, 570);

        // Text - Right side (URL or tagline)
        ctx.font = '300 13px Inter, sans-serif';
        ctx.fillStyle = '#84868f';
        ctx.textAlign = 'right';
        ctx.fillText('Art-Directed Visual Identity  ·  personafit.ai', 1160, 570);

        // 5. Trigger download
        const link = document.createElement('a');
        link.download = `personafit-share-card-${activeStyle}.png`;
        link.href = canvas.toDataURL('image/png');
        link.click();
      }
    };

    imgOrig.onload = onImgLoad;
    imgTrans.onload = onImgLoad;
    const translations = I18N[currentLang] || I18N['en'];
    imgOrig.onerror = () => showToast(translations.toast_img_load_error, 'error');
    imgTrans.onerror = () => showToast(translations.toast_img_load_error, 'error');
  }

  // Helper to compress large base64 images into tiny thumbnails (150x150 JPEG, 60% quality)
  function createThumbnail(src, callback) {
    if (!src || !src.startsWith('data:')) {
      callback(src);
      return;
    }
    const img = new Image();
    img.src = src;
    img.onload = () => {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      canvas.width = 150;
      canvas.height = 150;
      ctx.drawImage(img, 0, 0, 150, 150);
      try {
        const thumb = canvas.toDataURL('image/jpeg', 0.6);
        callback(thumb);
      } catch (err) {
        callback(src);
      }
    };
    img.onerror = () => {
      callback(src);
    };
  }

  // Save Current Styled Avatar to Local Storage Collection
  function saveToCollection() {
    const styleLabelMap = {
      professional: '비즈니스 프로필',
      travel: '여행 테마',
      cinematic: '시네마틱'
    };

    createThumbnail(imgTransformed.src, (thumbSrc) => {
      // Store full image only if it is a URL or a small inline data URL (e.g. < 200KB)
      const isLargeDataUrl = imgTransformed.src.startsWith('data:') && imgTransformed.src.length > 200000;
      const fullImgVal = isLargeDataUrl ? null : imgTransformed.src;

      const newItem = {
        id: 'avatar_' + Date.now(),
        imgSrc: thumbSrc,
        fullImgSrc: fullImgVal,
        style: activeStyle,
        styleLabel: styleLabelMap[activeStyle] || '커스텀 스타일',
        date: new Date().toLocaleDateString('ko-KR', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit'
        }),
        filters: {
          contrast: filterContrast.value,
          brightness: filterBrightness.value,
          saturation: filterSaturation.value
        }
      };

      collection.unshift(newItem);
      
      try {
        localStorage.setItem('personafit_collection', JSON.stringify(collection));
      } catch (e) {
        console.warn('QuotaExhaustedError: storage full, pruning old items.', e);
        // Prune older collection items to prevent crashing
        if (collection.length > 8) {
          collection = collection.slice(0, 8);
          try {
            localStorage.setItem('personafit_collection', JSON.stringify(collection));
          } catch (e2) {
            console.error('Failed to save collection after pruning:', e2);
          }
        }
      }

      // Add effect & feedback
      saveHistoryBtn.classList.add('disabled-state');
      const translations = I18N[currentLang] || I18N['en'];
      saveHistoryBtn.innerHTML = `<i data-lucide="check" class="btn-icon-inline"></i><span>${translations.btn_add_collection_done}</span>`;
      lucide.createIcons();

      setTimeout(() => {
        saveHistoryBtn.classList.remove('disabled-state');
        saveHistoryBtn.innerHTML = `<i data-lucide="bookmark" class="btn-icon-inline"></i><span>${translations.btn_add_collection}</span>`;
        lucide.createIcons();
      }, 1500);

      renderGallery();
    });
  }

  // Redraw gallery cards
  function renderGallery() {
    if (collection.length === 0) {
      galleryEmpty.classList.remove('hidden');
      return;
    }

    galleryEmpty.classList.add('hidden');
    galleryGrid.querySelectorAll('.gallery-card').forEach(c => c.remove());

    const translations = I18N[currentLang] || I18N['en'];

    collection.forEach(item => {
      const card = document.createElement('div');
      card.className = 'gallery-card';
      
      const badgeClass = `style-${item.style}`;
      
      let localizedStyleLabel = item.styleLabel;
      if (item.style === 'professional') localizedStyleLabel = translations.preset_corporate_name;
      else if (item.style === 'travel') localizedStyleLabel = translations.preset_travel_name;
      else if (item.style === 'cinematic') localizedStyleLabel = translations.preset_cinematic_name;
      else if (item.style === 'today') {
        const trend = Object.keys(TODAY_STYLE_LOCALIZATION[currentLang] || {}).find(k => k === item.styleLabel || (TODAY_STYLE_LOCALIZATION['ko'][k] && TODAY_STYLE_LOCALIZATION['ko'][k].theme === item.styleLabel));
        if (trend) {
          localizedStyleLabel = TODAY_STYLE_LOCALIZATION[currentLang][trend].theme;
        } else {
          localizedStyleLabel = translations.preset_today_name;
        }
      } else if (item.style === 'custom') {
        localizedStyleLabel = translations.custom_style;
      }

      card.innerHTML = `
        <div class="gallery-card-img-wrapper">
          <img src="${item.imgSrc}" alt="${localizedStyleLabel}">
          <span class="gallery-card-badge ${badgeClass}">${localizedStyleLabel}</span>
          <button class="gallery-card-delete-btn" data-id="${item.id}" title="${translations.delete_avatar}">
            <i data-lucide="x" style="width: 14px; height: 14px;"></i>
          </button>
        </div>
        <div class="gallery-card-info">
          <span class="gallery-card-title">${localizedStyleLabel}</span>
          <span class="gallery-card-date">${item.date}</span>
        </div>
      `;

      // Event listener to delete a single item
      card.querySelector('.gallery-card-delete-btn').addEventListener('click', (e) => {
        e.stopPropagation();
        deleteCollectionItem(item.id);
      });

      // Event listener to reload history item back to canvas for review
      card.addEventListener('click', () => {
        imgOriginal.src = userImageSrc || item.fullImgSrc || item.imgSrc;
        imgTransformed.src = item.fullImgSrc || item.imgSrc;
        
        filterContrast.value = item.filters.contrast || 100;
        filterBrightness.value = item.filters.brightness || 100;
        filterSaturation.value = item.filters.saturation || 100;
        imgTransformed.style.filter = `contrast(${filterContrast.value}%) brightness(${filterBrightness.value}%) saturate(${filterSaturation.value}%)`;

        stateUploadRequired.classList.add('hidden');
        stateProcessing.classList.add('hidden');
        stateReady.classList.remove('hidden');

        canvasControls.classList.remove('disabled');
        actionTools.classList.remove('disabled');
        if (snsDownloadSection) snsDownloadSection.classList.remove('disabled');
        setupDownloadLink();
      });

      galleryGrid.appendChild(card);
    });

    lucide.createIcons();
  }

  // Delete a saved avatar
  function deleteCollectionItem(id) {
    collection = collection.filter(item => item.id !== id);
    try {
      localStorage.setItem('personafit_collection', JSON.stringify(collection));
    } catch (e) {
      console.error('Failed to update storage after deletion:', e);
    }
    renderGallery();
  }



  // ========================
  // REACTOR PROMPT LIBRARY (1800개 라이브 연동)
  // ========================

  let filteredPrompts = [];  // 필터된 결과
  let currentPage = 0;
  const PAGE_SIZE = 24;
  let isLoadingMore = false;
  let activeLibCategory = 'all';

  // 카테고리 → 자동 슬라이더 튜닝 테이블
  const categoryTuning = {
    portrait: { weight: 6.5, closeness: 85, detail: 45 },
    photo:    { weight: 6.5, closeness: 85, detail: 45 },
    cosplay:  { weight: 9.5, closeness: 55, detail: 65 },
    character:{ weight: 9.5, closeness: 55, detail: 65 },
    illustration:{ weight: 9.0, closeness: 60, detail: 60 },
    plush:    { weight: 8.5, closeness: 65, detail: 50 },
    sticker:  { weight: 8.0, closeness: 65, detail: 55 },
    food:     { weight: 7.0, closeness: 75, detail: 55 },
    product:  { weight: 7.0, closeness: 75, detail: 55 },
    poster:   { weight: 8.5, closeness: 60, detail: 60 },
    infographic:{ weight: 7.5, closeness: 70, detail: 50 },
    design:   { weight: 7.5, closeness: 70, detail: 50 },
    other:    { weight: 7.5, closeness: 70, detail: 50 }
  };


  function updateTodayStyleDisplay() {
    if (!cachedTodayStyleData) return;
    const descEl = document.getElementById('today-preset-desc');
    const nameEl = document.getElementById('today-preset-name');
    
    const themeKey = cachedTodayStyleData.theme;
    const localized = TODAY_STYLE_LOCALIZATION[currentLang] && TODAY_STYLE_LOCALIZATION[currentLang][themeKey];
    
    const displayTheme = localized ? localized.theme : cachedTodayStyleData.theme;
    const displayDesc = localized ? localized.description : cachedTodayStyleData.description;
    
    if (descEl) {
      descEl.textContent = displayDesc || '';
      descEl.title = displayTheme || '';
    }
    if (nameEl) {
      nameEl.textContent = displayTheme || '';
    }
  }

  function fetchTodayStyle() {
    fetch('/api/today-style')
      .then(r => r.json())
      .then(data => {
        cachedTodayStyleData = data;
        updateTodayStyleDisplay();
        todayPrompt = data.prompt || '';
      })
      .catch(err => {
        console.error('Failed to fetch today style:', err);
        const descEl = document.getElementById('today-preset-desc');
        const translations = I18N[currentLang] || I18N['en'];
        if (descEl) descEl.textContent = translations.preset_today_desc;
      });
  }

  function initLibrary() {
    // gallery-data.json 비동기 로드
    fetch('/gallery-data.json?_t=' + Date.now())
      .then(r => r.json())
      .then(data => {
        allPrompts = (data.posts || []).filter(p => p.prompt && p.prompt.trim());
        updateLibraryCount();
        // 내장 DB는 fallback용으로 유지 (필요 시 아래 stylePresetsDatabase 사용)
      })
      .catch(err => {
        console.warn('gallery-data.json 로드 실패, 내장 DB 사용:', err);
        allPrompts = stylePresetsDatabase.map(s => ({
          id: s.id,
          caption: s.title,
          prompt: s.prompt,
          thumbnail: null,
          tags: [s.category]
        }));
        updateLibraryCount();
      });
  }

  function updateLibraryCount() {
    const badge = document.getElementById('library-count-badge');
    const translations = I18N[currentLang] || I18N['en'];
    if (badge) {
      const formattedCount = allPrompts.length.toLocaleString();
      const template = translations.library_badge_text || "{count} prompts";
      badge.textContent = template.replace('{count}', formattedCount);
    }
  }

  function openLibrary() {
    if (libraryModal) {
      libraryModal.classList.remove('hidden');
      if (librarySearch) {
        librarySearch.value = '';
        librarySearch.focus();
      }
      activeLibCategory = 'all';
      document.querySelectorAll('.sidebar-tab').forEach(t => t.classList.remove('active'));
      const allTab = document.querySelector('.sidebar-tab[data-category="all"]');
      if (allTab) allTab.classList.add('active');
      resetAndRender();
    }
  }

  function closeLibrary() {
    if (libraryModal) libraryModal.classList.add('hidden');
  }

  function resetAndRender() {
    currentPage = 0;
    filteredPrompts = getFiltered();
    libraryGrid.innerHTML = '';
    renderPage();
    // 무한 스크롤 바인딩
    const gridContainer = document.querySelector('.library-grid-container');
    if (gridContainer) {
      gridContainer.onscroll = () => {
        if (gridContainer.scrollTop + gridContainer.clientHeight >= gridContainer.scrollHeight - 200) {
          if (!isLoadingMore && currentPage * PAGE_SIZE < filteredPrompts.length) {
            renderPage();
          }
        }
      };
    }
  }

  function getFiltered() {
    const query = librarySearch ? librarySearch.value.toLowerCase().trim() : '';
    return allPrompts.filter(p => {
      const catMatch = (activeLibCategory === 'all') ||
        (p.tags && p.tags.some(t => t.toLowerCase() === activeLibCategory));
      const qMatch = !query ||
        (p.caption && p.caption.toLowerCase().includes(query)) ||
        (p.prompt && p.prompt.toLowerCase().includes(query));
      return catMatch && qMatch;
    });
  }

  function renderPage() {
    isLoadingMore = true;
    const start = currentPage * PAGE_SIZE;
    const end = Math.min(start + PAGE_SIZE, filteredPrompts.length);
    const slice = filteredPrompts.slice(start, end);

    if (start === 0 && slice.length === 0) {
      const translations = I18N[currentLang] || I18N['en'];
      libraryGrid.innerHTML = `<p style="grid-column:1/-1;text-align:center;color:var(--text-muted);padding:40px 0;">${translations.no_search_results}</p>`;
      isLoadingMore = false;
      return;
    }

    slice.forEach(post => {
      const card = document.createElement('div');
      card.className = 'style-card reactor-card';
      card.addEventListener('click', () => applyReactorStyle(post));

      const imgSrc = post.thumbnail;

      const tags = (post.tags || ['other']);
      const tagHTML = tags.map(t => `<span class="reactor-tag">${t}</span>`).join('');

      const captionShort = (post.caption || '').replace(/\n/g, ' ').substring(0, 60);
      const promptShort = (post.prompt || '').substring(0, 80);

      card.innerHTML = `
        <div class="style-card-preview reactor-preview">
          ${imgSrc
            ? `<img src="${imgSrc}" loading="lazy" alt="preview" onerror="if(!this.dataset.fallback){this.dataset.fallback='true';this.src='https://reactorprompt.vercel.app'+this.getAttribute('src');}else{this.parentNode.style.background='linear-gradient(135deg,#1f2937,#111827)';this.remove();}">`
            : `<div class="no-thumb-placeholder"><i data-lucide="image" style="width:32px;height:32px;opacity:0.3;"></i></div>`
          }
          <div class="reactor-tag-row">${tagHTML}</div>
        </div>
        <div class="style-card-info">
          <h4 class="style-card-title">${captionShort || (I18N[currentLang] || I18N['en']).no_title}</h4>
          <p class="style-card-desc">${promptShort}...</p>
        </div>
      `;
      libraryGrid.appendChild(card);
    });

    lucide.createIcons();
    currentPage++;
    isLoadingMore = false;
  }

  function filterLibrary() {
    resetAndRender();
  }

  function applyReactorStyle(post) {
    // 프롬프트 주입
    if (customPrompt) {
      let promptText = (post.prompt || '').substring(0, 200);
      const currentGender = genderSelect ? genderSelect.value : 'random';
      if (currentGender !== 'random') {
        promptText = adaptPromptGender(promptText, currentGender);
      }
      customPrompt.value = promptText;
      updateCharCount();
    }

    // 카테고리 기반 자동 슬라이더 튜닝
    const primaryTag = (post.tags && post.tags[0]) || 'other';
    const tuning = categoryTuning[primaryTag] || categoryTuning.other;

    if (sliderWeight) {
      sliderWeight.value = tuning.weight;
      sliderWeightVal.textContent = tuning.weight;
    }
    if (sliderCloseness) {
      sliderCloseness.value = tuning.closeness;
      sliderClosenessVal.textContent = `${tuning.closeness}%`;
    }
    if (sliderDetail) {
      sliderDetail.value = tuning.detail;
      sliderDetailVal.textContent = `${tuning.detail}%`;
    }

    presetItems.forEach(p => p.classList.remove('active'));
    activeStyle = 'custom';

    closeLibrary();
    const translations = I18N[currentLang] || I18N['en'];
    showToast(translations.toast_library_applied, 'success');
  }

  // 랜덤 셔플 - 1800개 중 무작위 1개 즉시 적용
  function shuffleRandomStyle() {
    if (allPrompts.length === 0) {
      const translations = I18N[currentLang] || I18N['en'];
      showToast(translations.toast_library_loading, 'error');
      return;
    }

    let targetPrompts = allPrompts;

    if (detectedImageType === 'animal' || detectedImageType === 'object') {
      const filtered = allPrompts.filter(p => {
        const tags = p.tags || [];
        return tags.some(t => ['illustration', 'sticker', 'character', 'other', 'poster'].includes(t.toLowerCase()));
      });
      if (filtered.length > 0) {
        targetPrompts = filtered;
      }
    } else {
      const filtered = allPrompts.filter(p => {
        const tags = p.tags || [];
        return tags.some(t => ['portrait', 'photo', 'cosplay', 'character'].includes(t.toLowerCase()));
      });
      if (filtered.length > 0) {
        targetPrompts = filtered;
      }
    }

    const rnd = targetPrompts[Math.floor(Math.random() * targetPrompts.length)];
    applyReactorStyleDirect(rnd);
  }

  function applyReactorStyleDirect(post) {
    if (customPrompt) {
      let promptText = (post.prompt || '').substring(0, 200);
      let currentGender = genderSelect ? genderSelect.value : 'random';
      if (currentGender === 'random') {
        currentGender = Math.random() < 0.5 ? 'male' : 'female';
        if (genderSelect) {
          genderSelect.value = currentGender;
        }
      }
      promptText = adaptPromptGender(promptText, currentGender);
      customPrompt.value = promptText;
      updateCharCount();
    }
    const primaryTag = (post.tags && post.tags[0]) || 'other';
    const tuning = categoryTuning[primaryTag] || categoryTuning.other;
    if (sliderWeight) { sliderWeight.value = tuning.weight; sliderWeightVal.textContent = tuning.weight; }
    if (sliderCloseness) { sliderCloseness.value = tuning.closeness; sliderClosenessVal.textContent = `${tuning.closeness}%`; }
    if (sliderDetail) { sliderDetail.value = tuning.detail; sliderDetailVal.textContent = `${tuning.detail}%`; }
    presetItems.forEach(p => p.classList.remove('active'));
    activeStyle = 'custom';
    const translations = I18N[currentLang] || I18N['en'];
    const translatedTags = (post.tags || ['other']).map(t => {
      const key = 'category_' + t.toLowerCase();
      return translations[key] || t;
    });
    showToast(translations.toast_shuffle_applied.replace('{tags}', translatedTags.join(', ')), 'success');
  }

  // ========================
  // 기존 내장 DB (Fallback)
  // ========================
  const stylePresetsDatabase = [
    { id: 'studio_classic', title: '시네마틱 스튜디오', category: 'portrait',
      prompt: 'Professional corporate headshot, 8k resolution, photorealistic, cinematic lighting, portrait photography, detailed skin texture, crisp focus, neutral studio background',
      bg: 'linear-gradient(135deg, #1f2937, #111827)' },
    { id: 'neon_noir', title: '네온 느와르', category: 'portrait',
      prompt: 'Moody cinematic portrait, high contrast dark atmosphere, subtle neon red ambient lighting, realistic, detailed reflections',
      bg: 'linear-gradient(135deg, #4c1d95, #111827)' },
    { id: 'anime_ghibli', title: '지브리 감성', category: 'illustration',
      prompt: 'Anime character portrait, Studio Ghibli aesthetic, hand-drawn digital illustration, soft pastel colors, whimsical mood',
      bg: 'linear-gradient(135deg, #10b981, #065f46)' },
    { id: 'cyberpunk_classic', title: '네온 디스토피아', category: 'cosplay',
      prompt: 'Futuristic cyberpunk portrait, neon magenta and cyan highlights, glowing cybernetic visor, highly detailed, octane render, techwear aesthetic',
      bg: 'linear-gradient(135deg, #ec4899, #06b6d4)' },
    { id: 'oil_painting', title: '고전 유화', category: 'illustration',
      prompt: 'Classical oil painting portrait, Rembrandt lighting style, textured thick brush strokes, fine art museum aesthetic, dramatic shadows',
      bg: 'linear-gradient(135deg, #78350f, #1e1b4b)' },
  ];

  // 사이드바 탭 이벤트 재바인딩 (카테고리 변수 activeLibCategory 사용)
  sidebarTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      sidebarTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      activeLibCategory = tab.dataset.category;
      filterLibrary();
    });
  });

  // 랜덤 셔플 버튼 바인딩
  const shuffleBtn = document.getElementById('shuffle-prompt-btn');
  if (shuffleBtn) shuffleBtn.addEventListener('click', shuffleRandomStyle);

  // ========================
  // MINI-GAME ENGINE SET
  // ========================

  function initMinigames() {
    const tabMemory = document.getElementById('tab-memory');
    const tabTictactoe = document.getElementById('tab-tictactoe');
    const gameMemoryContainer = document.getElementById('game-memory-container');
    const gameTictactoeContainer = document.getElementById('game-tictactoe-container');
    const minigameRestart = document.getElementById('minigame-restart');
    const tttRestart = document.getElementById('ttt-restart');

    if (tabMemory && tabTictactoe && gameMemoryContainer && gameTictactoeContainer) {
      tabMemory.addEventListener('click', () => {
        tabMemory.classList.add('active');
        tabTictactoe.classList.remove('active');
        gameMemoryContainer.classList.remove('hidden');
        gameTictactoeContainer.classList.add('hidden');
      });

      tabTictactoe.addEventListener('click', () => {
        tabMemory.classList.remove('active');
        tabTictactoe.classList.add('active');
        gameMemoryContainer.classList.add('hidden');
        gameTictactoeContainer.classList.remove('hidden');
      });
    }

    if (minigameRestart) {
      minigameRestart.addEventListener('click', () => resetMemoryGame());
    }
    if (tttRestart) {
      tttRestart.addEventListener('click', () => resetTttGame());
    }
  }

  function startMinigames() {
    const minigameWrapper = document.getElementById('minigame-wrapper');
    if (minigameWrapper) {
      minigameWrapper.classList.remove('hidden');
    }
    resetMemoryGame();
    resetTttGame();
  }

  function stopMinigames() {
    const minigameWrapper = document.getElementById('minigame-wrapper');
    if (minigameWrapper) {
      minigameWrapper.classList.add('hidden');
    }
    if (memoryTimerInterval) {
      clearInterval(memoryTimerInterval);
      memoryTimerInterval = null;
    }
  }

  // --- Game 1: Memory Match ---
  function resetMemoryGame() {
    const grid = document.getElementById('minigame-grid');
    const movesText = document.getElementById('minigame-moves');
    const timerText = document.getElementById('minigame-timer');

    if (!grid) return;

    if (memoryTimerInterval) clearInterval(memoryTimerInterval);
    memoryTimerInterval = null;
    memoryTime = 0;
    memoryMoves = 0;
    firstFlippedCard = null;
    secondFlippedCard = null;
    memoryMatchedCount = 0;
    isCheckingMatch = false;

    if (movesText) movesText.textContent = '0 moves';
    if (timerText) timerText.textContent = '0:00';

    const emojis = ['🎨', '📷', '💻', '🧠', '🎮', '🚀', '⚡', '🔮'];
    const cards = [...emojis, ...emojis];
    
    for (let i = cards.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [cards[i], cards[j]] = [cards[j], cards[i]];
    }

    grid.innerHTML = '';
    cards.forEach((emoji, index) => {
      const cardEl = document.createElement('div');
      cardEl.className = 'card';
      cardEl.dataset.index = index;
      cardEl.dataset.value = emoji;
      cardEl.addEventListener('click', () => handleCardClick(cardEl));
      grid.appendChild(cardEl);
    });

    memoryTimerInterval = setInterval(() => {
      memoryTime++;
      const mins = Math.floor(memoryTime / 60);
      const secs = String(memoryTime % 60).padStart(2, '0');
      if (timerText) timerText.textContent = `${mins}:${secs}`;
    }, 1000);
  }

  function handleCardClick(cardEl) {
    if (isCheckingMatch) return;
    if (cardEl.classList.contains('revealed') || cardEl.classList.contains('matched')) return;

    cardEl.classList.add('revealed');
    cardEl.textContent = cardEl.dataset.value;

    if (!firstFlippedCard) {
      firstFlippedCard = cardEl;
    } else {
      secondFlippedCard = cardEl;
      checkMemoryMatch();
    }
  }

  function checkMemoryMatch() {
    isCheckingMatch = true;
    memoryMoves++;
    
    const movesText = document.getElementById('minigame-moves');
    const translations = I18N[currentLang] || I18N['en'];
    if (movesText) {
      movesText.textContent = translations.moves_count.replace('{moves}', memoryMoves);
    }

    const val1 = firstFlippedCard.dataset.value;
    const val2 = secondFlippedCard.dataset.value;

    if (val1 === val2) {
      setTimeout(() => {
        firstFlippedCard.classList.remove('revealed');
        firstFlippedCard.classList.add('matched');
        secondFlippedCard.classList.remove('revealed');
        secondFlippedCard.classList.add('matched');

        firstFlippedCard = null;
        secondFlippedCard = null;
        isCheckingMatch = false;

        memoryMatchedCount += 2;
        if (memoryMatchedCount === 16) {
          clearInterval(memoryTimerInterval);
          const translations = I18N[currentLang] || I18N['en'];
          const congratsMsg = translations.app_title === "PersonaFit Studio" ? `🎉 Congratulations! Memory Match Win! (Moves: ${memoryMoves})` : translations.game_memory_title;
          // Format congrats
          let formatCongrats = `🎉 Congratulations! Memory Match Win! (Moves: ${memoryMoves})`;
          if (currentLang === 'ko') formatCongrats = `🎉 축하합니다! Memory Match 성공! (이동 횟수: ${memoryMoves}회)`;
          else if (currentLang === 'es') formatCongrats = `🎉 ¡Felicitaciones! ¡Ganaste en Memory Match! (Movimientos: ${memoryMoves})`;
          else if (currentLang === 'zh') formatCongrats = `🎉 恭喜！记忆匹配成功！ (步数: ${memoryMoves} 步)`;
          else if (currentLang === 'ja') formatCongrats = `🎉 おめでとうございます！神経衰弱クリア！ (移動数: ${memoryMoves}回)`;
          
          showToast(formatCongrats, 'success');
        }
      }, 300);
    } else {
      setTimeout(() => {
        firstFlippedCard.classList.remove('revealed');
        firstFlippedCard.textContent = '';
        secondFlippedCard.classList.remove('revealed');
        secondFlippedCard.textContent = '';

        firstFlippedCard = null;
        secondFlippedCard = null;
        isCheckingMatch = false;
      }, 800);
    }
  }

  // --- Game 2: Tic-Tac-Toe ---
  function resetTttGame() {
    const grid = document.getElementById('ttt-grid');
    const statusText = document.getElementById('ttt-status');

    if (!grid) return;

    tttBoard = Array(9).fill('');
    tttActive = true;
    isAiThinking = false;

    if (statusText) statusText.textContent = 'Your turn (X)';

    grid.innerHTML = '';
    for (let i = 0; i < 9; i++) {
      const cellEl = document.createElement('div');
      cellEl.className = 'ttt-cell';
      cellEl.dataset.index = i;
      cellEl.addEventListener('click', () => handleTttClick(cellEl, i));
      grid.appendChild(cellEl);
    }
  }

  function handleTttClick(cellEl, index) {
    if (!tttActive || isAiThinking || tttBoard[index] !== '') return;

    tttBoard[index] = 'X';
    cellEl.textContent = 'X';
    cellEl.classList.add('taken', 'x-player');

    const translations = I18N[currentLang] || I18N['en'];

    if (checkTttWinner('X')) {
      tttActive = false;
      updateTttStatusMessage();
      showToast(translations.game_ttt_status_win, 'success');
      return;
    }

    if (tttBoard.every(cell => cell !== '')) {
      tttActive = false;
      updateTttStatusMessage();
      return;
    }

    isAiThinking = true;
    updateTttStatusMessage();

    setTimeout(() => {
      if (!tttActive) return;
      makeAiMove();
      isAiThinking = false;
    }, 450);
  }

  function makeAiMove() {
    let aiIndex = findWinningMove('O');
    if (aiIndex === -1) {
      aiIndex = findWinningMove('X');
    }
    if (aiIndex === -1 && tttBoard[4] === '') {
      aiIndex = 4;
    }
    if (aiIndex === -1) {
      const emptyIndices = tttBoard.map((val, idx) => val === '' ? idx : null).filter(val => val !== null);
      if (emptyIndices.length > 0) {
        aiIndex = emptyIndices[Math.floor(Math.random() * emptyIndices.length)];
      }
    }

    if (aiIndex !== -1) {
      tttBoard[aiIndex] = 'O';
      const grid = document.getElementById('ttt-grid');
      if (grid) {
        const cellEl = grid.children[aiIndex];
        if (cellEl) {
          cellEl.textContent = 'O';
          cellEl.classList.add('taken', 'o-ai');
        }
      }

      if (checkTttWinner('O')) {
        tttActive = false;
        updateTttStatusMessage();
        return;
      }

      if (tttBoard.every(cell => cell !== '')) {
        tttActive = false;
        updateTttStatusMessage();
        return;
      }
    }

    updateTttStatusMessage();
  }

  function findWinningMove(player) {
    const winningCombos = [
      [0, 1, 2], [3, 4, 5], [6, 7, 8],
      [0, 3, 6], [1, 4, 7], [2, 5, 8],
      [0, 4, 8], [2, 4, 6]
    ];

    for (let combo of winningCombos) {
      const count = combo.filter(idx => tttBoard[idx] === player).length;
      const empty = combo.filter(idx => tttBoard[idx] === '').length;
      if (count === 2 && empty === 1) {
        return combo.find(idx => tttBoard[idx] === '');
      }
    }
    return -1;
  }

  function checkTttWinner(player) {
    const winningCombos = [
      [0, 1, 2], [3, 4, 5], [6, 7, 8],
      [0, 3, 6], [1, 4, 7], [2, 5, 8],
      [0, 4, 8], [2, 4, 6]
    ];

    return winningCombos.some(combo => {
      return combo.every(idx => tttBoard[idx] === player);
    });
  }

  function adaptPromptGender(prompt, targetGender) {
    if (!prompt || (targetGender !== 'male' && targetGender !== 'female')) return prompt;

    const femaleToMale = [
      { f: 'woman', m: 'man' },
      { f: 'women', m: 'men' },
      { f: 'girl', m: 'boy' },
      { f: 'girls', m: 'boys' },
      { f: 'female', m: 'male' },
      { f: 'lady', m: 'gentleman' },
      { f: 'ladies', m: 'gentlemen' },
      { f: 'goddess', m: 'god' },
      { f: 'herself', m: 'himself' },
      { f: 'she', m: 'he' },
      { f: 'her', m: 'his' },
      { f: 'dress', m: 'suit' },
      { f: 'skirt', m: 'pants' },
      { f: 'makeup', m: 'grooming' },
      { f: 'blouse', m: 'shirt' }
    ];

    const maleToFemale = [
      { m: 'man', f: 'woman' },
      { m: 'men', f: 'women' },
      { m: 'boy', f: 'girl' },
      { m: 'boys', f: 'girls' },
      { m: 'male', f: 'female' },
      { m: 'gentleman', f: 'lady' },
      { m: 'gentlemen', f: 'ladies' },
      { m: 'guy', f: 'girl' },
      { m: 'guys', f: 'girls' },
      { m: 'god', f: 'goddess' },
      { m: 'himself', f: 'herself' },
      { m: 'he', f: 'she' },
      { m: 'his', f: 'her' },
      { m: 'suit', f: 'dress' },
      { m: 'pants', f: 'skirt' },
      { m: 'grooming', f: 'makeup' },
      { m: 'shirt', f: 'blouse' }
    ];

    let result = prompt;

    function replaceWord(text, fromWord, toWord) {
      const patterns = [
        { regex: new RegExp('\\b' + fromWord + '\\b', 'g'), replacement: toWord },
        { regex: new RegExp('\\b' + fromWord.charAt(0).toUpperCase() + fromWord.slice(1) + '\\b', 'g'), 
          replacement: toWord.charAt(0).toUpperCase() + toWord.slice(1) },
        { regex: new RegExp('\\b' + fromWord.toUpperCase() + '\\b', 'g'), replacement: toWord.toUpperCase() }
      ];
      
      let temp = text;
      patterns.forEach(p => {
        temp = temp.replace(p.regex, p.replacement);
      });
      return temp;
    }

    if (targetGender === 'male') {
      femaleToMale.forEach(pair => {
        result = replaceWord(result, pair.f, pair.m);
      });
    } else if (targetGender === 'female') {
      maleToFemale.forEach(pair => {
        result = replaceWord(result, pair.m, pair.f);
      });
    }

    return result;
  }

  function cropImageToFace(base64Src, bbox, callback) {
    if (!bbox || bbox.length !== 4) {
      callback(base64Src);
      return;
    }

    const img = new Image();
    img.src = base64Src;
    img.onload = () => {
      const width = img.naturalWidth;
      const height = img.naturalHeight;

      const ymin = (bbox[0] / 100) * height;
      const xmin = (bbox[1] / 100) * width;
      const ymax = (bbox[2] / 100) * height;
      const xmax = (bbox[3] / 100) * width;

      const fW = xmax - xmin;
      const fH = ymax - ymin;
      const fSize = Math.max(fW, fH);
      const centerX = xmin + fW / 2;
      const centerY = ymin + fH / 2;

      // Zoom focus box (1.7x face size)
      let cropSize = fSize * 1.7;
      const maxPossibleSize = Math.min(width, height);
      if (cropSize > maxPossibleSize) {
        cropSize = maxPossibleSize;
      }

      let cropX = centerX - cropSize / 2;
      let cropY = centerY - cropSize / 2;

      if (cropX < 0) {
        cropX = 0;
      } else if (cropX + cropSize > width) {
        cropX = width - cropSize;
      }

      if (cropY < 0) {
        cropY = 0;
      } else if (cropY + cropSize > height) {
        cropY = height - cropSize;
      }

      const canvas = document.createElement('canvas');
      canvas.width = 600;
      canvas.height = 600;
      const ctx = canvas.getContext('2d');

      ctx.drawImage(
        img,
        Math.floor(cropX), Math.floor(cropY), Math.floor(cropSize), Math.floor(cropSize),
        0, 0, 600, 600
      );

      try {
        const croppedSrc = canvas.toDataURL('image/png');
        callback(croppedSrc);
      } catch (err) {
        console.warn('Canvas crop failed, fallback to original', err);
        callback(base64Src);
      }
    };

    img.onerror = () => {
      callback(base64Src);
    };
  }

  function applyLanguage(lang) {
    currentLang = lang;
    localStorage.setItem('personafit_lang', lang);
    const langSelect = document.getElementById('lang-select');
    if (langSelect) langSelect.value = lang;
    
    const translations = I18N[lang] || I18N['en'];
    
    // 1. Translate elements with data-i18n
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      if (translations[key]) {
        el.textContent = translations[key];
      }
    });
    
    // 2. Translate placeholders
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
      const key = el.getAttribute('data-i18n-placeholder');
      if (translations[key]) el.setAttribute('placeholder', translations[key]);
    });
    
    // 3. Translate titles
    document.querySelectorAll('[data-i18n-title]').forEach(el => {
      const key = el.getAttribute('data-i18n-title');
      if (translations[key]) el.setAttribute('title', translations[key]);
    });
    
    // 4. Translate tooltips
    document.querySelectorAll('.info-badge').forEach(el => {
      const key = el.getAttribute('data-i18n-tooltip');
      if (translations[key]) el.setAttribute('data-tooltip', translations[key]);
    });
    
    updateTodayStyleDisplay();
    updateSnsCropDescription();
    updateConnectionStatusUI();
    updateTttStatusMessage();
    updateLibraryCount();
    renderGallery();
  }
  
  function updateSnsCropDescription() {
    if (!snsPresetSelect) return;
    const val = snsPresetSelect.value;
    const preset = snsPresets[val];
    const translations = I18N[currentLang] || I18N['en'];
    if (snsCropInfo && preset) {
      if (val === 'original') {
        snsCropInfo.innerHTML = translations.sns_crop_info_template.replace('{name}', translations.sns_opt_original);
      } else {
        const option = snsPresetSelect.querySelector(`option[value="${val}"]`);
        const name = option ? option.textContent : preset.name;
        snsCropInfo.innerHTML = translations.sns_crop_info_pad
          .replace('{name}', name)
          .replace('{w}', preset.w)
          .replace('{h}', preset.h)
          .replace('{aspect}', preset.aspect);
      }
    }
  }
  
  function updateConnectionStatusUI() {
    const translations = I18N[currentLang] || I18N['en'];
    if (isCodexConnected) {
      if (codexStatusBadge) {
        codexStatusBadge.className = 'status-badge connected';
        codexStatusBadge.textContent = translations.codex_connected;
      }
      if (generateBtn) {
        const btnText = generateBtn.querySelector('span');
        if (btnText) btnText.textContent = translations.render_btn_codex;
      }
      const lbl = document.getElementById('connect-btn-label');
      if (lbl) lbl.textContent = translations.reconnect;
    } else {
      if (codexStatusBadge) {
        codexStatusBadge.className = 'status-badge disconnected';
        codexStatusBadge.textContent = translations.codex_offline;
      }
      if (generateBtn) {
        const btnText = generateBtn.querySelector('span');
        if (btnText) btnText.textContent = translations.render_btn_mock;
      }
      const lbl = document.getElementById('connect-btn-label');
      if (lbl) lbl.textContent = translations.login;
    }
  }
  
  function updateTttStatusMessage() {
    const statusText = document.getElementById('ttt-status');
    if (!statusText) return;
    const translations = I18N[currentLang] || I18N['en'];
    if (!tttActive) {
      if (checkTttWinner('X')) statusText.textContent = translations.game_ttt_status_win;
      else if (checkTttWinner('O')) statusText.textContent = translations.game_ttt_status_lose;
      else if (tttBoard.every(cell => cell !== '')) statusText.textContent = translations.game_ttt_status_draw;
    } else {
      statusText.textContent = isAiThinking ? translations.game_ttt_status_ai : translations.game_ttt_status_your;
    }
  }

});
