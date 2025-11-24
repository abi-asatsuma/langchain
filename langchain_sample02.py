import os
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

llm = ChatOllama(model="llama3", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", "あなたは簡潔に答えるアシスタントです。"),
    ("user", "{question}")
])

chat_histories = {}
def get_history(session_id: str):
    return chat_histories.setdefault(session_id, InMemoryChatMessageHistory())

runnable = prompt | llm
chain = RunnableWithMessageHistory(
    runnable,
    get_history,
    input_messages_key="question",
    history_messages_key="chat_history",
)
if __name__ == "__main__":
    result = chain.invoke(
        {"question": "LangChainって何ですか？"},
        config={"configurable": {"session_id": "default"}},
    )
    print(result.content)
    result2 = chain.invoke(
        {"question": "もう少し詳しく教えてください。"},
        config={"configurable": {"session_id": "default"}},
    )
    print(result2.content)
