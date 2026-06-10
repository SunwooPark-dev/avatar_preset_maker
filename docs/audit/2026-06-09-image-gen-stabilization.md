# Audit: Image Generation Stabilization

- Date: 2026-06-09
- Agent: Antigravity
- Mode: debug → execute → verify
- Task ID: e81c7c9e-39a7-48aa-b62e-27cb19ebdf8c

## Why
이미지 생성이 지속적으로 실패(Codex CLI 120초 timeout 발생)하여 원인 분석 및 안정화 필요.

## Scope
- `server.py` 내 `_run_generation_job` 함수 수정
- `test_gen.py` 진단 스크립트 수정 및 실행
- 서버 재시작 및 3축 검증

## Root Cause Analysis

### 실패 원인 (3가지)
1. **`-i source.png` 플래그 + isolated `tmp_dir` 조합**
   - Codex는 `exec -i <file>` 플래그로 이미지를 직접 attach하는 경우, isolated 디렉터리에서 bash 도구를 통한 파일 탐색 시 예상치 못한 경로 불일치 발생
   - 결과: 프로세스가 stdin 입력 대기로 hang → 120초 timeout

2. **`--disable hooks` 플래그들**
   - hooks를 비활성화하면 Codex가 bash shell tool을 실행 불가
   - 성공 사례(gen_ff71a99b6305)에서 hooks는 활성화 상태였음
   - 결과: Codex가 generated_images 폴더 탐색 및 파일 복사 불가

3. **격리된 tmp 디렉터리 사용**
   - 작업 디렉터리가 `tmp_{job_id}` 이면 Codex가 session 시작 시 workdir 표시가 달라짐
   - 성공 사례는 항상 메인 `work_dir`에서 실행됨

## Fix Applied

### server.py - `_run_generation_job` 재설계
| 항목 | 수정 전 | 수정 후 |
|---|---|---|
| CWD | `tmp_{job_id}` (격리된 임시 디렉터리) | `work_dir` (메인 디렉터리) |
| 이미지 참조 | `-i source.png` 플래그 | 프롬프트 텍스트에서 `source_{job_id}.png` 참조 |
| Hook 설정 | `--disable hooks` (3개) | 제거 (hooks 활성화) |
| reasoning | `model_reasoning_effort=low` 포함됨 | `model_reasoning_effort=low` 유지 |
| 임시 디렉터리 | 생성 후 삭제 (로그 손실) | 제거 (없음) |
| 로그 저장 | `tmp_dir` 내에서 삭제됨 | `work_dir/logs/` 에 영구 보존 |
| output 폴링 | session_id 기반 + 120초 | session_id 기반 + 직접 파일 감시 + 240초 |

## Files Changed
- `server.py`: `_run_generation_job` 함수 전면 재설계
- `logs/test_gen.py`: 동일 방식으로 업데이트 (진단 스크립트)

## Commands Run
| Command | Exit Code | Result |
|---|---|---|
| `python verify_test.py` | 0 | 3축 ALL PASSED (최적화/안정성/호환성) |
| `python test_gen.py` (구방식) | 1 | TimeoutExpired (120s) - FAILED |
| `python test_gen.py` (신방식) | 0 | output_test_direct.png 2048236 bytes - SUCCESS ✅ |

## Results
- **이미지 생성 성공 확인**: `output_test_direct.png` 생성 (2,048,236 bytes)
- **Codex 실행 시간**: ~100초 (세션 시작 → 이미지 생성 → bash 복사)
- **로그 영구 보존**: `work_dir/logs/gen_{job_id}_err.log`
- **3축 검증 통과**: 최적화(13.6초), 안정성(400/invalid 처리), 호환성(CLI path, JS syntax)

## Evidence
- `output_test_direct.png`: 생성된 아바타 이미지
- `logs/gen_test_direct_err.log`: 성공 실행 로그
- `gen_ff71a99b6305_err.log`: 기존 성공 사례 비교 기준

## Risks
- Codex 실행 시간이 60~120초 소요 → 사용자 대기 UX 고려 필요
- `work_dir`에서 직접 실행 시 동시 다중 요청이 겹칠 가능성 (현재 사용량 수준에서 허용 범위)
- generated_images 폴더 경로(`C:\Users\sunwo\.codex\generated_images`) 하드코딩 - 환경 변수화 권장

## Rollback
1. `server.py` 내 `_run_generation_job`을 이전 버전(--disable hooks, -i flag)으로 복원
2. 단, 이전 버전은 동작하지 않으므로 실질적 롤백 불필요

## Remaining TODO
- [ ] 동시 다중 생성 요청 테스트 (부하 테스트)
- [ ] `C:\Users\sunwo\.codex\generated_images` 경로 환경 변수화
- [ ] 생성 대기 UI에 진행률 표시 개선
