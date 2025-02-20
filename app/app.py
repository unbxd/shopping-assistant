import uvicorn
from fastapi import FastAPI, Query
from pydantic import BaseModel

from chat import chat

app = FastAPI()

class ChatInput(BaseModel):
    text: str
    convo_id: str



@app.post("/v1.0/verticals/{vertical}/recommend/chat")
async def active_experiments(vertical: str, chat_input: ChatInput, uid: str = Query(..., description="User ID for tracking")):
    experiment_list = chat(vertical, uid, chat_input.text)
    return experiment_list


if __name__ == "__main__":
    uvicorn.run("app:app", port=8000, reload=True)