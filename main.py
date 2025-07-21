from fastapi import FastAPI, Request
from platzi_bot import handle_message
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    await handle_message(data)
    return {"status": "ok"}
