# PersonaFit Studio — Profile Art Direction

PersonaFit Studio는 사용자의 프로필 이미지를 아티스틱하고 다양한 스타일 프리셋(Corporate, Travel, Cinematic, Today's Trend)으로 변환해주는 프리미엄 웹 어플리케이션입니다.

Windows/Linux 환경 전반에서 이식성 있게 동작하며, OpenAI Codex API(Image 2.0 / DALL-E 3)와 Google Gemini API를 상호보완적으로 사용하여 강력한 이미지 생성 및 오케스트레이션을 제공합니다.

---

## 🌟 주요 기능 (Key Features)

1. **Art-Directed Profile Editor**:
   - **Corporate (증명사진)**, **Travel (여행지)**, **Cinematic (영화 포스터)** 프리셋 및 **오늘의 밈(Today's Style)** 제공
   - 사용자 자유 문구 입력을 지원하는 Custom Prompt 기능
2. **Detail Tuning Parameters**:
   - 프롬프트 강도(Prompt Weight), 원본 싱크율(Closeness to original), 선명도(Detailing strength) 슬라이더 미세 조정
3. **Smart Image Processing Pipeline**:
   - 업로드된 사진 속의 성별 자동 감지 및 젠더 중립성/다양성 기반 프롬프트 셔플 기능
   - 최고의 바스트-샷 구도를 잡기 위한 얼굴 중심 인공지능 줌-크롭(Face Zoom-Crop) 기능
4. **SNS Format Exporter**:
   - X, LinkedIn, Threads, Instagram 스토리 등 타겟 SNS 규격 맞춤형 이미지 리사이즈 및 블러 패딩 아웃풋 다운로드
5. **Interactive Loading Experience**:
   - 생성 대기 시간(30초~1분) 동안 사용자의 지루함을 방지하는 인블록 게임(Memory Match, Tic-Tac-Toe) 및 2초 주기 상태 프로세스 롤링 메시지 연출
6. **Privacy Shield**:
   - 업로드된 이미지는 분석 즉시 완전히 파기되며 서버에 보관되지 않는 로컬 퍼스트 안심 설계

---

## 📂 프로젝트 구조 (Project Structure)

```
avatar_preset_maker/
├── server.py                   # Python Threading HTTP 백엔드 서버
├── app.js                      # 프론트엔드 UI 오케스트레이션 및 상태 관리
├── index.html                  # 스위스 레이아웃 그리드 기반 웹 마크업
├── styles.css                  # Quiet Premium Neutral 톤앤매너 디자인 시스템
├── update_today_style.py       # 오늘의 Style SNS 밈 자동 갱신 및 썸네일 생성기
├── generate_thumbnails.py      # 스타일 라이브러리용 DALL-E 3 배치 생성기
├── generate_thumbnails_direct.py # 스타일 라이브러리용 Gemini/Imagen 배치 생성기
├── tests/
│   └── verify_ux_hurdles.py    # Playwright 기반 UX 및 대기 상태 E2E 테스트 스크립트
├── docs/
│   └── audit/                  # 작업 내역 및 감사 로그 보관 디렉터리 (26개 로그)
├── assets/                     # 기본 테마용 정적 리소스 및 프리셋 썸네일
└── today-style.json            # 갱신된 오늘의 밈 설정 데이터
```

---

## ⚙️ 설정 및 실행 방법 (Setup & Run Guide)

### 1. 필수 환경변수 설정
프로젝트를 실행하기 전에 아래 환경변수를 시스템 또는 `.env`에 설정하십시오.

```bash
# OpenAI API Key (BOM이 제거된 클린한 문자열 권장)
OPENAI_API_KEY=sk-proj-...

# Google Gemini API Key
GEMINI_API_KEY=AIzaSy...
```

### 2. 서버 실행
아래 명령어를 실행하여 웹 서버를 띄웁니다.

```bash
python server.py
```
- 서버 구동 포트: `http://localhost:8080` (기본값)

### 3. 오늘의 밈 자동 갱신
매일 최신 유행 트렌드 밈을 갱신하려면 아래 배치 명령어를 실행합니다. 스케줄러(cron)에 매일 자정 등록하여 운영할 수 있습니다.

```bash
python update_today_style.py
```

### 4. E2E 자동화 테스트 수행 (Playwright)
사용자 흐름 및 UX 안심 요소가 정상적으로 렌더링되고 작동하는지 검증합니다.

```bash
# playwright 라이브러리 설치 필요
pip install playwright
playwright install

# 테스트 실행
python tests/verify_ux_hurdles.py
```
- 실행 완료 시 `tests/screenshots/` 폴더 내에 UI 검증 캡처본이 자동 저장됩니다.
