# main.py

from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
from langchain.agents import initialize_agent
from langchain_community.tools import TavilySearchResults

# ---------------------------------------------------
# 1. Load environment variables from .env
# ---------------------------------------------------
load_dotenv()

# Get Google API key from environment
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    raise ValueError("Google API Key not found. Please set it in .env as GOOGLE_API_KEY")

# Get Tavily API key from environment
tavily_api_key = os.getenv("TAVILY_API_KEY")
if not tavily_api_key:
    raise ValueError("Tavily API Key not found. Please set it in .env as TAVILY_API_KEY")

# ---------------------------------------------------
# 2. Create the LLM (Gemini model)
# ---------------------------------------------------
# LangChain wraps Google Generative AI into an LLM interface.
# Here we use the free-tier gemini-1.5-flash model.
llm = ChatGoogleGenerativeAI(
    model='gemini-1.5-flash',
    google_api_key=google_api_key
)

# ---------------------------------------------------
# 3. Create the Tavily Search Tool
# ---------------------------------------------------
# TavilySearchResults is a LangChain "Tool" that lets the agent
# fetch real-time information from the internet.
search_tool = TavilySearchResults(
    search_depth='basic',        # 'basic' = fewer results, 'advanced' = more results
    tavily_api_key=tavily_api_key
)

# ---------------------------------------------------
# 4. Put tools into a list
# ---------------------------------------------------
tools = [search_tool]

# ---------------------------------------------------
# 5. Initialize the Agent
# ---------------------------------------------------
# 'zero-shot-react-description' = The LLM decides which tools to use
# based only on the tool descriptions and your query (no examples given).
# verbose=True shows each step the agent takes.
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent='zero-shot-react-description',
    verbose=True
)

# ---------------------------------------------------
# 6. Run the Agent
# ---------------------------------------------------
# When you call agent.invoke(), LangChain will:
#   1. Pass your question to the LLM.
#   2. The LLM thinks about the problem ("thought" step).
#   3. If it decides it needs fresh info, it calls the Tavily tool.
#   4. Tavily returns search results.
#   5. LLM uses those results to craft the final answer.
#   6. LangChain prints the intermediate steps because verbose=True.
print("\n=== Asking the agent ===\n")
response = agent.invoke("who is more popular hania amir or alia bhatt")

print("\n=== Final Answer ===\n")
print(response)
