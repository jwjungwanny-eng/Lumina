# Lumina
다른 언어의 사용자가 이해하기 어려운 문서나 글의 내용의 핵심을 추출하는 프로젝트임다
# AI 다국어 문서 분석 및 번역 시스템 

Google Gemini API의 강력한 멀티모달(Multimodal) 기능을 활용하여 이미지 및 텍스트 문서를 분석하고, 다국어로 번역하며, 핵심 내용을 스마트하게 추출해 주는 웹 애플리케이션입니다.

## 🚀 주요 기능

* **다양한 파일 형식 지원:** 일반 텍스트 문서뿐만 아니라 이미지 파일 내의 텍스트와 맥락까지 분석 가능 (.txt, .pdf, 이미지 파일)
* **6개국 다국어 번역:** 한국어, 영어, 일본어, 중국어, 베트남어, 태국어 지원
* **AI 심층 분석:** 
  * 전체 내용에 대한 문맥 맞춤형 번역
  * 문서의 핵심 주제 1줄 요약
  * 문서 내 주요 정보 및 해야 할 일(To-do) 자동 추출
* **음성 지원 기능:** 번역된 텍스트를 해당 언어의 네이티브 음성(TTS)으로 읽어주는 기능 (확장 예정)

## 🛠 기술 스택

* **Frontend:** HTML5, CSS3, Vanilla JavaScript
* **Backend:** Python, FastAPI, Uvicorn
* **AI Model:** Google Gemini 1.5 Flash API
* **Development Environment:** GitHub Codespaces

## 📂 프로젝트 구조

```text
├── frontend/
│   └── index.html           # 프론트엔드 UI 및 API 호출 로직
├── backend/
│   ├── main.py              # FastAPI 서버 및 Gemini 연동 로직
│   ├── requirements.txt     # 파이썬 의존성 패키지 목록
│   └── .env.example         # 환경 변수 템플릿
├── .gitignore               # 보안 및 캐시 파일 업로드 방지
└── README.md                # 프로젝트 설명 문서