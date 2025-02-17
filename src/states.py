from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from langchain_core.runnables.graph import MermaidDrawMethod
from IPython.display import display, Image


import os
from dotenv import main



main.load_dotenv()

class SummarizeState(TypedDict):
    video_path: str
    audio_text: str
    summary: str



