from fastapi import FastAPI, Request
from pydantic import BaseModel
from langchainapp.langchain_sample04 import app

api = FastAPI()

class Query(BaseModel):
    message: str

@api.post("/chat")
def chat(query: Query):
    result = app.invoke(
        {"messages": [{"role": "user", "content": query.message}]},
        {"configurable": {"thread_id": "session1"}}
    )
    return {"response": result["messages"][-1].content}
