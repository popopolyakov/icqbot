import random
from bot.bot import Bot
from bot.filter import Filter
from bot.handler import MessageHandler, CommandHandler, BotButtonCommandHandler, HelpCommandHandler
import os
from os.path import join, dirname
from dotenv import load_dotenv
import json
import requests
import sys
from PIL import Image
from bs4 import BeautifulSoup
import data_messengs
from itertools import islice
import json
import random
import time
from urllib.parse import unquote

# фильтр на вхходящий ивент ф-ция messae_cb


chick = unquote('%F0%9F%90%A3')
ne_nu_eto_ban = unquote('https%3A%2F%2Ffiles.icq.net%2Fget%2F28g8gdwjaVqYSCuoC9nApM5ddeb7a21ae')
russia = unquote(' %F0%9F%87%B7%F0%9F%87%BA')
tanec = unquote('%F0%9F%95%BA')

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)


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


def message_cb(bot, event):
    back = event.text.split()
    if back[0].lower() == 'мир':
        wed_site = 'https://api.thevirustracker.com/free-api?global=stats'
        text = requests.get(wed_site)
        if text.status_code != 200:
            # This means something went wrong.
            print('ВСЕ МИМО')
        else:
            data = text.json()
            total_cases = data['results'][0]['total_cases']
            total_recovered = data['results'][0]['total_recovered']
            total_deaths = data['results'][0]['total_deaths']
            today_cases = data['results'][0]['total_new_cases_today']
            todaydeaths = data['results'][0]['total_new_deaths_today']
            covidinfo = 'Мир' + \
                        '\nВсего заразившихся %s' % total_cases + \
                        '\nВсего выздоровело %s' % total_recovered + \
                        '\nВсего умерло %s' % total_deaths + \
                        '\nСегодня заразившихся %s' % today_cases + \
                        '\nСегодня умерло %s' % todaydeaths
            curUser = event.data['from']['userId']
            bot.send_text(chat_id=curUser, text=covidinfo)
    if back[0][0].upper() + back[0][1:].lower() in data_messengs.country:
        coun = back[0][0].upper() + back[0][1:].lower()
        wed_site = 'https://api.thevirustracker.com/free-api?countryTotal=' + data_messengs.country[coun]
        text = requests.get(wed_site)
        if text.status_code != 200:
            # This means something went wrong.
            print('ВСЕ МИМО')
        else:
            data_country = text.json()
            print(data_country)
            total_cases = data_country['countrydata'][0]['total_cases']
            total_recovered = data_country['countrydata'][0]['total_recovered']
            totaldeaths = data_country['countrydata'][0]['total_deaths']
            today_cases = data_country['countrydata'][0]['total_new_cases_today']
            todaydeaths = data_country['countrydata'][0]['total_new_deaths_today']
            print(total_cases)
            covidinfo = '%s:' % coun + \
                        '\nВсего заразившихся %s' % total_cases + \
                        '\nВсего выздоровело %s' % total_recovered + \
                        '\nВсего умерло %s' % totaldeaths + \
                        '\nСегодня заразившихся %s' % today_cases + \
                        '\nСегодня умерло %s' % todaydeaths
            print(covidinfo)
            curUser = event.data['from']['userId']
            bot.send_text(chat_id=curUser, text=covidinfo)
    region = event.text[0].upper() + event.text[1:].lower()
    reg_data = data_messengs.regions_stat
    if region in reg_data:
        print(reg_data)
        covidinfo = region + \
                    '\nВсего заразившихся %s' % reg_data[region]['data_confirmed'] + \
                    '\nВсего вылечено %s' % reg_data[region]['data_cured'] + \
                    '\nВсего умерло %s' % reg_data[region]['data_deaths'] + \
                    '\nСегодня заразившихся %s' % reg_data[region]['data_today_confirmed'] + \
                    '\nСегодня вылечено %s' % reg_data[region]['data_today_cured'] + \
                    '\nСегодня умерло %s' % reg_data[region]['data_today_deaths'] + \
                    '\n% Смертей ' + str(reg_data[region]['data_deaths_pros'])

        curUser = event.data['from']['userId']
        bot.send_text(chat_id=curUser, text=covidinfo)



def runTests(bot, event):
    bot.send_text(chat_id=event.from_chat,
                  text='Привет, это тест на определение вашего психологического спокойствия во время самоизоляции.'
                       ' Нажми "Начать" или "Отмена"',
                  inline_keyboard_markup="{}".format(json.dumps([[
                      {"text": "Начать тест", "callbackData": "0_0"},
                      {"text": "Отмена", "callbackData": "cancel", "style": "attention"},
                  ]])))


def testcommands(bot, event):
    if event.data['callbackData'] == "1_recommend":
        bot.send_text(chat_id=event.from_chat,
                      text=data_messengs.recommend_1)

    if event.data['callbackData'] == "2_recommend":
        bot.send_text(chat_id=event.from_chat,
                      text=data_messengs.recommend_2)

    if event.data['callbackData'] == "3_recommend":
        curUser = event.data['from']['userId']
        bot.send_text(chat_id=curUser,
                      text=data_messengs.recommend_3)
    # print(bot)
    # print(event)
    # print(event.data['callbackData'])
    strToParse = event.data['callbackData'].split('_')
    count = int(strToParse[1])
    stage = int(strToParse[0])
    photo = 0
    if (len(strToParse) == 3):
        photo = bool(strToParse[2])
    print(count, stage)
    log = 'Count: %s Stage: %s' % (count, stage)
    curUser = event.data['from']['userId']
    print('Log', log, '          Stage true?', stage == 0)
    # bot.send_text(chat_id=curUser, text=log)
    msg_id = event.data['message']['msgId']
    print(msg_id, 'msg id')
    newCounter = []
    curCount = count
    if stage != 8:
        for count in range(count, count + 4, 1):
            newCounter.append(str(stage + 1) + '_' + str(count + 1))
        print(newCounter)
    else:
        newCounter.append(str(stage + 1) + '_' + str(count + 1) + '_False')
        newCounter.append(str(stage + 1) + '_' + str(count + 1) + '_True')
        print(newCounter)
    #######
    ##ЗНАЮ ЧТО МОЖНО по DRY вовее но надо быстрее на следующее переходить((((((((((((
    #######
    if stage == 0:
        bot.edit_text(chat_id=curUser, msg_id=msg_id,
                      text="Злились ли вы во время самоизоляции из-за глупости или неловкости другого человека ?",
                      inline_keyboard_markup="{}".format(json.dumps([[
                          {"text": "Почти никогда.", "callbackData": newCounter[0]},
                          {"text": "Периодически", "callbackData": newCounter[1]},
                          {"text": "Да, довольно часто", "callbackData": newCounter[2]},
                      ]])))
    if stage == 1:
        bot.edit_text(chat_id=curUser, msg_id=msg_id,
                      text="Поросыпались ли вы во время самоизоляции посреди ночи с сильным сердцебиением ?",
                      inline_keyboard_markup="{}".format(json.dumps([[
                          {"text": "Нет, ни разу", "callbackData": newCounter[0]},
                          {"text": "Периодически", "callbackData": newCounter[1]},
                          {"text": "Да, довольно часто", "callbackData": newCounter[2]},
                      ]])))
    if stage == 2:
        bot.edit_text(chat_id=curUser, msg_id=msg_id,
                      text="Можете ли вы прибегнуть к силе своего голоса, чтобы отстоять свою точку зрения ?",
                      inline_keyboard_markup="{}".format(json.dumps([[
                          {"text": "Могу, но очень редко", "callbackData": newCounter[0]},
                          {"text": "Нет, но сдерживаться трудно", "callbackData": newCounter[1]},
                          {"text": "Ясное дело, могу.", "callbackData": newCounter[2]},
                      ]])))
    if stage == 3:
        bot.edit_text(chat_id=curUser, msg_id=msg_id, text="Вы довольны своей фигурой ?",
                      inline_keyboard_markup="{}".format(json.dumps([[
                          {"text": "Да, несомненно", "callbackData": newCounter[0]},
                          {"text": "Да, но не всем", "callbackData": newCounter[1]},
                          {"text": "Нет", "callbackData": newCounter[2]},
                      ]])))
    if stage == 4:
        bot.edit_text(chat_id=curUser, msg_id=msg_id,
                      text="Если ваши отношения с партнером потерпят крах, у вас есть свободный выбор среди нескольких кандидатов ? (Если вы одиноки в данный момент, был бы у вас выбор среди кандидатур, если бы вы стремились к новому партнерству ?)",
                      inline_keyboard_markup="{}".format(json.dumps([[
                          {"text": "Огромный выбор", "callbackData": newCounter[0]},
                          {"text": "Будет легко", "callbackData": newCounter[1]},
                          {"text": "Мне нужно время", "callbackData": newCounter[2]},
                      ]])))
    if stage == 5:
        bot.edit_text(chat_id=curUser, msg_id=msg_id, text="Как часто вам снятся страшные сны ?",
                      inline_keyboard_markup="{}".format(json.dumps([[
                          {"text": "Почти никогда", "callbackData": newCounter[0]},
                          {"text": "Иногда", "callbackData": newCounter[1]},
                          {"text": "Чаще 1 раза в месяц", "callbackData": newCounter[2]},
                      ]])))
    if stage == 6:
        bot.edit_text(chat_id=curUser, msg_id=msg_id, text="У вас есть надежный круг хороших друзей ?",
                      inline_keyboard_markup="{}".format(json.dumps([[
                          {"text": "Да, безусловно", "callbackData": newCounter[0]},
                          {"text": "В основном приятели", "callbackData": newCounter[1]},
                          {"text": "У меня есть только я", "callbackData": newCounter[2]},
                      ]])))
    if stage == 7:
        bot.edit_text(chat_id=curUser, msg_id=msg_id,
                      text="Временами у меня бывают приступы смеха или плача, с которыми я никак не могу справиться?",
                      inline_keyboard_markup="{}".format(json.dumps([[
                          {"text": "Никогда", "callbackData": newCounter[0]},
                          {"text": "Иногда", "callbackData": newCounter[1]},
                          {"text": "Часто", "callbackData": newCounter[2]},
                      ]])))
    if stage == 8:
        print(newCounter, 'NEW COUNTER')
        bot.edit_text(chat_id=curUser, msg_id=msg_id, text='Ваши результаты записаны, желаете узнать результат?',
                      inline_keyboard_markup="{}".format(json.dumps([[
                          {"text": 'Да, конечно', 'callbackData': newCounter[0]},
                          {"text": "Отмена", "callbackData": newCounter[1]},
                      ]])))
    print(stage == 9 & photo == True)
    if stage == 9 and photo == True:
        bot.send_text(chat_id=curUser, text=curCount)
        if (curCount > 10):
            bot.send_text(chat_id=curUser,
                          text='Поздравляем, вы здоровы. А чтобы еще вас развеселить, загрузите ваше фото :)',
                          inline_keyboard_markup="{}".format(json.dumps([[
                              {"text": 'Прикрепить фото', 'callbackData': newCounter[0]},
                              {"text": "Отмена", "callbackData": newCounter[1]},
                          ]])))
            bot.send_text(chat_id=curUser, text='Ждем ваше фото')
        if (curCount <= 10):
            bot.send_text(chat_id=curUser, text='Рекомендуем обратиться за помощью к психологу. 8 (800) 333-44-34')
    print(stage == 9)
    if stage == 9 and photo == False:
        if (curCount > 12):
            bot.send_text(chat_id=curUser, text='Поздравляем, вы здоровы')
        if (curCount < 12):
            bot.send_text(chat_id=curUser, text='Рекомендуем обратиться за помощью')
        bot.send_text(chat_id=curUser, text='Спасибо за прохождение кода')


def watermark_photo(input_image_path,
                    output_image_path,
                    watermark_image_path,
                    position):
    base_image = Image.open(input_image_path)
    watermark = Image.open(watermark_image_path)

    # add watermark to your image
    base_image.paste(watermark, position)
    base_image.save(output_image_path)


def image_cb(bot, event):
    curUser = event.data['chat']['chatId']
    photo = event.data['parts'][0]['payload']['fileId']
    print(photo)
    infoPhoto = bot.get_file_info(file_id=photo)
    url = infoPhoto.json()['url']
    print('PHOTo JSON', infoPhoto.json(), '\n\nURL', url)
    bot.send_text(chat_id=curUser,
                  text=infoPhoto.json()['filename'])
    try:
        resp = requests.get(url, stream=True).raw
        print('resp', resp)
    except requests.exceptions.RequestException as e:
        sys.exit(1)
    try:
        img = Image.open(resp)
        print('img', img)
    except IOError:
        print("Unable to open image")
        sys.exit(1)
    downloadphotojpg = photo + '.jpg'
    img.save(downloadphotojpg)
    photolabel = photo + '_new.jpg'
    print(photolabel)
    watermark_photo(downloadphotojpg, photolabel,
                    'zdorov.jpg', position=(0, 0))
    # print(event.data['chat']['chatId'], 'USER')
    with open(photolabel, "rb") as file:
        bot.send_file(chat_id=curUser, file=file)


def getwebpage(bot, event):
    curUser = event.data['from']['userId']
    url = 'https://koronovirus.site/ru/russia/50/'  # url для второй страницы
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html5lib')
    root = soup.html
    root_childs = [e.name for e in root.children if e.name is not None]
    # print(table)
    # with open('test.html', 'w') as output_file:
    #     output_file.write(r.text.encode('cp1251'))


def sleeps(bot, event):
    curUser = event.data['from']['userId']


def mygame_mygame_bastaakanagana(bot, event):
    # random.randint(A, B) - случайное целое число N, A ≤ N ≤ B.
    d = {a: str(random.randint(0, 1)) for a in range(0, 10, 1)}
    print(d)
    print(event.data)
    bot.send_text(chat_id=event.from_chat, text='Игра.\nПеред тобой 10 человек: '
                                                'вычисли того, кто болен короновирусом.\n')
    print(d[0], d[1], d[2])
    tanec = 'fafafaa'
    bot.send_text(chat_id=event.from_chat,
                  text='Выбери чела, кого ты считаешь зараженным.',
                  inline_keyboard_markup="[{}]".format(json.dumps([
                      {"text": tanec, "callbackData": d[0]}, {"text": tanec, "callbackData": d[1]},
                      {"text": tanec, "callbackData": d[2]}, {"text": tanec, "callbackData": d[3]},
                      {"text": tanec, "callbackData": d[4]}, {"text": tanec, "callbackData": d[5]},
                      {"text": tanec, "callbackData": d[6]}, {"text": tanec, "callbackData": d[7]},
                  ])))


def recommendation(bot, event):
    bot.send_text(chat_id=event.from_chat,
                  text=data_messengs.main_recomend,
                  inline_keyboard_markup="{}".format(json.dumps([[
                      {"text": "1", "callbackData": "1_recommend", "style": "attention"},
                      {"text": "2", "callbackData": "2_recommend", "style": "attention"},
                      {"text": "3", "callbackData": "3_recommend", "style": "attention"}
                  ]])))


def buttons_answer_cb(bot, event):
    print(event.data)
    curUser = event.data['from']['userId']
    if event.data['callbackData'] == "1":
        bot.send_text(chat_id=curUser, text='gagaga')
    elif event.data['callbackData'] == "0":
        bot.send_text(chat_id=curUser, text="YOU LOOSE!")


def stat(bot, event):
    bot.send_text(chat_id=event.from_chat,
                  text=data_messengs.info)


def help_cb(bot, event):
    bot.send_text(chat_id=event.data['chat']['chatId'], text="Some message help")


bot.dispatcher.add_handler(HelpCommandHandler(callback=help_cb))

bot.dispatcher.add_handler(MessageHandler(callback=message_cb))
# bot.dispatcher.add_handler(MessageHandler(filters=Filter.image, callback=image_cb))
bot.dispatcher.add_handler(CommandHandler(command='start', callback=start_mes))
bot.dispatcher.add_handler(CommandHandler(command='getwebpage', callback=getwebpage))
bot.dispatcher.add_handler(CommandHandler(command='gotosleep', callback=sleeps))
bot.dispatcher.add_handler(CommandHandler(command='game', callback=mygame_mygame_bastaakanagana))
bot.dispatcher.add_handler(CommandHandler(command='gettest', callback=runTests))
bot.dispatcher.add_handler(CommandHandler(command='recommend', callback=recommendation))
bot.dispatcher.add_handler(BotButtonCommandHandler(callback=testcommands))
bot.dispatcher.add_handler(CommandHandler(command='info', callback=stat))

bot.start_polling()
bot.idle()
