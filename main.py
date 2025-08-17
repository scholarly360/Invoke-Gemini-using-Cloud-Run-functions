""" GCP FastAPI example with Google Gemini AI"""

import httpx, os, uuid
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from vellox import Vellox
from pydantic import BaseModel
from typing import Optional
from google import genai
from pathlib import Path


app = FastAPI()
_security = HTTPBearer(auto_error=False)
API_TOKEN = os.getenv("API_TOKEN", "") # set while deploying
client = genai.Client()
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")  # current Vertex default

class SummarizeTextRequest(BaseModel):
    text: Optional[str] = None

def require_token(creds: HTTPAuthorizationCredentials = Depends(_security)):
    if not creds or creds.scheme.lower() != "bearer" or creds.credentials != API_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing token")

""" Simple endpoint """
@app.get("/health", dependencies=[Depends(require_token)])
def health():
    return {"message": "Hello Running (Securely)!"}

""" Simple summarize as Markdown """
@app.post("/summarize", dependencies=[Depends(require_token)])
async def summarize(req: SummarizeTextRequest):
    if not req.text:
        raise HTTPException(400, "Provide 'text'.")
    source = req.text
    prompt = (""" Summarize the following clearly as markdown \n\n---\n""" + source)
    resp = client.models.generate_content(model=MODEL, contents=prompt, config={"temperature": 0.1})
    return {"summary": resp.text}


""" Wrap FastAPI (ASGI) so it looks like a Cloud Run function """
vellox = Vellox(app=app, lifespan="off")
""" This is your function entrypoint for GCP """
def handler(request):
    return vellox(request)