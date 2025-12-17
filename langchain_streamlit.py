import streamlit as st
from langchain_sample04 import app

st.title("天気＆コーディネートAI")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

user_input = st.chat_input("質問を入力してください（例: 今日の東京の気温は？）")

if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    result = app.invoke(
        {"messages": st.session_state["messages"]},
        {"configurable": {"thread_id": "streamlit-thread"}}
    )
    ai_content = result["messages"][-1].content
    st.session_state["messages"].append({"role": "assistant", "content": ai_content})
    # 入力欄をクリアするには rerun するしかないので、下記を追加
    st.rerun()

for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.markdown(f"**あなた:** {msg['content']}")
    else:
        st.markdown(f"**AI:** {msg['content']}")
