import io

from bot.bot import Bot
from bot.filter import Filter
from bot.handler import MessageHandler, CommandHandler, BotButtonCommandHandler
import os
from os.path import join, dirname
from dotenv import load_dotenv
import json
import requests
import sys
from PIL import Image
from bs4 import BeautifulSoup
import html5lib

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)



# class tests(user):
#     def __init__(self):

def startmes(bot, event):
    bot.send_text(chat_id=event.from_chat, text='Привет')

def message_cb(bot, event):
    text=requests.get('https://api.thevirustracker.com/free-api',params={'global': 'stats'})
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
    count=int(strToParse[1])
    stage=int(strToParse[0])
    photo=0
    if (len(strToParse)==3):
        photo = bool(strToParse[2])
    print(count, stage)
    log='Count: %s Stage: %s' % (count, stage)
    curUser=event.data['from']['userId']
    print('Log',log, '          Stage true?', stage == '0')
    bot.send_text(chat_id=curUser, text=log)
    msg_id=event.data['message']['msgId']
    print(msg_id, 'msg id')
    newCounter = []
    if stage != 8:
        for count in range(count,count+4,1):
            newCounter.append(str(stage+1)+'_'+str(count+1))
        print(newCounter)
    else:
        newCounter[0]=str(stage+1)+'_'+str(count+1)+'_False'
        newCounter[1] = str(stage + 1) + '_' + str(count + 1) + '_True'
        print(newCounter)
    #######
    ##ЗНАЮ ЧТО МОЖНО по DRY вовее но надо быстрее на следующее переходить((((((((((((
    #######
    if stage == 0:
        bot.edit_text(chat_id=curUser, msg_id=msg_id, text="ты даун",
                      inline_keyboard_markup="{}".format(json.dumps([[
                          {"text": "да", "callbackData": newCounter[0]},
                          {"text": "ок", "callbackData": newCounter[1]},
                          {"text": "жопа", "callbackData": newCounter[2]},
            ]])))
    if stage == 1:
        bot.edit_text(chat_id=curUser, msg_id=msg_id, text="edited text1",
                      inline_keyboard_markup="{}".format(json.dumps([[
                          {"text": "да", "callbackData": newCounter[0]},
                          {"text": "жопа", "callbackData": newCounter[1]},
                          {"text": "ок", "callbackData": newCounter[2]},
            ]])))
    if stage == 2:
        bot.edit_text(chat_id=curUser, msg_id=msg_id, text="edited text2",
                      inline_keyboard_markup="{}".format(json.dumps([[
                          {"text": "Action 1", "callbackData": newCounter[0]},
                          {"text": "Action 2", "callbackData": newCounter[1]},
                          {"text": "Action 3", "callbackData": newCounter[2]},
            ]])))
    if stage == 3:
        bot.edit_text(chat_id=curUser, msg_id=msg_id, text="edited text3",
                      inline_keyboard_markup="{}".format(json.dumps([[
                          {"text": "Action 1", "callbackData": newCounter[0]},
                          {"text": "Action 2", "callbackData": newCounter[1]},
                          {"text": "Action 3", "callbackData": newCounter[2]},
            ]])))
    if stage == 4:
        bot.edit_text(chat_id=curUser, msg_id=msg_id, text="edited text4",
                      inline_keyboard_markup="{}".format(json.dumps([[
                          {"text": "Action 1", "callbackData": newCounter[0]},
                          {"text": "Action 2", "callbackData": newCounter[1]},
                          {"text": "Action 3", "callbackData": newCounter[2]},
            ]])))
    if stage == 5:
        bot.edit_text(chat_id=curUser, msg_id=msg_id, text="edited text5",
                      inline_keyboard_markup="{}".format(json.dumps([[
                          {"text": "Action 1", "callbackData": newCounter[0]},
                          {"text": "Action 2", "callbackData": newCounter[1]},
                          {"text": "Action 3", "callbackData": newCounter[2]},
            ]])))
    if stage == 6:
        bot.edit_text(chat_id=curUser, msg_id=msg_id, text="edited text6",
                      inline_keyboard_markup="{}".format(json.dumps([[
                          {"text": "Action 1", "callbackData": newCounter[0]},
                          {"text": "Action 2", "callbackData": newCounter[1]},
                          {"text": "Action 3", "callbackData": newCounter[2]},
            ]])))
    if stage == 7:
        bot.edit_text(chat_id=curUser, msg_id=msg_id, text="edited text7",
                      inline_keyboard_markup="{}".format(json.dumps([[
                          {"text": "Action 1", "callbackData": newCounter[0]},
                          {"text": "Action 2", "callbackData": newCounter[1]},
                          {"text": "Action 3", "callbackData": newCounter[2]},
            ]])))
    if stage == 8:
        bot.edit_text(chat_id=curUser, msg_id=msg_id, text='Ваши результаты записаны, желаете ввести фото?',
                  inline_keyboard_markup="{}".format(json.dumps([[
                      {"text": 'Прикрепить фото', 'callbackData': newCounter[0]},
                      {"text": "Отмена", "callbackData": newCounter[1]},
                  ]])))
    if stage == 9 & photo==True:
        if (count>12):
            bot.send_text(chat_id=curUser, text='Поздравляем, вы здоровы')
        if (count<12):
            bot.send_text(chat_id=curUser, text='Рекомендуем обратиться за помощью')
        bot.send_text(chat_id=curUser, text='Ждем ваше фото')
    if stage == 9 & photo==False:
        if (count > 12):
            bot.send_text(chat_id=curUser, text='Поздравляем, вы здоровы')
        if (count < 12):
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
    root_childs = [e.name for e in root.children if e.name is not None]
    #print(table)
    # with open('test.html', 'w') as output_file:
    #     output_file.write(r.text.encode('cp1251'))


def sleeps(bot,event):
    curUser = event.data['from']['userId']

bot.dispatcher.add_handler(MessageHandler(callback=message_cb))
bot.dispatcher.add_handler(MessageHandler(filters=Filter.image, callback=image_cb))
bot.dispatcher.add_handler(CommandHandler(command='start',callback=startmes))
bot.dispatcher.add_handler(CommandHandler(command='getwebpage',callback=getwebpage))
bot.dispatcher.add_handler(CommandHandler(command='gotosleep',callback=sleeps))
bot.dispatcher.add_handler(CommandHandler(command='gettest',callback=runTests))
bot.dispatcher.add_handler(BotButtonCommandHandler(callback=testcommands))
bot.start_polling()
bot.idle()