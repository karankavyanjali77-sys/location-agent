import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from agent.agent import create_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
import asyncio

app = FastAPI()
session_service = InMemorySessionService()
agent = create_agent()
runner = Runner(agent=agent, session_service=session_service, app_name="zoo-guide")

class QueryRequest(BaseModel):
    message: str
    session_id: str = "default"

@app.post("/query")
async def query_agent(req: QueryRequest):
    from google.genai.types import Content, Part
    session = await session_service.get_session(
        app_name="zoo-guide", user_id="user", session_id=req.session_id
    )
    if not session:
        session = await session_service.create_session(
            app_name="zoo-guide", user_id="user", session_id=req.session_id
        )
    content = Content(role="user", parts=[Part(text=req.message)])
    result_text = ""
    async for event in runner.run_async(
        user_id="user", session_id=req.session_id, new_message=content
    ):
        if event.is_final_response() and event.content:
            result_text = event.content.parts[0].text
    return JSONResponse({"response": result_text})

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
