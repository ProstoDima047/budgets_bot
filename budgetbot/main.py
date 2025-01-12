import telebot, pickle, atexit
from user import User, users
from conf import API_KEY, DATA

bot = telebot.TeleBot(API_KEY)

with open(DATA, 'rb') as fp:
    users = pickle.load(fp)

def save_users():
    for user in users:
        users[user].command_data = {}
        users[user].command = None
    with open(DATA, 'wb') as fp:
        pickle.dump(users, fp, protocol=pickle.HIGHEST_PROTOCOL)

def make_user(chat):
    if chat in users:
        return users[chat]
    user = User()
    user.chat = chat
    users[chat] = user
    return user

def setup(message):
    text = message.text
    user = make_user(message.chat.id)
    return (text, user)

@bot.message_handler(content_types=['text'])
def handle(message):
    text, user = setup(message)
    text = text.lstrip('/')
    msg_info = user.parse(text)
    if (msg_info.delete_users_message): 
        user.deletable_messages.append(message)
    if user.command == None:
        delete_messages(user)
    send_message(user, msg_info)

def delete_messages(user):
    if len(user.deletable_messages) > 0:
        for m in user.deletable_messages:
            bot.delete_message(m.chat.id, m.message_id)
        user.deletable_messages = []

def send_message(user, message_info): 
    msg = bot.send_message(user.chat, message_info.text, reply_markup=message_info.markup)
    if message_info.delete:
        user.deletable_messages.append(msg)

  
atexit.register(save_users)
bot.infinity_polling(skip_pending = True)