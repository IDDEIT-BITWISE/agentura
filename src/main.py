
from tools.text import get_summary
from tools.audio import audio_to_text
from openai import OpenAI

import os
from dotenv import main


if __name__ == "__main__":
    main.load_dotenv()

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    article = open('C://Users//Andrey//Desktop//agentura//agentura//src//test_media//test_article.txt',encoding='utf-8').read()
    audio_path = 'C://Users//Andrey//Desktop//agentura//agentura//src//test_media//test_auditt.mp3'

    audio2text = audio_to_text(audio_path=audio_path)

    print(f"""
    ====================
    ТЕКСТ ИЗ АУДИОЗАПИСИ
    ==================== 
          {audio2text}

""")
    
    title, summary = get_summary(audio2text)
    
    print(f'''
        ============
        СУММАРИЗАЦИЯ
        ============
{title}\n{summary}
''')




    
