import telebot
from telebot import types
import uuid 
from pytubefix import YouTube
import os

token = '6618739641:AAHvHVK0AnOnE90xn3G6TBw8jstGw0VbE9M'
developer_id = '446597696'


def start_keyboard():   
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    b1 = types.KeyboardButton(text="Оставить заявку")
    b2 = types.KeyboardButton(text="Заполнить карточку участника")
    keyboard.add(b1, b2)
    
    return keyboard

def again_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    b1 = types.KeyboardButton(text="Начать заново")
    keyboard.add(b1)
    
    return keyboard

        
Bot = telebot.TeleBot(token, parse_mode = None)

@Bot.message_handler(commands=["start"])
def start(m, res=False):
    Bot.send_message(m.chat.id, text="Привет! Отправь ссылку на видео!")
    Bot.register_next_step_handler(m, handle_link)
    
def handle_link(message):
    url = message.text
    try:
        download_folder = "downloads"
        
        unique_id = uuid.uuid4().hex
        file = f"output_{unique_id}.mp4"


        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        if not audio_stream:
            Bot.reply_to(message, "❌ Не удалось найти аудиопоток.")
            return

        audio_stream.download(output_path=download_folder, filename=file)

        Bot.send_message(message.chat.id, file)
        
        # with open(file, 'rb') as video_file:
        #     Bot.send_video(message.chat.id, video_file)
            
            # if os.path.exists(file):
            #     os.remove(file)
            
        
            
    except Exception as e:
        Bot.reply_to(message, f"❌ Ошибка: {str(e)}")
        
@Bot.message_handler(content_types=['text'])
def answer(m):
    if m.text == "Admin111":
        Bot.send_message(m.chat.id, text="ADMIN")

Bot.polling()