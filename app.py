from bot.bot import Bot
from bot.handler import MessageHandler, CommandHandler, BotButtonCommandHandler
import os
from os.path import join, dirname
from dotenv import load_dotenv
import json
import requests


dotenv_path = join(dirname(__file__), 'token.env')
load_dotenv(dotenv_path)
TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)



# class tests(user):
#     def __init__(self):

def startmes(bot, event):
    if event.data['msgId']['text'] == '/start':
        bot.send_text(chat_id=event.from_chat, text='Привет')

def message_cb(bot, event):
    text=requests.get('https://api.thevirustracker.com/free-api',params={'global': 'stats'},)
    if text.status_code != 200:
        # This means something went wrong.
        print('ВСЕ МИМО')
    data=text.json()
    data=data['results'][0]
    totalCases=data['total_cases']
    totalRecovered=data['total_recovered']
   # print(totalCases,totalRecovered)
    covidinfo='Всего заразившихся %s!' % totalCases
   # print(covidinfo)
    #print(event.from_chat)
    print(event)
    bot.send_text(chat_id=event.from_chat, text=covidinfo)

def runTests(bot, event):
    print('Hai')
    bot.send_text(chat_id=event.from_chat,
                  text="Hello with buttons.",
                  inline_keyboard_markup="{}".format(json.dumps([[
                      {"text": "Action 1", "url": "http://mail.ru"},
                      {"text": "Action 2", "callbackData": "0_0", "style": "attention"},
                  ]])))


def testcommands(bot, event):
    print(bot)
    print(event)
    print(event.data['callbackData'])
    strToParse=event.data['callbackData'].split('_')
    count=strToParse[1]
    stage=strToParse[0]
    print(count, stage)
    log='Count: %s Stage: %s' % (count, stage)
    curUser=event.data['from']['userId']
    print('Log',log, '          Stage true?', stage == '0')
    bot.send_text(chat_id=curUser, text=log)

    if stage == '0':
        print('Hallo')
        msg_id = bot.send_text(chat_id=curUser, text="Message to be edited").json()['msgId']
        bot.edit_text(chat_id=curUser, msg_id=msg_id, text="edited text",
                      inline_keyboard_markup="{}".format(json.dumps([[
                {"text": "Action 1", "callbackData": "1_0"},
                {"text": "Action 2", "callbackData": "1_0", "style": "attention"},
            ]])))
        bot.answer_callback_query(
            query_id=event.data['queryId'],
            text=log,
            show_alert=False,
            inline_keyboard_markup="{}".format(json.dumps([[
                {"text": "Action 1", "url": "http://mail.ru"},
                {"text": "Action 2", "callbackData": "0_0", "style": "attention"},
            ]]))
        )
    if stage == '1':
        print('Hallo')
        bot.answer_callback_query(
            query_id=event.data['queryId'],
            text=log,
            show_alert=False
        )
   # if stage == '2':



bot.dispatcher.add_handler(MessageHandler(callback=message_cb))
bot.dispatcher.add_handler(CommandHandler(command='start',callback=startmes))
bot.dispatcher.add_handler(CommandHandler(command='gettest',callback=runTests))
bot.dispatcher.add_handler(BotButtonCommandHandler(callback=testcommands))
bot.start_polling()
bot.idle()
