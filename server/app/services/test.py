from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()
openai_api_key = os.environ.get('OPENAI_API_KEY')
llm = ChatOpenAI(openai_api_key=openai_api_key)
llm.invoke("Hello, world!")