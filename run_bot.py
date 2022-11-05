from os import path
import sys
sys.path.append(path.abspath('openchat'))

import random
from openchat.openchat import OpenChat
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
bot = telebot.TeleBot("5621518936:AAHBQTGtFHei6tHUD3WI_tFRPrUA2BV6SRw")

#TODO: Store message.from_user info to DB, but remember GDPR
#TODO: Write details to default persons, and check it out
#TODO: Add /thankyou with the list of patrons "and other unknown but knightly sirs who donated through the crypt"
#TODO: Write main function, move all command to itsown funcs, use changeable parameters as external

#openchat = OpenChat(model='blender.medium', device='cpu', environment='custom')
openchat = OpenChat(model='blender.small', device='cpu', environment='custom')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Hello {name}. First, you need to choose the person you want to talk to. Click to /choose".format(name=message.from_user.first_name))
    openchat.start()

def pers_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 4
    markup.add(InlineKeyboardButton("Scientist", callback_data="pers1"),
               InlineKeyboardButton("Tourist", callback_data="pers2"),
               InlineKeyboardButton("Student", callback_data="pers3"),
               InlineKeyboardButton("Custom", callback_data="pers4"))
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "pers1":
        openchat.setup_persona(call.message.from_user.id, "Good man, likes science, IT, computer. He is from London")
        bot.send_message(call.message.chat.id, "Ok, let's talk")
    elif call.data == "pers2":
        openchat.setup_persona(call.message.from_user.id, "Woman, tourist, from New York, USA, was in Africa")
        bot.send_message(call.message.chat.id, "Ok, let's talk")
    elif call.data == "pers3":
        openchat.setup_persona(call.message.from_user.id, "Girl, student, likes anime and cats")
        bot.send_message(call.message.chat.id, "Ok, let's talk")
    elif call.data == "pers4":
        bot.send_message(call.message.chat.id, "Not ready right now. Choose another option")

@bot.message_handler(commands=['choose'])
def choose_persona(message):
    openchat.start()
    bot.send_message(message.chat.id, "Choose who you want to talk to", reply_markup=pers_markup())

@bot.message_handler(commands=['wiki'])#TODO: meaning from wiki
def meaning_message(message):
    bot.send_message(message.chat.id, "Meaning of word from wiki. Not ready right now")

@bot.message_handler(commands=['tr'])#TODO: translate to several lang
def translation_message(message):
    bot.send_message(message.chat.id, "Translation of word to several lang. Not ready right now")

@bot.message_handler(commands=['stat'])#TODO: statistics
def statistics_message(message):
    bot.send_message(message.chat.id, "Statistics. Not ready right now")

@bot.message_handler(commands=['donate'])
def donate_message(message):
    bot.send_message(message.chat.id,
                     "*Hi, and thank you*\n"
                     "I'm learning English and that's why I created this AI bot. And I wanted to share with you. I hope, you like it.\n"
                     "You can donate any amount of money. Your money will be used to pay for servers and improve the bot.\n"
                     "Sincerely, Scientist\n\n"
                     "Patreon link\n"
                     "https://www.patreon.com/talkingwithai\n\n"
                     "Boosty link\n"
                     "https://boosty.to/talkingwithai\n\n"
                     "*ETH wallet (or any ERC20/BEP20 token)*\n"
                     "0xE7D1C11fefcb8c559DDb8838423553a8FB242712\n\n"
                     #"Bitcoin wallet\n"#TODO: add Bitcoin
                     #"\n\n"
                     #"*VISA*\n"
                     #"4374 6901 0038 9301\n\n"
                     "For all questions and suggestions, you can write to me\n"
                     "https://t.me/Scientist_Futuration",
                     parse_mode='Markdown')

@bot.message_handler(content_types=['text'])
def message(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot_massage = openchat.predict_message(message.from_user.id, message.text)
    bot.send_message(message.chat.id, bot_massage)

@bot.message_handler(content_types=['audio'])
def audio_message(message):
    bot.send_message(message.chat.id, "Audio messages are not ready right now")

bot.infinity_polling()
