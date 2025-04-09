from fastapi import FastAPI, UploadFile, Form, Depends, HTTPException
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

from rag_engine import ingest_document, query_rag
from auth import authenticate_user, create_access_token, get_current_user

app = FastAPI()

# CORS middleware for frontend API calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static directory for HTML/CSS/JS
app.mount("/static", StaticFiles(directory="static"), name="static")

# OAuth2 setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Serve index.html at root
@app.get("/", response_class=HTMLResponse)
async def serve_home():
    return FileResponse("static/index.html")

# User login for token
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token({"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}

# Upload PDF
@app.post("/upload")
async def upload_file(file: UploadFile, token: str = Depends(oauth2_scheme)):
    content = await file.read()
    result = ingest_document(content)
    return JSONResponse(content={"message": result})

# Ask a question
@app.post("/query")
async def ask_question(query: str = Form(...), token: str = Depends(oauth2_scheme)):
    answer = query_rag(query)
    return JSONResponse(content={"answer": answer})

# Run only in local dev
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Use PORT from environment
    uvicorn.run("main:app", host="0.0.0.0", port=port)
