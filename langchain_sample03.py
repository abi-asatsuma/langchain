from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

search_tool = TavilySearchResults(max_results=3)

agent = create_agent(
    model=ChatOpenAI(model="gpt-4o-mini"),
    tools=[search_tool],
    system_prompt="最新情報をWeb検索して回答してください。"
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "最新のAIニュースは？"}]
})
