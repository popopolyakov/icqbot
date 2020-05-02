from bot.bot import Bot
from bot.handler import MessageHandler
import os
from os.path import join, dirname
from dotenv import load_dotenv
import requests


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)

def message_cb(bot, event):

    text=requests.get('https://api.thevirustracker.com/free-api',params={'global': 'stats'},)
    if text.status_code != 200:
        # This means something went wrong.
        print('ВСЕ МИМО')
    data=text.json()
    data=data['results'][0]
    totalCases=data['total_cases']
    totalRecovered=data['total_recovered']
    print(totalCases,totalRecovered)
    covidinfo='Всего заразившихся %s!' % totalCases
    print(covidinfo)
    bot.send_text(chat_id=event.from_chat, text=covidinfo)


bot.dispatcher.add_handler(MessageHandler(callback=message_cb))
bot.start_polling()
bot.idle()