from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

# ---------------------------------------------------
# 1. Load environment variables from .env
# ---------------------------------------------------
load_dotenv()

# ---------------------------------------------------
# 2. Setup Google Gemini as the LLM
# ---------------------------------------------------
google_api_key = os.getenv("googleapi")  # read API key from .env
llm = ChatGoogleGenerativeAI(
    model='gemini-1.5-flash',  # Fast + cheap model for testing
    google_api_key=google_api_key
)

# ---------------------------------------------------
# 3. Define a Pydantic schema for structured output
# ---------------------------------------------------
class Celebrity(BaseModel):
    """Information Regarding Celebrity"""
    name: str = Field(description='Name of the celeb')
    country: str = Field(description="Country of the celeb")   # use lowercase to follow Pydantic style
    insta_followers: int = Field(description='Insta Followers of the celeb')

# ---------------------------------------------------
# 4. Wrap the LLM with structured output
# ---------------------------------------------------
structured_llm = llm.with_structured_output(Celebrity)

# ---------------------------------------------------
# 5. Invoke the LLM
# ---------------------------------------------------
response = structured_llm.invoke("Tell me about Hania Amir")

# ---------------------------------------------------
# 6. Since response is already a Celebrity object, access fields directly
# ---------------------------------------------------
print("Name:", response.name)
print("Country:", response.country)
print("Instagram Followers:", response.insta_followers)
