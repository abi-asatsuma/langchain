from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
import requests
import os

@tool
def get_weather(city: str) -> str:
    """指定した都市の現在の天気と気温を取得します（OpenWeather API使用）。"""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
      return "OPENWEATHER_API_KEY が設定されていません。"
    
    city_map = {
        "東京": "Tokyo,JP",
        "大阪": "Osaka,JP",
        "名古屋": "Nagoya,JP",
        "札幌": "Sapporo,JP",
        "福岡": "Fukuoka,JP",
    }
    q = city_map.get(city, city)

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": q,
        "appid": api_key,
        "units": "metric",
        "lang": "ja",
    }
    resp = requests.get(url, params=params, timeout=10)
    if resp.status_code != 200:
        return f"OpenWeather APIエラー: {resp.status_code} {resp.text[:200]}"

    data = resp.json()
    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]
    humidity = data["main"]["humidity"]
    return f"{city}の現在の天気: {desc}、気温: {temp}℃、湿度: {humidity}%"

tools = [get_weather]

# モデル
model = ChatOllama(model="gpt-oss:20b", temperature=0)
model_with_tools = model.bind_tools(tools)

checkpointer = InMemorySaver()

def agent_node(state: MessagesState):
    system_msg = SystemMessage(content="""日本語で簡潔に答えてください。
- 現在の天気・気温: get_weather ツールを使用してください。""")
    
    messages = [system_msg] + state["messages"]
    response = model_with_tools.invoke(messages)
    
    if response.tool_calls:
        return {"messages": [response]}
    return {"messages": [response], "__end__": True}

# グラフ（同じ）
builder = StateGraph(MessagesState)
builder.add_node("agent", agent_node)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "agent")
builder.add_conditional_edges(
    "agent",
    lambda state: "tools" if state["messages"][-1].tool_calls else END,
    {"tools": "tools", END: END}
)
builder.add_edge("tools", "agent")
app = builder.compile(checkpointer=checkpointer)

# デモ
# print("=== 1回目: 天気検索 ===")
# result1 = app.invoke(
#     {"messages": [{"role": "user", "content": "今日の東京の気温は？"}]},
#     {"configurable": {"thread_id": "1"}}
# )
# print("1回目:", result1["messages"][-1].content[:100] + "...")

# print("\n=== 2回目: コーディネート ===")
# result2 = app.invoke(
#     {"messages": [{"role": "user", "content": "今日はどんな服装したらいい？"}]},
#     {"configurable": {"thread_id": "1"}}
# )
# print("2回目:", result2["messages"][-1].content)
