import logging
import os
from flask import Flask,request
from telegram.ext import CommandHandler,Updater,MessageHandler,Filters,Dispatcher
from telegram import Bot,Update,ReplyKeyboardMarkup
from utils import get_reply, fetch_news, topics_keyboard
#enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                   level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "1212130808:AAEOYU2pjn5zM18IVzp5iwFvRUijJFylO7M"
#app object
app = Flask(__name__)
@app.route('/')
def index():
    return "hello"

@app.route(f'/{TOKEN}', methods=['GET','POST'])
def webhook():
    """ webhook view which receives updates from telegram"""
    #create update obj from json-format request data
    update = Update.de_json(request.get_json(),bot)
    #process update
    dp.process_update(update)
    return "ok"



def start(bot,update):#default arg
    print(update)
    author = update.message.from_user.first_name
    reply = "Hi!, {}".format(author)
    bot.send_message(chat_id=update.message.chat_id,text=reply)
def _help(bot,update):
    help_text = "Hey! this is the help text."
    bot.send_message(chat_id=update.message.chat_id,text=help_text)
def news(bot,update):
    bot.send_message(chat_id=update.message.chat_id,text="Choose a category:",
        reply_markup=ReplyKeyboardMarkup(keyboard=topics_keyboard,one_time_keyboard=True))


def reply_text(bot,update):
    intent, reply = get_reply(update.message.text, update.message.chat_id)
    if intent == "get_news":
        articles = fetch_news(reply)
        for article in articles:

            bot.send_message(chat_id=update.message.chat_id,text=article['link'])

    else:
        bot.send_message(chat_id=update.message.chat_id,text=reply)
def echo_sticker(bot,update):
    bot.send_sticker(chat_id=update.message.chat_id,sticker=update.message.sticker.file_id)
def error(bot,update):
    logger.error("Update '%s' caused error '%s'",update,update.error)
  

bot = Bot(TOKEN)
try:
    bot.set_webhook("https://pacific-refuge-55647.herokuapp.com/"+TOKEN)
except Exception as e:
    print(e)
    
dp = Dispatcher(bot, None)
dp.add_handler(CommandHandler("start",start))
dp.add_handler(CommandHandler("help",_help))
dp.add_handler(CommandHandler("news",news))
dp.add_handler(MessageHandler(Filters.text,reply_text))
dp.add_handler(MessageHandler(Filters.sticker,echo_sticker))
        
dp.add_error_handler(error)
dp.add_error_handler(error)            
if __name__ =="__main__":
    port = int(os.environ.get("PORT", 8443))
    app.run(host='0.0.0.0', port=port)
    