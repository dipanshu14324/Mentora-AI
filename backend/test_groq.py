from dotenv import load_dotenv
import os

from langchain_groq import ChatGroq


load_dotenv()

key = os.getenv("GROQ_API_KEY")

print("KEY START:", key[:8])
print("KEY LENGTH:", len(key))


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=key,
    temperature=0
)


response = llm.invoke("Explain CNN in one sentence")

print(response.content)