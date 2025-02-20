import uvicorn
from fastapi import FastAPI, Query, Request
from chat import chat

app = FastAPI()


@app.post("/v1.0/verticals/{vertical}/recommend/chat")
async def chat_endpoint(vertical, req: Request):
    uid = req.query_params.get('uid')
    request_data = await req.json()
    text = request_data.get('text', '')
    response = chat(vertical, uid, text)
    return response


if __name__ == "__main__":
    uvicorn.run("app:app", port=8000, reload=True)
