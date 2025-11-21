import os
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOllama(model="llama3", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", "あなたは簡潔に答えるアシスタントです。"),
    ("user", "{question}")
])

chain = prompt | llm

if __name__ == "__main__":
    result = chain.invoke({"question": "LangChainって何ですか？"})
    print(result.content)
