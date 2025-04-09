from fastapi import FastAPI, UploadFile, Form, Depends, HTTPException
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import uvicorn
import os

from rag_engine import ingest_document, query_rag
from auth import authenticate_user, create_access_token, get_current_user

app = FastAPI()

# CORS (for frontend JS to call APIs)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# ✅ Serve index.html at root URL
@app.get("/", response_class=HTMLResponse)
async def serve_home():
    return FileResponse("index.html")  # Or change path if it's in another folder

# 🔐 Token login
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token({"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}

# 📄 Upload PDF
@app.post("/upload")
async def upload_file(file: UploadFile, token: str = Depends(oauth2_scheme)):
    content = await file.read()
    result = ingest_document(content)
    return JSONResponse(content={"message": result})

# 💬 Ask a question
@app.post("/query")
async def ask_question(query: str = Form(...), token: str = Depends(oauth2_scheme)):
    answer = query_rag(query)
    return JSONResponse(content={"answer": answer})

# 🔄 Only for local dev (Render doesn't run this)
if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
