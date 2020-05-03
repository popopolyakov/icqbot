from bot.bot import Bot
from bot.handler import MessageHandler, CommandHandler, BotButtonCommandHandler, UnknownCommandHandler, \
    HelpCommandHandler
import os
from os.path import join, dirname
from dotenv import load_dotenv
import json
import requests

import time
from urllib.parse import unquote

chick = unquote('%F0%9F%90%A3')
ne_nu_eto_ban = unquote('https%3A%2F%2Ffiles.icq.net%2Fget%2F28g8gdwjaVqYSCuoC9nApM5ddeb7a21ae')
russia = unquote(' %F0%9F%87%B7%F0%9F%87%BA')

dotenv_path = join(dirname(__file__), 'token.env')
load_dotenv(dotenv_path)
TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)


# class tests(user):
#     def __init__(self):

def start_mes(bot, event):
    # event.data['msgId']['text'] == '/start':

    nowtime = time.ctime()
    mas_time1 = nowtime.split(":")
    mas_time2 = mas_time1[0]
    mas_time3 = mas_time2.split(" ")
    int_hour = int(mas_time3[4])

    if int_hour < 12:
        bot.send_text(chat_id=event.from_chat, text='Доброе утро, {0}!'.format(event.data['from']['firstName']))
    if int_hour >= 18:
        bot.send_text(chat_id=event.from_chat, text='Добрый вечер, {0}!'.format(event.data['from']['firstName']))
    else:
        bot.send_text(chat_id=event.from_chat, text='Добрый день, {0}!'.format(event.data['from']['firstName']))

    bot.send_text(chat_id=event.from_chat, text='Я - бот "COVIDinfoBOT"\n'
                                                'Ты можешь:\n'
                                                '1) Написать сообщение, чтобы узнать новости по набранному контексту\n'
                                                '2) Пройти проверку на covid-2019\n'
                                                '3) Написать свой город, чтобы узнать эпидемиологическую обстановку в нем\n'
                                                'P.S Чтобы посмотреть возможности бота,'
                                                ' напиши: "/help" ')
    print("проверка")


def any_message(bot, event):
    bot.send_text(chat_id=event.from_chat, text='Чтобы разбудить бота, напишите: "/start" {0}'.format(russia))
    bot.send_text(chat_id=event.from_chat, text=ne_nu_eto_ban)
    print("проверка any_message")


def help_cb(bot, event):
    bot.send_text(chat_id=event.data['chat']['chatId'], text="Some message help")


def message_cb(bot, event):
    text = requests.get('https://api.thevirustracker.com/free-api', params={'global': 'stats'}, )
    if text.status_code != 200:
        # This means something went wrong.
        print('ВСЕ МИМО')
    data = text.json()
    data = data['results'][0]
    totalCases = data['total_cases']
    totalRecovered = data['total_recovered']
    # print(totalCases,totalRecovered)
    covidinfo = 'Всего заразившихся %s!' % totalCases
    # print(covidinfo)
    # print(event.from_chat)
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
    strToParse = event.data['callbackData'].split('_')
    count = strToParse[1]
    stage = strToParse[0]
    print(count, stage)
    log = 'Count: %s Stage: %s' % (count, stage)
    curUser = event.data['from']['userId']
    print('Log', log, '          Stage true?', stage == '0')
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

# print(dir(urllib.parse()))
# print(dir(bot.dispatcher.add_handler))
# print(bot.dispatcher.add_handler)
bot.dispatcher.add_handler(CommandHandler(command='start', callback=start_mes))
# bot.dispatcher.add_handler(MessageHandler(callback=message_cb))

bot.dispatcher.add_handler(MessageHandler(callback=any_message))

# bot.dispatcher.add_handler(UnknownCommandHandler(callback=any_message))

# Handler for help command
bot.dispatcher.add_handler(HelpCommandHandler(callback=help_cb))

bot.dispatcher.add_handler(CommandHandler(command='gettest', callback=runTests))
bot.dispatcher.add_handler(BotButtonCommandHandler(callback=testcommands))
bot.start_polling()
bot.idle()
