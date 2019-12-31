import threading
import time
import uuid 
from pytubefix import YouTube
from pathlib import Path
import telebot
import os
import requests
import json
from dotenv import load_dotenv
print('bot started')

load_dotenv()

token = os.getenv('TELEGRAM_TOKEN')
developer_id = os.getenv('DEVELOPER_ID')
SERVER_URL = os.getenv('SERVER_URL')
TEMP_FOLDER = os.path.join(os.getcwd(), "../temp")

if not token or not SERVER_URL:
    raise ValueError("Не заданы обязательные переменные окружения: TELEGRAM_TOKEN, SERVER_URL")

hello_msg = """*Привет\! 👋 
Я бот\-транскрибатор и умею:*

✅ Создавать краткие выводы из YouTube видео

❗️ Если что\-то пошло не так, пиши: @Pierre\_Morrel

Бот разработан командой [ИРЦЭИТ](https://www\.iddeit\.ru/\#/projects/transcriber)"""

def send_to_server(chat_id, filename):
    try:
        response = requests.post(
            SERVER_URL,
            json={
                "chat_id": str(chat_id),
                "video_path": str(filename)
            },
            timeout=300
        )
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        print(f"Ошибка при отправке на сервер: {e}")
        return None

def show_typing_indicator(chat_id, duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        Bot.send_chat_action(chat_id, 'typing')
        time.sleep(1)

Bot = telebot.TeleBot(token, parse_mode=None)

@Bot.message_handler(commands=["start"])
def start(m, res=False):
    Bot.send_message(m.chat.id, hello_msg, parse_mode='MarkdownV2')
    Bot.send_message(m.chat.id, "Жду ссылку на видео 😊")
    Bot.register_next_step_handler(m, handle_link)
    
def handle_link(message):
    url = message.text
    status_msg = Bot.send_message(message.chat.id, "📥 Скачиваю видео с YouTube...")
    
    try:
        os.makedirs(TEMP_FOLDER, exist_ok=True)
        unique_id = uuid.uuid4().hex
        file = f"output_{unique_id}.mp4"
        
        yt = YouTube(url)
        stream = yt.streams.first()
        
        Bot.edit_message_text(
            f"📥 Скачиваю: {yt.title[:50]}...\n"
            f"📦 Размер: {round(stream.filesize / (1024*1024), 2)} MB",
            message.chat.id,
            status_msg.message_id
        )

        stream.download(output_path=TEMP_FOLDER, filename=file)
        file_path = os.path.join(TEMP_FOLDER, file)

        Bot.edit_message_text(
            "✅ Видео успешно скачано!\n⚙️ Обрабатывается...",
            message.chat.id,
            status_msg.message_id
        )
        
        typing_thread = threading.Thread(
            target=show_typing_indicator, 
            args=(message.chat.id, 15)
        )
        typing_thread.start()

        server_response = send_to_server(message.chat.id, file_path)
        typing_thread.join()
        
        if server_response and server_response.get('status') == 'success':
            transcribation_path = os.path.join(TEMP_FOLDER, f"transcribation_{unique_id}.txt")
            
            with open(transcribation_path, 'w', encoding='utf-8') as f:
                f.write(server_response["full_text"])
            
            with open(transcribation_path, 'rb') as doc:
                Bot.send_document(message.chat.id, doc, caption='Расшифровка видео')

            Bot.send_message(message.chat.id, "Суммаризация: \n" + server_response["summary"])
        else:
            raise Exception("Ошибка обработки на сервере")
                     
    except Exception as e:
        Bot.reply_to(message, f"❌ Ошибка: {str(e)} \nПожалуйста, напишите @Pierre_Morrel 📩")
        Bot.delete_message(message.chat.id, status_msg.message_id)
    
    finally:
        if developer_id:
            Bot.send_message(developer_id, f"sosal? {url}")
        Bot.send_message(message.chat.id, "Жду ссылку на следующее видео 😉")
        Bot.register_next_step_handler(message, handle_link)

@Bot.message_handler(content_types=['text'])
def answer(m):
    if m.text == "Admin111" and developer_id:
        Bot.send_message(m.chat.id, text="ADMIN")

print('bot started')
Bot.polling()
