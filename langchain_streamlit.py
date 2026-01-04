import streamlit as st
from langchainapp.langchain_sample04 import app

st.title("天気＆コーディネートAI")

user_input = st.chat_input("質問を入力してください（例: 今日の東京の気温は？）")

if user_input:
    result = app.invoke(
        {"messages": [{"role": "user", "content": user_input}]},
        {"configurable": {"thread_id": "streamlit-thread"}}
    )
    messages = result["messages"]
    # 履歴をすべて表示
    for msg in messages:
        cls = msg.__class__.__name__
        if cls == "HumanMessage":
            st.markdown(f"**あなた:** {msg.content}")
        elif cls == "AIMessage":
            st.markdown(f"**AI:** {msg.content}")
