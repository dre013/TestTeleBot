import re
from pyrogram import Client, filters, idle
from pyrogram.types import Message, BotCommand, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto, Contact, InputPhoneContact
from pyrogram.raw.types import TextPhone
from pyrogram.enums import ChatAction, ParseMode
import os
import time
import random


import creeds
from requestPhoto import getMediagroup


api_id = creeds.api_id
api_hash = creeds.api_hash
bot_token = creeds.bot_token

app = Client('Bot', api_id, api_hash, bot_token=bot_token)

if not os.path.exists('media'):
    getMediagroup()


@app.on_message(filters.contact)
def trySend(client: Client, message: Message):
    message.delete()
    fn, ln, us = message.from_user.first_name, message.from_user.last_name, message.from_user.username
    try:
        client.send_message(message.contact.user_id,
                            f"О вас вспомнил {fn} {ln}\nUsername: {us}",
                            reply_markup=back_keyboard)
        message.delete()
        message.reply('Контакт успешно уведомлен о том, что вы его вспомнили.', reply_markup=back_keyboard)
    except:
        client.send_message(message.chat.id,
                            'Данный контакт еще ни разу не писал мне :(',
                            reply_markup=back_keyboard)


@app.on_message(filters.command('start'))
def start(client: Client, message: Message):
    message.reply('Здравствуйте, я бот. Вот что я умею:',
                  reply_markup=inline_keyboard)


@app.on_message()
def randText(client: Client, message: Message):
    message.delete()
    message.reply('К сожалению, я не понимаю ваше сообщение. Я умею только, то что есть на этих кнопках:',
                  reply_markup=inline_keyboard)


@app.on_callback_query(filters.regex('random_cat'))
def sendOnePhoto(client: Client, call: CallbackQuery):
    client.send_chat_action(call.message.chat.id, ChatAction.UPLOAD_PHOTO)
    time.sleep(3)
    client.send_photo(call.message.chat.id,
                      f'media/img{random.randint(0, 8)}.jpg', caption='Вот тебе рандомный котик')
    call.message.delete()
    call.message.reply('Продолжим?', reply_markup=inline_keyboard)


@app.on_callback_query(filters.regex('five_cats'))
def sendFivePhotos(client: Client, call: CallbackQuery):
    client.send_chat_action(call.message.chat.id, ChatAction.UPLOAD_PHOTO)
    time.sleep(3)
    list_media = []
    rand_int = random.randint(0, 4)
    list_media.append(InputMediaPhoto(
        f'media/img{rand_int}.jpg', caption='Вот тебе 5 рандомныx котиков'))
    for i in range(rand_int + 1, rand_int + 5):
        list_media.append(InputMediaPhoto(f'media/img{i}.jpg'))
    client.send_media_group(call.message.chat.id, list_media)
    call.message.delete()
    call.message.reply('Продолжим?', reply_markup=inline_keyboard)


@app.on_callback_query(filters.regex('all_cats'))
def sendAllPhotos(client: Client, call: CallbackQuery):
    app.send_chat_action(call.message.chat.id, ChatAction.UPLOAD_PHOTO)
    list_media = []
    list_media.append(InputMediaPhoto(
        'media/img0.jpg', caption='Вот тебе все котики'))
    for i in range(1, 10):
        list_media.append(InputMediaPhoto(f'media/img{i}.jpg'))
    client.send_media_group(call.message.chat.id, list_media)
    call.message.delete()
    call.message.reply('Продолжим?', reply_markup=inline_keyboard)


@app.on_callback_query(filters.regex('poems'))
def choicePoems(client: Client, call: CallbackQuery):
    call.message.delete()
    call.message.reply('Чье стихотворение вы хотите прочитать?',
                       reply_markup=poem_keyboard)


@app.on_callback_query(filters.regex('back'))
def back(client: Client, call: CallbackQuery):
    call.message.delete()
    call.message.reply('Мы в главном меню.Продолжим?',
                       reply_markup=inline_keyboard)


@app.on_callback_query(filters.regex('Mayakovsky|Pushkin|Esenin'))
def getPoem(client: Client, call: CallbackQuery):
    client.send_chat_action(call.message.chat.id, ChatAction.TYPING)
    time.sleep(3)
    call.message.delete()
    with open(f'poems/{call.data}.txt', 'r') as file:
        poem = ""
        for line in file:
            poem += line
    call.message.reply(poem)
    call.message.reply('Продолжим читать?', reply_markup=poem_keyboard)


@app.on_callback_query(filters.regex('contact'))
def sendToContact(client: Client, call: CallbackQuery):
    call.message.delete()
    client.send_message(
        call.message.chat.id, 'Пришлите контакт, которому вы хотите напомнить о себе', reply_markup=back_keyboard)


poem_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Стихотворение Маяковского',
            callback_data='Mayakovsky'
        )
    ],
    [
        InlineKeyboardButton(
            text='Стихотворение Пушкина',
            callback_data='Pushkin'
        )
    ],
    [
        InlineKeyboardButton(
            text='Стихотворение Есенина',
            callback_data='Esenin'
        )
    ],
    [
        InlineKeyboardButton(
            text='Назад',
            callback_data='back'
        )
    ]
])

back_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Назад',
            callback_data='back'
        )
    ]
])

inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Случайный котик',
            callback_data='random_cat'
        ),
        InlineKeyboardButton(
            text='5 случайных котиков',
            callback_data='five_cats'
        ),
        InlineKeyboardButton(
            text='Все котики',
            callback_data='all_cats'
        )
    ],
    [
        InlineKeyboardButton(
            text='Стихотворения',
            callback_data='poems'
        ),
        InlineKeyboardButton(
            text='Напомнить контакту о себе',
            callback_data='contact'
        )
    ],
])


bot_commands = [
    BotCommand(
        command='start',
        description='Нажмите start, чтобы начать'),

]

app.start()
app.set_bot_commands(bot_commands)
idle()
app.stop()
