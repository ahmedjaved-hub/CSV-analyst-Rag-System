from fastapi import FastAPI,UploadFile,File,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from rag import build_csv_context
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
from google.genai import types
from fastapi.responses import StreamingResponse
import os
import uuid
import pandas as pd
import io

load_dotenv()

client = genai.Client()
sessions = {}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/Upload")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename or not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    contents = await file.read()
    try:
        df = pd.read_csv(io.BytesIO(contents))
        context = build_csv_context(df)
        print("Successfully built csv context")
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Failed to process CSV: {str(e)}")
    
    session_id = str(uuid.uuid4())
    sessions[session_id]= context
    print(f"saved context for session {session_id} {sessions}")

    return {"session_id": session_id,"message":"CSV uploaded and ready"}




class ChatRequest(BaseModel):
    session_id :str
    message:str


@app.post("/chat")
async def chat(request: ChatRequest):
    context = sessions.get(request.session_id)
    if not context:
        raise HTTPException(status_code=404, detail="Session not found Upload a csv")
    

    Prompt = f"""
    You are a CSV analysis assistant.
    Use the following context to answer the user's question.
    must be in paragraph form and explain the answer
    
    Context:
    {context}
    Answer questions about this data clearly and concisely
    cite specific numbers ,column names, or row values when relevant
    if the question cannot be answered then say it explicitly
    User Question:
    {request.message}
    """

    async def stream_response():
        stream = await client.aio.models.generate_content_stream(
            model="gemini-2.5-flash",
            contents = Prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=1024,
            )
        )   
        async for chunks in stream:
            if chunks.text:
                yield chunks.text
    
    
    return StreamingResponse(stream_response(),media_type="text/plain")