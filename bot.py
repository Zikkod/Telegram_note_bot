import telebot
from telebot import types
from telebot import util
from db import *

bot = telebot.TeleBot('Your token')

connection1 = create_connection("notes.sqlite")
connection2 = create_connection("nums.sqlite")
connection3 = create_connection("names.sqlite")

create_table1(connection1)
create_table2(connection2)
create_table3(connection3)

@bot.message_handler(commands=["start"])
def start(m, res=False):
    startKBoard = types.ReplyKeyboardMarkup(row_width=1)
    show_notes = types.KeyboardButton(text="Посмотреть все заметки")
    show_certain_note = types.KeyboardButton(text="Посмотреть определённую заметку")
    add_note = types.KeyboardButton(text="Добавить заметку")
    delete_note = types.KeyboardButton(text="Удалить заметку")
    startKBoard.add(show_notes, show_certain_note, add_note, delete_note)
    bot.send_message(m.chat.id, "Приветствую тебя. Я бот для хранения заметок. Пользуясь мной, запрещено нарушать законы РФ."
                                "Продолжая пользоваться мной, вы соглашаетесь с этими правилами", reply_markup=startKBoard)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text.lower() == "посмотреть все заметки":
        notes = show_notes(connection1, message.from_user.id)
        splitted_text = util.smart_split(notes, chars_per_string=3000)
        for text in splitted_text:
            bot.send_message(message.chat.id, text)

    elif message.text.lower() == "посмотреть определённую заметку":
        choiceKBoard = types.ReplyKeyboardMarkup(row_width=1)
        btn_id = types.KeyboardButton(text="id")
        btn_name = types.KeyboardButton(text="Название")
        choiceKBoard.add(btn_id, btn_name)
        msg = bot.send_message(message.chat.id, f'Найти заметку по id или названию?', reply_markup=choiceKBoard)
        bot.register_next_step_handler(msg, search_id_or_name)

    elif message.text.lower() == "добавить заметку":
        msg = bot.send_message(message.chat.id, 'Введите название заметки', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, enter_name)

    elif message.text.lower() == "удалить заметку":
        choiceKBoard = types.ReplyKeyboardMarkup(row_width=1)
        btn_id = types.KeyboardButton(text="id")
        btn_name = types.KeyboardButton(text="Название")
        choiceKBoard.add(btn_id, btn_name)
        msg = bot.send_message(message.chat.id, 'Удалить заметку по id или названию?', reply_markup=choiceKBoard)
        bot.register_next_step_handler(msg, delete_id_or_name)


def enter_name(message):
    save_name(message.text, message.from_user.id, connection3)
    msg = bot.send_message(message.chat.id, 'Введите текст заметки', reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, enter_note_text)


def enter_note_text(message):
    save_note_text(message.text, message.from_user.id, connection3)
    text = add_note(connection1, connection2, connection3, message.from_user.id)
    startKBoard = types.ReplyKeyboardMarkup(row_width=1)
    show_notes = types.KeyboardButton(text="Посмотреть все заметки")
    show_certain_note = types.KeyboardButton(text="Посмотреть определённую заметку")
    add_note_btn = types.KeyboardButton(text="Добавить заметку")
    delete_note = types.KeyboardButton(text="Удалить заметку")
    startKBoard.add(show_notes, show_certain_note, add_note_btn, delete_note)
    bot.send_message(message.chat.id, text, reply_markup=startKBoard)



def delete_id_or_name(message):
    if message.text.lower() == "id":
        msg = bot.send_message(message.chat.id, 'Введите id заметки', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, delete_id)
    elif message.text.lower() == "название":
        msg = bot.send_message(message.chat.id, 'Введите название заметки', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, delete_name)
    else:
        choiceKBoard = types.ReplyKeyboardMarkup(row_width=1)
        btn_id = types.KeyboardButton(text="id")
        btn_name = types.KeyboardButton(text="Название")
        choiceKBoard.add(btn_id, btn_name)
        msg = bot.send_message(message.chat.id, f'Удалить заметку по id или названию?', reply_markup=choiceKBoard)
        bot.register_next_step_handler(msg, search_id_or_name)


def delete_id(message):
    if is_int(message.text):
        msg = delete_note_id(message.from_user.id, message.text, connection1, connection2)
        startKBoard = types.ReplyKeyboardMarkup(row_width=1)
        show_notes = types.KeyboardButton(text="Посмотреть все заметки")
        show_certain_note = types.KeyboardButton(text="Посмотреть определённую заметку")
        add_note = types.KeyboardButton(text="Добавить заметку")
        delete_note = types.KeyboardButton(text="Удалить заметку")
        startKBoard.add(show_notes, show_certain_note, add_note, delete_note)
        bot.send_message(message.chat.id, msg, reply_markup=startKBoard)
    else:
        msg = bot.send_message(message.chat.id, 'Введёное значение не является числом')
        bot.register_next_step_handler(msg, delete_id)


def delete_name(message):
    msg = delete_note_name(message.from_user.id, message.text, connection1, connection2)
    startKBoard = types.ReplyKeyboardMarkup(row_width=1)
    show_notes = types.KeyboardButton(text="Посмотреть все заметки")
    show_certain_note = types.KeyboardButton(text="Посмотреть определённую заметку")
    add_note = types.KeyboardButton(text="Добавить заметку")
    delete_note = types.KeyboardButton(text="Удалить заметку")
    startKBoard.add(show_notes, show_certain_note, add_note, delete_note)
    bot.send_message(message.chat.id, msg, reply_markup=startKBoard)


def search_id_or_name(message):
    if message.text.lower() == "id":
        msg = bot.send_message(message.chat.id, 'Введите id заметки', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, search_id)
    elif message.text.lower() == "название":
        msg = bot.send_message(message.chat.id, 'Введите название заметки', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, search_name)
    else:
        choiceKBoard = types.ReplyKeyboardMarkup(row_width=1)
        btn_id = types.KeyboardButton(text="id")
        btn_name = types.KeyboardButton(text="Название")
        choiceKBoard.add(btn_id, btn_name)
        msg = bot.send_message(message.chat.id, f'Найти заметку по id или названию?', reply_markup=choiceKBoard)
        bot.register_next_step_handler(msg, search_id_or_name)


def search_id(message):
    if is_int(message.text):
        startKBoard = types.ReplyKeyboardMarkup(row_width=1)
        show_notes = types.KeyboardButton(text="Посмотреть все заметки")
        show_certain_note = types.KeyboardButton(text="Посмотреть определённую заметку")
        add_note = types.KeyboardButton(text="Добавить заметку")
        delete_note = types.KeyboardButton(text="Удалить заметку")
        startKBoard.add(show_notes, show_certain_note, add_note, delete_note)
        msg = show_certain_note_id(connection1, message.from_user.id, message.text)
        bot.send_message(message.chat.id, msg, reply_markup=startKBoard)
    else:
        msg = bot.send_message(message.chat.id, 'Введёное значение не является числом')
        bot.register_next_step_handler(msg, search_id)


def search_name(message):
    notes = show_certain_note_name(connection1, message.from_user.id, message.text)
    splitted_text = util.smart_split(notes, chars_per_string=3000)
    startKBoard = types.ReplyKeyboardMarkup(row_width=1)
    show_notes = types.KeyboardButton(text="Посмотреть все заметки")
    show_certain_note = types.KeyboardButton(text="Посмотреть определённую заметку")
    add_note = types.KeyboardButton(text="Добавить заметку")
    delete_note = types.KeyboardButton(text="Удалить заметку")
    startKBoard.add(show_notes, show_certain_note, add_note, delete_note)
    for text in splitted_text:
        bot.send_message(message.chat.id, text, reply_markup=startKBoard)


#bot.polling(none_stop=True, interval=0)
bot.polling()
