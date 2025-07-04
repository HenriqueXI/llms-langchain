# client.py
from mcp.client.stdio import stdio_client, StdioServerParameters
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
import asyncio

async def main():
    server_params = StdioServerParameters(command="python", args=["mcp_server.py"])
    async with stdio_client(server_params) as (read, write):
        from mcp.client import ClientSession
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)

            llm = ChatOpenAI(model="gpt-4o", temperature=0)
            agent = create_react_agent(llm, tools)

            resp = await agent.ainvoke({"messages":[("user","Quais imóveis estão disponíveis no Centro?")]})
            print(resp["messages"][-1].content)

if __name__=="__main__":
    asyncio.run(main())
