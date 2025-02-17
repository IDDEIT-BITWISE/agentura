import os
from dotenv import main

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import SequentialChain
from langchain.chains.llm import LLMChain
main.load_dotenv('../.env')

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

model = ChatOpenAI(model="gpt-4o", api_key=OPENAI_API_KEY)

result = model.invoke("Ты кто?")
print('full:')
print(result)

print('content:')
print(result.content)