from fastapi import FastAPI, Request
from pydantic import BaseModel
from langchainapp.langchain_sample04 import app
import time

api = FastAPI()

class Query(BaseModel):
    message: str

def call_langchain_api(message: str, max_retries: int = 3, delay: float = 1.0):
    for attempt in range(max_retries):
        try:
            result = app.invoke(
                {"messages": [{"role": "user", "content": message}]},
                {"configurable": {"thread_id": "api-session"}}
            )
            return result["messages"][-1].content
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(delay)
            else:
                return f"Error: {str(e)}"

@api.post("/chat")
def chat(query: Query):
    responses = []
    for line in query.message.splitlines():
        if line.strip():
            response = call_langchain_api(line)
            responses.append(response)
    return {"responses": responses}
