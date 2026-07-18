import os
import json
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from pydantic import BaseModel
import aiofiles
from dotenv import load_dotenv

# .env 파일에서 환경 변수를 안전하게 로드합니다.
load_dotenv()

# 구글 Gemini API 키 설정
GOOGLE_API_KEY = os.environ.get("GEMINI_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

app = FastAPI()

# 프론트엔드 접근 허용 (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalysisResult(BaseModel):
    topic: str
    translated_text: str
    extracted_info: str
    audio_url: str

@app.post("/analyze", response_model=AnalysisResult)
async def analyze_document(file: UploadFile = File(...), target_language: str = Form(...)):
    file_path = f"temp_{file.filename}"
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

    # Gemini 1.5 Flash 모델 사용 (멀티모달)
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    당신은 전문 문서 분석가입니다. 첨부된 파일(이미지 또는 문서)을 분석하여 다음 요청에 맞게 JSON 형식으로만 응답하세요.
    1. 'translated_text': 문서의 모든 내용을 {target_language} 언어로 문맥에 맞게 번역.
    2. 'extracted_info': 문서 내에서 가장 중요한 정보나 해야 할 일(To-do)을 추출하여 {target_language}로 작성 (없으면 '해당 없음').
    3. 'topic': 문서의 핵심 주제를 {target_language}로 1줄로 요약.
    
    응답 형식 (반드시 JSON 형식을 지킬 것):
    {{
        "topic": "주제 내용",
        "translated_text": "전체 번역 내용",
        "extracted_info": "중요 정보 요약"
    }}
    """

    try:
        uploaded_file_to_gemini = genai.upload_file(file_path)
        response = model.generate_content([uploaded_file_to_gemini, prompt])
        
        response_text = response.text.strip().replace("```json", "").replace("```", "")
        ai_data = json.loads(response_text)
        
        topic = ai_data.get("topic", "주제 추출 실패")
        translated_text = ai_data.get("translated_text", "번역 실패")
        extracted_info = ai_data.get("extracted_info", "해당 없음")
        
        genai.delete_file(uploaded_file_to_gemini.name)
        os.remove(file_path)

    except Exception as e:
        topic = "분석 오류"
        translated_text = f"Gemini API 호출 중 오류가 발생했습니다: {str(e)}"
        extracted_info = "오류 발생"
        if os.path.exists(file_path):
            os.remove(file_path)

    # 차후 구현될 음성 지원(TTS)을 위한 더미 URL입니다.
    audio_url = f"https://api.your-domain.com/audio/sample_tts.mp3"

    return AnalysisResult(
        topic=topic,
        translated_text=translated_text,
        extracted_info=extracted_info,
        audio_url=audio_url
    )