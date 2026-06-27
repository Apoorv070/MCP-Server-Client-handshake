import os
import asyncio
from dotenv import load_dotenv

# 1. Load configuration profiles
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Import core LangChain elements
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.tools import load_mcp_tools
from mcp.client.sse import sse_client
from mcp import ClientSession

# Import your local agent tools module 
from agent_tools import (
    fetch_country_info,
    search_cheap_flights,
    search_specific_flights,
    find_hotels,
    get_coordinates,
    get_weather,
    get_driving_distance,
)

async def main():
    print("🤖 Initializing Gemini LLM Engine...")
    # Initialize your Chat model
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        api_key=GOOGLE_API_KEY,
    )
    
    # Pack your local helper functions into a list
    internal_tools = [
        fetch_country_info,
        search_cheap_flights,
        search_specific_flights,
        find_hotels,
        get_coordinates,
        get_weather,
        get_driving_distance,
    ]
    
    # Connect directly to your running MCP hotel backend server
    url = "http://localhost:8000/sse"
    print(f"🔌 Connecting to MCP Server on {url}...")
    
    try:
        async with sse_client(url) as (read, write):
            async with ClientSession(read, write) as session:
                # Execute protocol handshake
                await session.initialize()
                print("⚙️ Handshake complete. Fetching remote tools...")
                
                # Auto-wrap FastMCP server tools into standard LangChain tools
                mcp_tools = await load_mcp_tools(session)
                
                # Combine both native python tools and server tools seamlessly
                all_tools = internal_tools + mcp_tools
                
                print("\n==================================================")
                print(f"🎉 Success! Combined Agent Tools Available ({len(all_tools)} total):")
                print("==================================================")
                for index, tool in enumerate(all_tools, start=1):
                    print(f"{index}. Name: {tool.name}")
                    print(f"   Description: {tool.description.strip().splitlines()[0] if tool.description else 'No description'}\n")
                
                # Execute a test generation task 
                print("Testing LLM generation connectivity...")
                test_response = await llm.ainvoke("Say: System online and ready!")
                print(f"Model Response: {test_response.content}")
                
    except Exception as e:
        print(f"\n❌ Pipeline Connection Error: {e}")
        print("Please check that your terminal running 'mcp_hotel_server.py' is active.")

if __name__ == "__main__":
    # Run the isolated asyncio event loop natively without Jupyter notebook collisions
    asyncio.run(main())
