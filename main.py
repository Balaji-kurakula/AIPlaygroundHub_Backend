from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import google.generativeai as genai
from typing import Optional
import tempfile
import shutil
from datetime import timedelta

# Import your services - ADD THE MISSING IMPORT HERE
from app.services.auth import AuthService, authenticate_user, get_user, create_access_token  # <-- ADD create_access_token here
from app.services.conversation import ConversationService
from app.services.image import ImageService
from app.services.document import DocumentService
from app.services.auth import AuthService, authenticate_user, get_user, create_access_token
from app.services.auth import AuthService, authenticate_user, get_user, create_access_token, verify_token


load_dotenv()

app = FastAPI(title="AI Playground API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"  # Remove this in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Configure Gemini client
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Services
auth_service = AuthService()
conversation_service = ConversationService(genai)  # Pass genai module
image_service = ImageService(genai)
document_service = DocumentService(genai)

# Models
class LoginRequest(BaseModel):
    username: str
    password: str

class User(BaseModel):
    username: str
    name: str

# Authentication endpoint
@app.post("/auth/login")
async def login(request: LoginRequest):
    if request.username == "demo" and request.password == "demo123":
        token = create_access_token({"sub": request.username})
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {"username": "demo", "name": "Demo User"}
        }
    raise HTTPException(status_code=401, detail="Invalid credentials")

# Protected route dependency
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return verify_token(credentials.credentials)

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Conversation Analysis
@app.post("/conversation/analyze")
async def analyze_conversation(
    audio: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            shutil.copyfileobj(audio.file, tmp_file)
            temp_path = tmp_file.name

        result = await conversation_service.analyze_audio(temp_path)
        os.unlink(temp_path)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Image Analysis
@app.post("/image/analyze")
async def analyze_image(
    image: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            shutil.copyfileobj(image.file, tmp_file)
            temp_path = tmp_file.name

        result = await image_service.analyze_image(temp_path)
        os.unlink(temp_path)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Document Summarization
@app.post("/document/summarize")
async def summarize_document(
    file: Optional[UploadFile] = File(None),
    url: Optional[str] = Form(None),
    current_user: dict = Depends(get_current_user)
):
    try:
        if file:
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                shutil.copyfileobj(file.file, tmp_file)
                temp_path = tmp_file.name
            
            result = await document_service.summarize_file(temp_path, file.filename)
            os.unlink(temp_path)
        elif url:
            result = await document_service.summarize_url(url)
        else:
            raise HTTPException(status_code=400, detail="Either file or URL must be provided")
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
