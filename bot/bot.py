import threading
import time
import telebot
import uuid 
from pytubefix import YouTube
from pathlib import Path
import os
import requests
import json


token = '7774412256:AAHJ7GKbG5sHtS_aU8J-Pdpwl7DAX_WInQA'
developer_id = '446597696'
SERVER_URL = 'http://127.0.0.1:8000/processFilename'
hello_msg = """*Привет\! 👋 
Я бот\-транскрибатор и умею:*

✅ Создавать краткие выводы из YouTube видео

❗️ Если что\-то пошло не так, пиши: @Pierre\_Morrel

Бот разработан командой [ИРЦЭИТ](https://www\.iddeit\.ru/\#/projects/transcriber)"""


TEMP_FOLDER = os.path.join(os.path.dirname(__file__), "..", "app", "temp") 

def send_to_server(chat_id, filename):
    try:
        response = requests.post(
            SERVER_URL,
            data=json.dumps({
                "chat_id": str(chat_id),
                "video_path": str(filename)
            })
        )
        
        if response.status_code == 200:
            return response.json()
        return None
        
    except Exception as e:
        print(f"Ошибка при отправке на сервер: {e}")
        return None

def show_typing_indicator(chat_id, duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        Bot.send_chat_action(chat_id, 'typing')
        time.sleep(1)


Bot = telebot.TeleBot(token, parse_mode = None)

@Bot.message_handler(commands=["start"])
def start(m, res=False):
    Bot.send_message(m.chat.id, hello_msg, parse_mode='MarkdownV2')
    Bot.send_message(m.chat.id, "Жду ссылку на видео 😊")
    Bot.register_next_step_handler(m, handle_link)
    
def handle_link(message):
    url = message.text
    status_msg = Bot.send_message(message.chat.id, "📥 Скачиваю видео с YouTube...")
    try:
        download_folder = TEMP_FOLDER
        
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

        stream.download(output_path=download_folder, filename=file)

        file_path = str(Path(os.path.join(download_folder, file)).resolve())

        Bot.edit_message_text(
            "✅ Видео успешно скачано!\n"
            "⚙️ Обрабатывается...",
            message.chat.id,
            status_msg.message_id
        )
        
        typing_thread = threading.Thread(
            target=show_typing_indicator, 
            args=(message.chat.id, 15)
        )
        
        typing_thread.start()

        server_response = send_to_server(message.chat.id, file)
        
        typing_thread.join()
        
        print(file_path)        
        if server_response and server_response.get('status') == 'success':
            Bot.edit_message_text(
                "✅ Файл успешно обработан сервером",
                message.chat.id,
                status_msg.message_id
            )
            transcribation_path = os.path.join(TEMP_FOLDER, f"transcribation_{unique_id}.txt")
            
            with open(transcribation_path, 'w', encoding='utf-8') as f:
                f.write(server_response["full_text"])
            
            with open(transcribation_path, 'rb') as doc:
                Bot.send_document(message.chat.id, doc, caption='Расшифровка видео')

            Bot.send_message(message.chat.id, "Суммаризация: \n" + server_response["summary"])
            
        else:
            Bot.reply_to(message, "❌ Ошибка обработки на сервере \n Пожалуйста, напишите @Pierre_Morrel 📩")
            Bot.delete_message(message.chat.id, status_msg.message_id)
                     
    except Exception as e:
        Bot.reply_to(message, f"❌ Ошибка: {str(e)} \n Пожалуйста, напишите @Pierre_Morrel 📩")
        Bot.delete_message(message.chat.id, status_msg.message_id)
    
    finally:
        Bot.send_message(message.chat.id, "Жду ссылку на следующее видео 😉")
        Bot.register_next_step_handler(message, handle_link)

        
@Bot.message_handler(content_types=['text'])
def answer(m):
    if m.text == "Admin111":
        Bot.send_message(m.chat.id, text="ADMIN")

Bot.polling()