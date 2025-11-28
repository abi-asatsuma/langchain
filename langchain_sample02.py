from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, MessagesState, START
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage

# モデル初期化
model = ChatOllama(model="llama3:8b", temperature=0)

# チェックポインター（履歴保持用）
checkpointer = InMemorySaver()

# ノード定義
def call_model(state: MessagesState):
     # システムメッセージをモデル呼び出しの時だけ使用
    system_msg = SystemMessage(content="日本語で、履歴を考慮して簡潔に答えてください。")
    messages = [system_msg] + state["messages"]
    
    response = model.invoke(messages)
    # 状態に返すのはAIメッセージだけ
    return {"messages": [response]}


# グラフ構築
builder = StateGraph(MessagesState)
builder.add_node("call_model", call_model)
builder.add_edge(START, "call_model")

app = builder.compile(checkpointer=checkpointer)

# 1回目の呼び出し
result = app.invoke(
    {"messages": [{"role": "user", "content": "わたしの名前は新卒太郎です。"}]},
    {"configurable": {"thread_id": "1"}}
)
print([(msg.type, msg.content) for msg in result["messages"]])

# 2回目の呼び出し
result = app.invoke(
    {"messages": [{"role": "user", "content": "わたしの名前は何ですか？"}]},
    {"configurable": {"thread_id": "1"}}
)
print([(msg.type, msg.content) for msg in result["messages"]])
