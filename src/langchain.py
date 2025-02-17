
from tools.text import get_summary
from tools.audio import audio_to_text
from openai import OpenAI

from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, create_openai_tools_agent
from langchain.schema import HumanMessage
from langchain_core.runnables.graph import MermaidDrawMethod
from IPython.display import display, Image

import os
from dotenv import main


if __name__ == "__main__":
    main.load_dotenv()


    class State(TypedDict):
        video_path: str
        audio_text: str
        summary: str

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    def audio_extraction_node(state: State):
        '''
        Extract audio from video
        '''
        







    
