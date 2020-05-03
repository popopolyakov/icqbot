from bot.bot import Bot
from bot.handler import MessageHandler, CommandHandler, BotButtonCommandHandler
import os
from os.path import join, dirname
from dotenv import load_dotenv
import json
import requests
import data
import pandas as pd

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)


# class tests(user):
#     def __init__(self):

def startmes(bot, event):
    if event.data['msgId']['text'] == '/start':
        bot.send_text(chat_id=event.from_chat, text='Привет')


def message_cb(bot, event):
    back = event.text.split()
    if back[0].lower() == 'всего' and len(back) > 1:
        if back[1].lower() == 'мир':
            wed_site = 'https://api.thevirustracker.com/free-api?global=stats'
            text = requests.get(wed_site)
            if text.status_code != 200:
                # This means something went wrong.
                print('ВСЕ МИМО')
            else:
                data = text.json()
                totalCases = data['results'][0]['total_cases']
                totalRecovered = data['results'][0]['total_recovered']
                total_deaths = data['results'][0]['total_deaths']
                covidinfo = 'Мир' + \
                            '\nВсего заразившихся %s' % totalCases + \
                            '\nВсего выздоровело %s' % totalRecovered + \
                            '\nВсего умерло %s' % total_deaths
                curUser = event.data['from']['userId']
                bot.send_text(chat_id=curUser, text=covidinfo)
        else:
            coun = back[1][0].upper() + back[1][1:].lower()
            wed_site = 'https://api.thevirustracker.com/free-api?countryTotal=' + data.country[coun]
            text = requests.get(wed_site)
            if text.status_code != 200:
                # This means something went wrong.
                print('ВСЕ МИМО')
            else:
                data = text.json()
                totalCases = data['countrydata'][0]['total_cases']
                totalRecovered = data['countrydata'][0]['total_recovered']
                total_deaths = data['countrydata'][0]['total_deaths']
                covidinfo = '%s:' % coun + \
                            '\nВсего заразившихся %s' % totalCases + \
                            '\nВсего выздоровело %s' % totalRecovered + \
                            '\nВсего умерло %s' % total_deaths
                curUser = event.data['from']['userId']
                bot.send_text(chat_id=curUser, text=covidinfo)
    elif back[0].lower() == 'сегодня' and len(back) > 1:
        if back[1].lower() == 'мир':
            wed_site = 'https://api.thevirustracker.com/free-api?global=stats'
            text = requests.get(wed_site)
            if text.status_code != 200:
                # This means something went wrong.
                print('ВСЕ МИМО')
            else:
                data = text.json()
                todayCases = data['results'][0]['total_new_cases_today']
                todaydeaths = data['results'][0]['total_new_deaths_today']
                covidinfo = 'Мир' + \
                            '\nСегодня заразившихся %s' % todayCases + \
                            '\nСегодня умерло %s' % todaydeaths
                curUser = event.data['from']['userId']
                bot.send_text(chat_id=curUser, text=covidinfo)
        else:
            coun = back[1][0].upper() + back[1][1:].lower()
            wed_site = 'https://api.thevirustracker.com/free-api?countryTotal=' + data.country[coun]
            text = requests.get(wed_site)
            if text.status_code != 200:
                # This means something went wrong.
                print('ВСЕ МИМО')
            else:
                data = text.json()
                print(data)
                todayCases = data['countrydata'][0]['total_new_cases_today']
                todaydeaths = data['countrydata'][0]['total_new_deaths_today']
                covidinfo = '%s:' % coun + \
                            '\nСегодня заразившихся %s' % todayCases + \
                            '\nСегодня умерло %s' % todaydeaths
                curUser = event.data['from']['userId']
                bot.send_text(chat_id=curUser, text=covidinfo)
    else:
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
    pass


def recommendation(bot, event):
    bot.send_text(chat_id=event.from_chat,
                  text=data.recomend)


def stat(bot, event):
    bot.send_text(chat_id=event.from_chat,
                  text=data.recomend)


bot.dispatcher.add_handler(MessageHandler(callback=message_cb))
bot.dispatcher.add_handler(CommandHandler(command='info', callback=stat))
bot.dispatcher.add_handler(CommandHandler(command='start', callback=startmes))
bot.dispatcher.add_handler(CommandHandler(command='gettest', callback=runTests))
bot.dispatcher.add_handler(CommandHandler(command='recommend', callback=recommendation))
bot.dispatcher.add_handler(BotButtonCommandHandler(callback=testcommands))
bot.start_polling()
bot.idle()
