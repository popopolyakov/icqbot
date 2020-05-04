import database
import numpy
from bot.bot import Bot
from bot.filter import Filter
from bot.handler import MessageHandler, CommandHandler, BotButtonCommandHandler, HelpCommandHandler
import os
from os.path import join, dirname
from dotenv import load_dotenv
import requests
import sys
from PIL import Image
from bs4 import BeautifulSoup
import json
import random
import time
from urllib.parse import unquote
#фильтр на вхходящий ивент ф-ция messae_cb


chick =unquote('%F0%9F%90%A3')
ne_nu_eto_ban = unquote('https%3A%2F%2Ffiles.icq.net%2Fget%2F28g8gdwjaVqYSCuoC9nApM5ddeb7a21ae')
russia =unquote (' %F0%9F%87%B7%F0%9F%87%BA')
tanec = unquote('%F0%9F%95%BA')
virus = unquote('%F0%9F%A6%A0')
prorvemsia = unquote('https%3A%2F%2Ffiles.icq.net%2Fget%2F28g8g000jFvRkjcVN6asG05e8793f11bd')
remont = unquote('%F0%9F%9B%A0%EF%B8%8F')
#ДЛЯ ИГРЫ COVID19
people1 = unquote('%F0%9F%A7%9F%E2%80%8D%E2%99%82%EF%B8%8F')
people2 = unquote('%F0%9F%91%A9%E2%80%8D%F0%9F%8E%A4')
people3 = unquote('%F0%9F%91%A8%E2%80%8D%E2%9C%88%EF%B8%8F')
people4 = unquote('%F0%9F%91%A8%E2%80%8D%F0%9F%92%BB')
people5 = unquote('%F0%9F%8E%85')
people6 = unquote('%F0%9F%91%A8%E2%80%8D%F0%9F%94%AC')
people7 = unquote('%F0%9F%99%8B%E2%80%8D%E2%99%82%EF%B8%8F')
people8 = unquote('%F0%9F%99%8B%E2%80%8D%E2%99%82%EF%B8%8F')
people9 = unquote('%F0%9F%A4%B4')
people10 = unquote('%F0%9F%A6%B8%E2%80%8D%E2%99%80%EF%B8%8F')
people11 = unquote('%F0%9F%A7%99%E2%80%8D%E2%99%80%EF%B8%8F')
people12 = unquote('%F0%9F%A7%9C%E2%80%8D%E2%99%82%EF%B8%8F')
people13 = unquote('%F0%9F%91%A8%E2%80%8D%F0%9F%9A%80')
people14 = unquote('%F0%9F%A7%9B%E2%80%8D%E2%99%82%EF%B8%8F')
people15 = unquote('%F0%9F%91%A8%E2%80%8D%F0%9F%94%A7')
people16 = unquote('%F0%9F%91%A9%E2%80%8D%F0%9F%8E%93')
people_covid = [people1,people2,people3,people4,
                people5,people6,people7,people8,
                people9,people10,people11,people12,
                people13,people14,people15,people16]

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)

def UnknownCommand(bot, event):
    bot.send_text(chat_id=event.from_chat, text = '{0}\n'
                  'Ой, извини, я не знаю такую команду...\n'
                  'Напиши /help , чтобы посмотреть, что я умею :)'.format(ne_nu_eto_ban))
    #bot.send_text(chat_id=event.from_chat, text = ne_nu_eto_ban)


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

    bot.send_text(chat_id=event.from_chat, text='Я - бот "COVIDinfoBOT"! {1}\n'
                                                'Я могу:\n'
                                                '1) Статистика по короновирусу - напиши: /info \n'
                                                '2) Рекомендации по короновирусу - напиши: /recommend \n'
                                                '3) Тест на психологическое состояние во время самоизоляции - напиши: /gettest \n'
                                                '4) Игра "Stop Covid-19" на повышение настроения - напиши: /game \n\n'
                                                'P.S Чтобы подробнее ознакомиться с возможностями бота,'
                                                ' напиши: /help \n'
                                                '{0}'.format(prorvemsia, russia))
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
    if back[0][0].upper() + back[0][1:].lower() in database.country:
        coun = back[0][0].upper() + back[0][1:].lower()
        wed_site = 'https://api.thevirustracker.com/free-api?countryTotal=' + database.country[coun]
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
    reg_data = database.regions_stat
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
                  text='Привет, это тест на определение вашего психологического спокойствия во время самоизоляции. Нажми "Начать" или "Отмена"',
                  inline_keyboard_markup="{}".format(json.dumps([[
                      {"text": "Начать тест", "callbackData": "0_0"},
                      {"text": "Отмена", "callbackData": "cancel", "style": "attention"},
                  ]])))


def testcommands(bot, event):
    curUser = event.data['from']['userId']
    if event.data['callbackData'] == "1_recommend":
        bot.send_text(chat_id=curUser,
                      text=database.recommend_1)

    if event.data['callbackData'] == "2_recommend":
        bot.send_text(chat_id=curUser,
                      text=database.recommend_2)

    if event.data['callbackData'] == "3_recommend":
        curUser = event.data['from']['userId']
        bot.send_text(chat_id=curUser,
                      text=database.recommend_3)

    # print(bot)
    # print(event)
    # print(event.data['callbackData'])
    strToParse=event.data['callbackData'].split('_')
    stage = int(strToParse[0])
    count = int(strToParse[1])
    if (len(strToParse)==3):
        photo = bool(strToParse[2])
    print(count, stage)
    log='Count: %s Stage: %s' % (count, stage)

    print('Log',log, '          Stage true?', stage == 0)
    #bot.send_text(chat_id=curUser, text=log)
    msg_id=event.data['message']['msgId']
    print(msg_id, 'msg id')
    newCounter = []
    curCount=count
    if stage != 8:
        for count in range(count,count+4,1):
            newCounter.append(str(stage+1)+'_'+str(count+1))
        print(newCounter)
    else:
        newCounter.append(str(stage+1)+'_'+str(count+1)+'_False')
        newCounter.append(str(stage + 1) + '_' + str(count + 1) + '_True')
        print(newCounter)
    #######
    ##ЗНАЮ ЧТО МОЖНО по DRY вовее но надо быстрее на следующее переходить((((((((((((
    #######
    if stage == 0:
        bot.edit_text(chat_id=curUser, msg_id=msg_id, text="Злились ли вы во время самоизоляции из-за глупости или неловкости другого человека ?",
                      inline_keyboard_markup="{}".format(json.dumps([[
                          {"text": "Почти никогда.", "callbackData": newCounter[0]},
                          {"text": "Периодически", "callbackData": newCounter[1]},
                          {"text": "Да, довольно часто", "callbackData": newCounter[2]},
            ]])))
    if stage == 1:
        bot.edit_text(chat_id=curUser, msg_id=msg_id, text="Поросыпались ли вы во время самоизоляции посреди ночи с сильным сердцебиением ?",
                      inline_keyboard_markup="{}".format(json.dumps([[
                          {"text": "Нет, ни разу", "callbackData": newCounter[0]},
                          {"text": "Периодически", "callbackData": newCounter[1]},
                          {"text": "Да, довольно часто", "callbackData": newCounter[2]},
            ]])))
    if stage == 2:
        bot.edit_text(chat_id=curUser, msg_id=msg_id, text="Можете ли вы прибегнуть к силе своего голоса, чтобы отстоять свою точку зрения ?",
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
        bot.edit_text(chat_id=curUser, msg_id=msg_id, text="Если ваши отношения с партнером потерпят крах, у вас есть свободный выбор среди нескольких кандидатов ? (Если вы одиноки в данный момент, был бы у вас выбор среди кандидатур, если бы вы стремились к новому партнерству ?)",
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
        bot.edit_text(chat_id=curUser, msg_id=msg_id, text="Временами у меня бывают приступы смеха или плача, с которыми я никак не могу справиться?",
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
    print(stage == 9 & photo==True)
    if stage == 9 and photo==True:
        bot.send_text(chat_id=curUser, text=curCount)
        if (curCount>10):
            bot.send_text(chat_id=curUser, text='Поздравляем, вы здоровы. А чтобы еще вас развеселить, загрузите ваше фото :)',
                          inline_keyboard_markup="{}".format(json.dumps([[
                              {"text": 'Прикрепить фото', 'callbackData': newCounter[0]},
                              {"text": "Отмена", "callbackData": newCounter[1]},
                          ]])))
            bot.send_text(chat_id=curUser, text='Ждем ваше фото')
        if (curCount<=10):
            bot.send_text(chat_id=curUser, text='Рекомендуем обратиться за помощью к психологу. 8 (800) 333-44-34')
    print(stage == 9)
    if stage == 9 and photo==False:
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

def image_cb(bot,event):
    curUser = event.data['chat']['chatId']
    photo = event.data['parts'][0]['payload']['fileId']
    print(photo)
    infoPhoto=bot.get_file_info(file_id=photo)
    url = infoPhoto.json()['url']
    print('PHOTo JSON', infoPhoto.json(), '\n\nURL', url)
    bot.send_text(chat_id=curUser,
                  text=infoPhoto.json()['filename'])
    try:
        resp = requests.get(url, stream=True).raw
        print('resp',resp)
    except requests.exceptions.RequestException as e:
        sys.exit(1)
    try:
        img = Image.open(resp)
        print('img', img)
    except IOError:
        print("Unable to open image")
        sys.exit(1)
    downloadphotojpg = photo+'.jpg'
    img.save(downloadphotojpg)
    bot.send_text(chat_id=event.from_chat,
                  text='Привет, это тест на определение вашего психологического спокойствия во время самоизоляции. Нажми "Начать" или "Отмена"',
                  inline_keyboard_markup="{}".format(json.dumps([[
                      {"text": "Пропустить", "callbackData": "0_0_true_none_none"},
                      {"text": "Пропустить", "callbackData": "0_0_false_none_none"},
                      {"text": "Отмена", "callbackData": "cancel", "style": "attention"},
                  ]])))


    photolabel=photo+'_new.jpg'
    print(photolabel)
    watermark_photo(downloadphotojpg, photolabel,
                    'zdorov.jpg', position=(0, 0))
    #print(event.data['chat']['chatId'], 'USER')
    with open(photolabel, "rb") as file:
        bot.send_file(chat_id=curUser, file=file)

def getwebpage(bot,event):
    curUser = event.data['from']['userId']
    url = 'https://koronovirus.site/ru/russia/50/' # url для второй страницы
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html5lib')
    root = soup.html
    # root_childs = [e.name for e in root.children if e.name is not None]
    # print(table)
    # with open('test.html', 'w') as output_file:
    #     output_file.write(r.text.encode('cp1251'))


def sleeps(bot,event):
    curUser = event.data['from']['userId']


def mygame_mygame_bastaakanagana(bot, event):
    # random.randint(A, B) - случайное целое число N, A ≤ N ≤ B.

    covid1people = random.randint(0, 7)
    covid2people = random.randint(0, 7)
    covid3people = random.randint(0, 7)
    d = {}
    for i in range(0, 8, 1):
        if i == covid1people or i == covid2people or i == covid3people:
            d[i] = "1"
        else:
            d[i] = "0"
    # d = {a: str(random.randint(0, 1)) for a in range(0,8,1)}

    emogi_nachalo = numpy.random.choice(people_covid, size=8, replace=False)

    global emogi_otvet
    emogi_otvet = []
    for i in range(0, 8, 1):

        if d[i] == "1":
            emogi_otvet.append(virus)
        else:
            emogi_otvet.append(emogi_nachalo[i])
    print(emogi_otvet)
    print(emogi_nachalo)
    print(d)

    print(event.data)
    # bot.send_text(chat_id=event.from_chat, text = 'Игра "Стоп сovid-19"\nПеред тобой 8 человек, но из них есть больные короновирусом :(\n ')
    #             # 'вычисли того, кто болен короновирусом.\n')
    print(d[0], d[1], d[2])
    msg_id1 = bot.send_text(chat_id=event.from_chat,
                            text='Игра "Stop Covid-19"\nПеред тобой 8 человек, но из них есть больные короновирусом :(\n '
                                 'Хорошо, что у тебя есть вакцина!\nВылечи человечка, кого считаешь зараженным! Но не промахнись!',
                            inline_keyboard_markup="[{}]".format(json.dumps([
                                {"text": emogi_nachalo[0], "callbackData": d[0]},
                                {"text": emogi_nachalo[1], "callbackData": d[1]},
                                {"text": emogi_nachalo[2], "callbackData": d[2]},
                                {"text": emogi_nachalo[3], "callbackData": d[3]},
                                {"text": emogi_nachalo[4], "callbackData": d[4]},
                                {"text": emogi_nachalo[5], "callbackData": d[5]},
                                {"text": emogi_nachalo[6], "callbackData": d[6]},
                                {"text": emogi_nachalo[7], "callbackData": d[7]}
                            ]))).json()['msgId']

def recommendation(bot, event):
    bot.send_text(chat_id=event.from_chat,
                  text=database.main_recomend,
                  inline_keyboard_markup="{}".format(json.dumps([[
                      {"text": "1", "callbackData": "1_recommend", "style": "attention"},
                      {"text": "2", "callbackData": "2_recommend", "style": "attention"},
                      {"text": "3", "callbackData": "3_recommend", "style": "attention"}
                  ]])))


def buttons_answer_cb(bot, event):
    print(event.data)
    curUser = event.data['from']['userId']
    msg_id1 = event.data['message']['msgId']
    print(msg_id1)
    print(curUser)
    otvet = event.data['callbackData']
    # print(d)
    # print(emogi_otvet)

    bot.edit_text(chat_id=curUser, msg_id=msg_id1,
                  text='У тебя есть вакцина!\nВылечи человечка, кого считаешь зараженным! Но не промахнись!',
                  inline_keyboard_markup="[{}]".format(json.dumps([
                      {"text": emogi_otvet[0], "callbackData": "3"}, {"text": emogi_otvet[1], "callbackData": "3"},
                      {"text": emogi_otvet[2], "callbackData": "3"}, {"text": emogi_otvet[3], "callbackData": "3"},
                      {"text": emogi_otvet[4], "callbackData": "3"}, {"text": emogi_otvet[5], "callbackData": "3"},
                      {"text": emogi_otvet[6], "callbackData": "3"}, {"text": emogi_otvet[7], "callbackData": "3"},
                  ])))

    if otvet == "1":

        index = 0
        flg = False

        f = open("jokes_like_a_grandfather_shit_in_a_stroller.txt")

        kol_jokes = int(f.readline())
        random_joke = random.randint(0, kol_jokes - 1)
        print(random_joke)

        while flg == False:

            stroka = next(f)
            if index == random_joke:
                bot.send_text(chat_id=curUser, text="Правильно! Вот приз!\n "
                                                    "Держи Секретный анекдот:\n"
                                                    "{0}\n"
                                                    "Чтобы сыграть еще раз - напиши: /game ".format(stroka))
                flg = True
            index += 1
        f.close()

    elif otvet == "0":
        bot.send_text(chat_id=curUser, text="Не угадал :(\nНичего страшного, начни сначала!\nНапиши: /game ")

def stat(bot, event):
    bot.send_text(chat_id=event.from_chat,
                  text=database.info)
def help_cb(bot, event):
    bot.send_text(chat_id=event.data['chat']['chatId'], text="/info - Статистика по короновирусу \n"
                  "/recommend - Рекомендации по короновирусу \n"
                  "/gettest - Тест на психологическое состояние во время самоизоляции \n"
                  "/game - Игра 'Stop Covid-19' на повышение настроения \n")

def getfun(bot, event):
    bot.send_text(chat_id=event.from_chat,
                  text='Ссылки, которые помогут не заскучать на карантине:\n\n\n'
                       '1. Послушать музыку в BOOM\n\n'
                       '2. Посмотреть фильм в Okko\n\n'
                       '3. Научиться чему то новому в GeekBrains\n\n'
                       '4. Просто вкусно покушать с DeliveryClub\n\n'
                       '5. Пострелять с друзьями в WarFace\n\n'
                       '6. Посмотреть интересное именно тебе видео на YouTube\n',
                  inline_keyboard_markup="{}".format(json.dumps([[
                      {"text": "1", "url": "https://boom.ru/"},
                      {"text": "2", "url": "http://okko.tv/"},
                      {"text": "3", "url": "http://geekbrains.ru/"},
                      {"text": "4", "url": "https://www.delivery-club.ru/"},
                      {"text": "5", "url": "https://wf.mail.ru/"},
                      {"text": "6", "url": "https://www.youtube.com/"},
                  ]])))


bot.dispatcher.add_handler(HelpCommandHandler(callback=help_cb))
bot.dispatcher.add_handler(MessageHandler(callback=message_cb))
bot.dispatcher.add_handler(MessageHandler(filters=Filter.image, callback=image_cb))
bot.dispatcher.add_handler(CommandHandler(command='start',callback=start_mes))
bot.dispatcher.add_handler(CommandHandler(command='getwebpage',callback=getwebpage))
bot.dispatcher.add_handler(CommandHandler(command='gotosleep',callback=sleeps))
bot.dispatcher.add_handler(CommandHandler(command='game',callback=mygame_mygame_bastaakanagana))
bot.dispatcher.add_handler(CommandHandler(command='gettest',callback=runTests))
bot.dispatcher.add_handler(CommandHandler(command='recommend', callback=recommendation))
bot.dispatcher.add_handler(BotButtonCommandHandler(callback=testcommands))
bot.dispatcher.add_handler(CommandHandler(command='info', callback=stat))
bot.dispatcher.add_handler(CommandHandler(command='getfun', callback=getfun))

bot.start_polling()
bot.idle()