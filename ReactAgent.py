# main.py
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

# Get API key from environment variables
api_key = os.getenv("googleapi")

if not api_key:
    raise ValueError("Google API Key not found. Please set it in .env as GOOGLE_API_KEY")

# Create the LLM instance
llm = ChatGoogleGenerativeAI(
  model='gemini-1.5-flash',
    google_api_key=api_key  # Pass the API key explicitly
)

# Invoke the model
result = llm.invoke("GIVE ME DETAILS OF HANIA AMIR")

# Print the response content
print(result)
