from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

# ---------------------------------------------------
# 1. Load environment variables from .env
# ---------------------------------------------------
load_dotenv()

# ---------------------------------------------------
# 2. Create the "generation" prompt template
# ---------------------------------------------------
generation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",   # 👈 This message is always treated as system instructions
            "You are a twitter techie influencer assistant tasked with writing excellent twitter posts."
            " Generate the best twitter post possible for the user's request."
            " If the user provides critique, respond with a revised version of your previous attempts.",
        ),
        # 👇 This will hold all past + current conversation messages dynamically
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# ---------------------------------------------------
# 3. Create the "reflection" prompt template
# ---------------------------------------------------
reflection_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",   # 👈 Instructions for reflection phase
            "You are a viral twitter influencer grading a tweet. Generate critique and recommendations for the user's tweet."
            "Always provide detailed recommendations, including requests for length, virality, style, etc.",
        ),
        # 👇 Again, insert the entire conversation history here
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# ---------------------------------------------------
# 4. Setup Google Gemini as the LLM
# ---------------------------------------------------
google_api_key = os.getenv("googleapi")  # read API key from .env
llm = ChatGoogleGenerativeAI(
    model='gemini-1.5-flash',            # Fast + cheap model for testing
    google_api_key=google_api_key
)

# ---------------------------------------------------
# 5. Combine prompts with LLM into runnable "chains"
# ---------------------------------------------------
generation_chain = generation_prompt | llm   # "pipe" means: fill prompt -> send to LLM
reflection_chain = reflection_prompt | llm
