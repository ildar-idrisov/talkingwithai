import argparse
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from db.session import DB
from openchat.openchat import OpenChat

# TODO: Store message.from_user info to DB, but remember GDPR
# TODO: Write details to default persons, and check it out
# TODO: Add /thankyou with the list of patrons "and other unknown but knightly sirs who donated through the crypt"
# TODO: Write main function, move all command to itsown funcs, use changeable parameters as external

DB.init_database_interface()
DB.validate_database()
bot = telebot.TeleBot("5621518936:AAHBQTGtFHei6tHUD3WI_tFRPrUA2BV6SRw")
# openchat = OpenChat(model='blender.small', device='cpu', environment='custom', maxlen=2048)
# openchat = OpenChat(model='blender.medium', device='cpu', environment='custom')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Hello {name}. First, you need to choose the person you want to talk to. "
                                      "Click to /choose".format(name=message.from_user.first_name))
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
        openchat.setup_persona(call.message.chat.id, "A young man who is passionate about science and technology works in an IT company. He loves computers and enjoys spending time learning new technologies and programs. In his free time, he often participates in various scientific conferences and seminars to develop his knowledge and skills. This is a purposeful and responsible person who values time and manages all his duties. He loves to listen to rock.A young man who is passionate about science and technology works in an IT company. He loves computers and enjoys spending time learning new technologies and programs. In his free time, he often participates in various scientific conferences and seminars to develop his knowledge and skills. This is a purposeful and responsible person who values time and manages all his duties. He loves to listen to rock.A young man who is passionate about science and technology works in an IT company. He loves computers and enjoys spending time learning new technologies and programs. In his free time, he often participates in various scientific conferences and seminars to develop his knowledge and skills. This is a purposeful and responsible person who values time and manages all his duties. He loves to listen to rock.")
        bot.send_message(call.message.chat.id, "Ok, let's talk")
    elif call.data == "pers2":
        openchat.setup_persona(call.message.chat.id, "A woman is a lover of travel and new experiences. She often visits different countries and cities, studying their culture and history. She loves to visit museums and galleries, walk along the streets and enjoy the national cuisine. Our character also loves nature and often goes to the mountains or the sea to enjoy peace and solitude. She loves meeting new people and learning about their life and culture. She has recently been to Europe where she visited Paris, Rome, Barcelona and Berlin. She has also been to Asia where she visited Japan, Thailand and Indonesia. She saw many amazing places and enjoyed the beauty of nature.")
        bot.send_message(call.message.chat.id, "Ok, let's talk")
    elif call.data == "pers3":
        openchat.setup_persona(call.message.chat.id, "A young student girl, she often watches various anime series and films, and also reads manga. She is also a fan of cats and has several fluffy paws at home. She adores them and loves to take care of them, clean their litter box and play with them. She also loves to draw and create various illustrations of her favorite anime characters. Our character also appreciates education and tries to study successfully in order to realize her dreams in the future.")
        bot.send_message(call.message.chat.id, "Ok, let's talk")
    elif call.data == "pers4":
        msg = bot.send_message(call.message.chat.id, "Describe the character you want to talk to."
                                                     "For example: A young man who loves an active lifestyle, especially swimming, running and hiking, watches football and basketball on TV."
                                                     "Or just list topics of conversation")
        bot.register_next_step_handler(msg, setup_custom_persona)

def setup_custom_persona(message):
    openchat.setup_persona(message.chat.id, message.text)
    bot.send_message(message.chat.id, "Ok, let's talk")

@bot.message_handler(commands=['choose'])
def choose_persona(message):
    openchat.start()
    bot.send_message(message.chat.id, "Choose who you want to talk to", reply_markup=pers_markup())


@bot.message_handler(commands=['wiki'])  # TODO: meaning from wiki
def meaning_message(message):
    bot.send_message(message.chat.id, "Meaning of word from wiki. Not ready right now")


@bot.message_handler(commands=['tr'])  # TODO: translate to several lang
def translation_message(message):
    bot.send_message(message.chat.id, "Translation of word to several lang. Not ready right now")


@bot.message_handler(commands=['stat'])  # TODO: statistics
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
                     # "Bitcoin wallet\n"#TODO: add Bitcoin
                     # "\n\n"
                     # "*VISA*\n"
                     # "4374 6901 0038 9301\n\n"
                     "For all questions and suggestions, you can write to me\n"
                     "https://t.me/Scientist_Ft",
                     parse_mode='Markdown')


@bot.message_handler(content_types=['text'])
def message(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot_message = openchat.predict_message(message.from_user.id, message.text)
    bot.send_message(message.chat.id, bot_message)


@bot.message_handler(content_types=['audio'])
def audio_message(message):
    bot.send_message(message.chat.id, "Audio messages are not ready right now")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', action='store', type=str, help='Model name')
    parser.add_argument('--gpu', help='Run on gpu, otherwise on cpu', action="store_true")
    args = parser.parse_args()

    model = 'blender.small'
    device = 'cpu'
    if args.model:
        model = args.model
    if args.gpu:
        device = 'gpu'

    openchat = OpenChat(model='blender.small', device=device, environment='custom', maxlen=2048)

    bot.infinity_polling()
