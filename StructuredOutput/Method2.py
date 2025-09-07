from typing_extensions import Annotated, TypedDict
from typing import Optional
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI

# ---------------------------------------------------
# 1. Load environment variables (API key from .env)
# ---------------------------------------------------
load_dotenv()
google_api_key = os.getenv("googleapi")

# ---------------------------------------------------
# 2. Define a structured schema using TypedDict
# ---------------------------------------------------
class Joke(TypedDict):
    """Joke to tell user."""

    setup: Annotated[str, ..., "The setup of the joke"]  
    punchline: Annotated[str, ..., "The punchline of the joke"]
    rating: Annotated[Optional[int], None, "How funny the joke is, from 1 to 10"]

# ---------------------------------------------------
# 3. Initialize Gemini model
# ---------------------------------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  # Fast + cheap model
    google_api_key=google_api_key
)

# ---------------------------------------------------
# 4. Wrap the LLM to force structured output
# ---------------------------------------------------
structured_llm = llm.with_structured_output(Joke)

# ---------------------------------------------------
# 5. Invoke the LLM
# ---------------------------------------------------
response = structured_llm.invoke("Tell me a short programming joke and rate it")

# ---------------------------------------------------
# 6. Since response is a Joke TypedDict, access fields directly
# ---------------------------------------------------
print("Setup:", response["setup"])
print("Punchline:", response["punchline"])
print("Rating:", response["rating"])
