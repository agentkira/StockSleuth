from fastapi import FastAPI, Request, UploadFile, File
from pydantic import BaseModel
from rag_chain import get_rag_chain
from db import save_conversation, SessionLocal, Conversation
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag_chain = get_rag_chain()

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def query_rag(request: QueryRequest):
    result = rag_chain.invoke({"question": request.query})
    answer = result["result"]
    save_conversation(request.query, answer)
    return {"response": answer}

@app.get("/conversations")
async def list_conversations():
    db = SessionLocal()
    conversations = db.query(Conversation).all()
    return JSONResponse([{"query": c.query, "response": c.response} for c in conversations])

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    docs_dir = "docs/pdfs"
    os.makedirs(docs_dir, exist_ok=True)
    file_path = os.path.join(docs_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"status": "uploaded"}
