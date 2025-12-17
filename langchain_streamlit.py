import streamlit as st
from langchain_sample04 import app  # 既存のappをインポート

st.title("天気＆コーディネートAI")

user_input = st.text_input("質問を入力してください（例: 今日の東京の気温は？）")

if st.button("送信") and user_input:
    result = app.invoke(
        {"messages": [{"role": "user", "content": user_input}]},
        {"configurable": {"thread_id": "1"}}
    )
    st.write(result["messages"][-1].content)
