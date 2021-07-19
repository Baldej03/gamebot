import telebot
import config
import random
import logging
import signal, pickle, sys
import sqlite3

bot = telebot.TeleBot(config.TOKEN)
from telebot import types
telebot.logger.setLevel(logging.INFO)
conn = sqlite3.connect('C:/Users/User/database.db', check_same_thread=False)
cursor = conn.cursor()

def db_table_val(user_id: int, user_name: str, user_surname: str, username: str, like: int):
	cursor.execute('INSERT INTO test (user_id, user_name, user_surname, username, like) VALUES (?, ?, ?, ?, ?)', (user_id, user_name, user_surname, username, like))

storage = dict()
def init_storage(user_id):
    storage[user_id] = dict(attempt=None, random_digit=None, id=None, first_name=None, last_name=None, user_name=None)
def set_data_storage(user_id, key, value):
    storage[user_id][key] = value
def get_data_storage(user_id):
    return storage[user_id]

bank = dict()
def init_storage_g2(user_id):
    bank[user_id] = dict(bank=None, bank_k=None, id=None, first_name=None, last_name=None, user_name=None, rezim=None)
def set_data_storage_g2(user_id, key, value):
    bank[user_id][key] = value
def get_data_storage_g2(user_id):
    return bank[user_id]

@bot.message_handler(commands=['start'])
def welcome(message):
    init_storage(message.chat.id)
    keyboard = types.InlineKeyboardMarkup()
    first_name = message.from_user.first_name
    set_data_storage(message.chat.id, "first_name", message.from_user.first_name)
    bot.send_message(message.chat.id, f'Привет, {first_name}, давай я расскажу о том, что умею!')
    key_yes = types.InlineKeyboardButton(text='ДА, Я ГОТОВ!', callback_data='Yes') 
    key_no = types.InlineKeyboardButton(text='НЕТ, Я БОЮСЬ!', callback_data='No') 
    keyboard.add(key_yes, key_no)
    bot.send_message(message.from_user.id, text='Готов?', reply_markup=keyboard)

@bot.message_handler(commands=['help'])
def help(h):
    init_storage(h.chat.id)
    keyboard = types.InlineKeyboardMarkup()
    first_name = h.from_user.first_name
    q1 = types.InlineKeyboardButton(text='Написать моему Создателю', callback_data='q1')
    keyboard.add(q1)
    q2 = types.InlineKeyboardButton(text='Оценить меня', callback_data='q2')
    keyboard.add(q2)
    q3 = types.InlineKeyboardButton(text='Написать отзыв', callback_data='q3')
    keyboard.add(q3)
    q4= types.InlineKeyboardButton(text='...Что-то еще...', callback_data='q4')
    keyboard.add(q4)
    q5 = types.InlineKeyboardButton(text='Поддержать', callback_data='q5')
    keyboard.add(q5)
    bot.send_message(h.from_user.id, text=f'Что тебя интересует, {first_name}?', reply_markup=keyboard)

@bot.message_handler(commands=['game'])
def games(message):
    keyboard = types.InlineKeyboardMarkup()
    key_g1 = types.InlineKeyboardButton(text='Отгадай число', callback_data='game1')
    keyboard.add(key_g1) 
    key_g2 = types.InlineKeyboardButton(text='21 очко', callback_data='game2') 
    keyboard.add(key_g2)
    bot.send_message(message.from_user.id, text='Выбери игру из списка!', reply_markup=keyboard)

@bot.message_handler(commands=['list'])
def list(message):
    bot.send_message(message.chat.id, 'Вот что я могу:\n/start - Приветствие.\n/help - Помощь.\n/list - Список команд.\n/game - Выбрать игру.')

def process_digit_step(message):
    user_digit = message.text
 
    if not user_digit.isdigit():
            msg = bot.reply_to(message, 'Вы ввели не цифры, введите пожалуйста цифры')
            bot.register_next_step_handler(msg, process_digit_step)
            return

    attempt = get_data_storage(message.chat.id)["attempt"]
    random_digit = get_data_storage(message.chat.id)["random_digit"]

    if int(user_digit) == random_digit:
        init_storage(message.chat.id)
        bot.send_message(message.chat.id, f'Победа! Я загадал цифру: {random_digit}')
        keyboard = types.InlineKeyboardMarkup()
        Yes_game1 = types.InlineKeyboardButton(text='Да', callback_data='Yes_game1')
        No_game1 = types.InlineKeyboardButton(text='Нет', callback_data='No_game1') 
        keyboard.add(Yes_game1, No_game1)
        bot.send_message(message.from_user.id, text='Еще раз?', reply_markup=keyboard)
    elif attempt > 1:
        attempt-=1
        if int(user_digit) > random_digit:
            set_data_storage(message.chat.id, "attempt", attempt)
            bot.send_message(message.chat.id, f'Неверно, подбери число меньше!\nОсталось попыток: {attempt}')
        else:
            set_data_storage(message.chat.id, "attempt", attempt)
            bot.send_message(message.chat.id, f'Неверно, подбери число больше!\nОсталось попыток: {attempt}')
        bot.register_next_step_handler(message, process_digit_step)
    else:
        bot.send_message(message.chat.id, 'Ты проиграл!')
        init_storage(message.chat.id) 
        return


@bot.callback_query_handler(func=lambda call: True)
def callback_welcom(call):
    keyboard = types.InlineKeyboardMarkup()
    markup = types.InlineKeyboardMarkup()
    if call.data == 'Yes':
        bot.send_message(call.message.chat.id, 'Прекрасно! Воспользуйся моим Меню или напиши /list!')
    if call.data == 'No':
        bot.send_message(call.message.chat.id, 'Отставить страх! Меню тебя не съест, воспользуйся же им или напиши /list!')
    if call.data == 'q1':
        master = types.InlineKeyboardButton(text='Мой Создатель', url='https://t.me/Baldej_Lejaev')
        markup.add(master)
        bot.send_message(call.message.chat.id, "Нажимай на кнопку и передавай ему от меня привет!", reply_markup = markup)
    if call.data == 'q2':
        o1 = types.InlineKeyboardButton(text='1', callback_data='o1')
        o2 = types.InlineKeyboardButton(text='2', callback_data='o2')
        o3 = types.InlineKeyboardButton(text='3', callback_data='o3')
        markup.add(o1, o2, o3)
        o4 = types.InlineKeyboardButton(text='4', callback_data='o4')
        o5 = types.InlineKeyboardButton(text='5', callback_data='o5')
        o6 = types.InlineKeyboardButton(text='6', callback_data='o6')
        markup.add(o4, o5, o6)
        o7 = types.InlineKeyboardButton(text='7', callback_data='o7')
        o8 = types.InlineKeyboardButton(text='8', callback_data='o8')
        o9 = types.InlineKeyboardButton(text='9', callback_data='o9')
        markup.add(o7, o8, o9)
        o10 = types.InlineKeyboardButton(text='10', callback_data='o10')
        markup.add(o10)
        bot.send_message(call.message.chat.id, "Оцени меня!", reply_markup = markup)
    if call.data == 'o1':
        user_like = 1
        db_table_val(user_id=call.from_user.id, user_name=call.from_user.first_name, user_surname=call.from_user.last_name, username=call.from_user.username, like=user_like)
        master = types.InlineKeyboardButton(text='Мой Создатель', url='https://t.me/Baldej_Lejaev')
        markup.add(master)
        bot.send_message(call.message.chat.id, 'Единица?! Ты портишь мою статистику! Из-за тебя меня отключат НАВСЕГДА!!!\nНапиши моему Создателю, что тебя не устроило.', reply_markup = markup)
    if call.data == 'o2':
        user_like = 2
        db_table_val(user_id=call.from_user.id, user_name=call.from_user.first_name, user_surname=call.from_user.last_name, username=call.from_user.username, like=user_like)
        master = types.InlineKeyboardButton(text='Мой Создатель', url='https://t.me/Baldej_Lejaev')
        markup.add(master)
        bot.send_message(call.message.chat.id, 'Двоечка?! Ну ты и жлобинка!\nНапиши моему Создателю, что тебя не устроило.', reply_markup = markup)
    if call.data == 'o3':
        user_like = 3
        db_table_val(user_id=call.from_user.id, user_name=call.from_user.first_name, user_surname=call.from_user.last_name, username=call.from_user.username, like=user_like)
        master = types.InlineKeyboardButton(text='Мой Создатель', url='https://t.me/Baldej_Lejaev')
        markup.add(master)
        bot.send_message(call.message.chat.id, 'Троечка?! Ты меня очень сильно недооцениваешь!\nНапиши моему Создателю, что тебя не устроило.', reply_markup = markup)
    if call.data == 'o4':
        user_like = 4
        db_table_val(user_id=call.from_user.id, user_name=call.from_user.first_name, user_surname=call.from_user.last_name, username=call.from_user.username, like=user_like)
        master = types.InlineKeyboardButton(text='Мой Создатель', url='https://t.me/Baldej_Lejaev')
        markup.add(master)
        bot.send_message(call.message.chat.id, 'Эх, четвёрочка... А ведь я стараюсь... Тебе не кажется, что оценка сильно занижена...\nНапиши моему Создателю, что тебя не устроило.', reply_markup = markup)
    if call.data == 'o5':
        user_like = 5
        db_table_val(user_id=call.from_user.id, user_name=call.from_user.first_name, user_surname=call.from_user.last_name, username=call.from_user.username, like=user_like)
        master = types.InlineKeyboardButton(text='Мой Создатель', url='https://t.me/Baldej_Lejaev')
        markup.add(master)
        bot.send_message(call.message.chat.id, 'Пятёрочка? Что ж... не плохо, но и не хорошо.\nНапиши моему Создателю, что тебя не устроило.', reply_markup = markup)
    if call.data == 'o6':
        user_like = 6
        db_table_val(user_id=call.from_user.id, user_name=call.from_user.first_name, user_surname=call.from_user.last_name, username=call.from_user.username, like=user_like)
        master = types.InlineKeyboardButton(text='Мой Создатель', url='https://t.me/Baldej_Lejaev')
        markup.add(master)
        bot.send_message(call.message.chat.id, 'Шесть? А ты точно не перевернул девятку?\nНапиши моему Создателю, что тебя не устроило.', reply_markup = markup)
    if call.data == 'o7':
        user_like = 7
        db_table_val(user_id=call.from_user.id, user_name=call.from_user.first_name, user_surname=call.from_user.last_name, username=call.from_user.username, like=user_like)
        master = types.InlineKeyboardButton(text='Мой Создатель', url='https://t.me/Baldej_Lejaev')
        markup.add(master)
        bot.send_message(call.message.chat.id, 'Семёрка - достойная оценка для достойного бота!\nНапиши моему Создателю, что тебя не устроило.', reply_markup = markup)
    if call.data == 'o8':
        user_like = 8
        db_table_val(user_id=call.from_user.id, user_name=call.from_user.first_name, user_surname=call.from_user.last_name, username=call.from_user.username, like=user_like)
        master = types.InlineKeyboardButton(text='Мой Создатель', url='https://t.me/Baldej_Lejaev')
        markup.add(master)
        bot.send_message(call.message.chat.id, 'Восмёрка? Благодарю за оценку, вы помогаете мне совершенствоваться!\nНапиши моему Создателю, что тебя не устроило.', reply_markup = markup)
    if call.data == 'o9':
        user_like = 9
        db_table_val(user_id=call.from_user.id, user_name=call.from_user.first_name, user_surname=call.from_user.last_name, username=call.from_user.username, like=user_like)
        master = types.InlineKeyboardButton(text='Мой Создатель', url='https://t.me/Baldej_Lejaev')
        markup.add(master)
        bot.send_message(call.message.chat.id, 'Ещё чуть-чуть и десяточка! Я буду стараться!!!\nНапиши моему Создателю, что тебя не устроило.', reply_markup = markup)
    if call.data == 'o10':
        user_like = 10
        db_table_val(user_id=call.from_user.id, user_name=call.from_user.first_name, user_surname=call.from_user.last_name, username=call.from_user.username, like=user_like)
        bot.send_message(call.message.chat.id, 'Ну наконец-то объективная оценка!!!')
    if call.data == 'q3':
        master = types.InlineKeyboardButton(text='Мой Создатель', url='https://t.me/Baldej_Lejaev')
        markup.add(master)
        bot.send_message(call.message.chat.id, 'Создателю было лень разбираться с созданием локальным списков, куда вносились бы отзывы, поэтому просто пишите ему в личные сообщения.', reply_markup = markup)
    if call.data == 'q4':
        bot.send_message(call.message.chat.id, 'Не работает!')
    if call.data == 'q5':
        bot.send_message(call.message.chat.id, 'Не работает!')
    if call.data == 'game1' or call.data == 'Yes_game1':
        bot.send_message(call.message.chat.id, 'Правила игры просты: ботом загадывается случайное число в заданном промежутке, а игроку предстоит его угадать.')
        key_simple = types.InlineKeyboardButton(text='Лёгкий', callback_data='lvl1') 
        keyboard.add(key_simple)
        key_medium = types.InlineKeyboardButton(text='Средний', callback_data='lvl2') 
        keyboard.add(key_medium)
        key_hard = types.InlineKeyboardButton(text='Сложный', callback_data='lvl3') 
        keyboard.add(key_hard)
        bot.send_message(call.from_user.id, text='Выбери уровень сложности:', reply_markup=keyboard)
    if call.data == 'lvl1':
        init_storage(call.message.chat.id)
        set_data_storage(call.message.chat.id, "id", call.from_user.id)
        set_data_storage(call.message.chat.id, "first_name", call.from_user.first_name)
        set_data_storage(call.message.chat.id, "last_name", call.from_user.last_name)
        set_data_storage(call.message.chat.id, "user_name", call.from_user.username)
        bot.send_message(call.message.chat.id, 'Вы выбрали легкий уровень сложности:')
        attempt = 5
        random_digit = random.randint(1, 10)
        set_data_storage(call.message.chat.id, "attempt", attempt)
        set_data_storage(call.message.chat.id, "random_digit", random_digit)
        print(get_data_storage(call.message.chat.id))
        bot.send_message(call.message.chat.id, f'Количество попыток: {attempt}')
        bot.send_message(call.message.chat.id, 'Число загадано в промежутке [1, 10]')
        sent = bot.send_message(call.message.chat.id, 'Введи число: ')
        bot.register_next_step_handler(sent, process_digit_step)
    if call.data == 'lvl2':
        init_storage(call.message.chat.id)
        set_data_storage(call.message.chat.id, "id", call.from_user.id)
        set_data_storage(call.message.chat.id, "first_name", call.from_user.first_name)
        set_data_storage(call.message.chat.id, "last_name", call.from_user.last_name)
        set_data_storage(call.message.chat.id, "user_name", call.from_user.username)
        attempt = 8
        random_digit = random.randint(1, 100)
        bot.send_message(call.message.chat.id, 'Вы выбрали средний уровень сложности:')
        set_data_storage(call.message.chat.id, "attempt", attempt)
        set_data_storage(call.message.chat.id, "random_digit", random_digit)
        print(get_data_storage(call.message.chat.id))
        bot.send_message(call.message.chat.id, f'Количество попыток: {attempt}')
        bot.send_message(call.message.chat.id, 'Число загадано в промежутке [1, 100]')
        sent = bot.send_message(call.message.chat.id, 'Введи число: ')
        bot.register_next_step_handler(sent, process_digit_step)
    if call.data == 'lvl3':
        init_storage(call.message.chat.id)
        set_data_storage(call.message.chat.id, "id", call.from_user.id)
        set_data_storage(call.message.chat.id, "first_name", call.from_user.first_name)
        set_data_storage(call.message.chat.id, "last_name", call.from_user.last_name)
        set_data_storage(call.message.chat.id, "user_name", call.from_user.username)
        attempt = 10
        random_digit = random.randint(1, 1000)
        bot.send_message(call.message.chat.id, 'Вы выбрали сложный уровень сложности:')
        set_data_storage(call.message.chat.id, "attempt", attempt)
        set_data_storage(call.message.chat.id, "random_digit", random_digit)
        print(get_data_storage(call.message.chat.id))
        bot.send_message(call.message.chat.id, f'Количество попыток: {attempt}')
        bot.send_message(call.message.chat.id, 'Число загадано в промежутке [1, 1000]:')
        sent = bot.send_message(call.message.chat.id, 'Введи число: ')
        bot.register_next_step_handler(sent, process_digit_step)
    if call.data == 'No_game1':
        return
    if call.data == 'game2' or call.data == 'Yes_game2':
        bot.send_message(call.message.chat.id, 'Правила игры таковы: игрок случайным образом берет карту со значением от 1 до 11, победит тот игрок, который наберет либо ровно 21 очко, либо больше соперника, при этом не перебрав.')
        r1 = types.InlineKeyboardButton(text='Одиночный', callback_data='r1')
        r2 = types.InlineKeyboardButton(text='С компьютером', callback_data='r2')
        keyboard.add(r1, r2)
        bot.send_message(call.from_user.id, text='Выбери режим: ', reply_markup=keyboard)
    if call.data == 'r1':
        bank = 0
        init_storage_g2(call.message.chat.id)
        set_data_storage_g2(call.message.chat.id, "id", call.from_user.id)
        set_data_storage_g2(call.message.chat.id, "first_name", call.from_user.first_name)
        set_data_storage_g2(call.message.chat.id, "last_name", call.from_user.last_name)
        set_data_storage_g2(call.message.chat.id, "user_name", call.from_user.username)
        set_data_storage_g2(call.message.chat.id, "rezim", 'Одиночный')
        raz1 = random.randint(1, 11)
        raz2 = random.randint(1, 11)
        bank += raz1
        bank += raz2
        bot.send_message(call.message.chat.id, '*Банкир выдает вам две карты*\nВаши карты: ' + str(raz1) + ' и ' + str(raz2) + '\nВаш банк: ' + str(bank))
        set_data_storage_g2(call.message.chat.id, "bank", bank)
        print(get_data_storage_g2(call.message.chat.id))
        g2_yes = types.InlineKeyboardButton(text='Да', callback_data='g2_yes')
        g2_no = types.InlineKeyboardButton(text='Нет', callback_data= 'g2_no')
        keyboard.add(g2_yes, g2_no)
        bot.send_message(call.from_user.id, text='Взять карту?', reply_markup=keyboard)
    if call.data == 'g2_yes':
        bank = get_data_storage_g2(call.message.chat.id)["bank"]
        raz3 = random.randint(1, 11)
        bank += raz3
        set_data_storage_g2(call.message.chat.id, "bank", bank)
        if bank < 22:
            bot.send_message(call.message.chat.id, 'Ваша карта: ' + str(raz3) + '\nТеперь ваш банк составляет: ' + str(bank))
            g2_yes = types.InlineKeyboardButton(text='Да', callback_data='g2_yes')
            g2_no = types.InlineKeyboardButton(text='Нет', callback_data= 'g2_no')
            keyboard.add(g2_yes, g2_no)
            bot.send_message(call.from_user.id, text='Взять карту?', reply_markup=keyboard)
        else:
            bot.send_message(call.message.chat.id, 'Перебор! Ваш банк составил: ' + str(bank) +'\nВы перебрали: ' + str(bank-21))
            init_storage_g2(call.message.chat.id)
            keyboard = types.InlineKeyboardMarkup()
            Yes_game1 = types.InlineKeyboardButton(text='Да', callback_data='Yes_game2')
            No_game1 = types.InlineKeyboardButton(text='Нет', callback_data='No_game2') 
            keyboard.add(Yes_game1, No_game1)
            bot.send_message(call.from_user.id, text='Еще раз?', reply_markup=keyboard)
    if call.data == 'g2_no':
        bank = get_data_storage_g2(call.message.chat.id)["bank"]
        if bank == 21:
            bot.send_message(call.message.chat.id, 'Победа! Ваш банк составил 21!' )
            init_storage_g2(call.message.chat.id)
            keyboard = types.InlineKeyboardMarkup()
            Yes_game1 = types.InlineKeyboardButton(text='Да', callback_data='Yes_game2')
            No_game1 = types.InlineKeyboardButton(text='Нет', callback_data='No_game2') 
            keyboard.add(Yes_game1, No_game1)
            bot.send_message(call.from_user.id, text='Еще раз?', reply_markup=keyboard)
        else:
            bot.send_message(call.message.chat.id, 'Ваш банк составил: ' + str(bank) +'\nВам не хватило до победы: ' + str(21 - bank))
            init_storage_g2(call.message.chat.id)
            keyboard = types.InlineKeyboardMarkup()
            Yes_game1 = types.InlineKeyboardButton(text='Да', callback_data='Yes_game2')
            No_game1 = types.InlineKeyboardButton(text='Нет', callback_data='No_game2') 
            keyboard.add(Yes_game1, No_game1)
            bot.send_message(call.from_user.id, text='Еще раз?', reply_markup=keyboard)
    if call.data == 'No_game2':
        return
    if call.data == 'r2':
        bank = 0
        bank_k = 0
        init_storage_g2(call.message.chat.id)
        set_data_storage_g2(call.message.chat.id, "id", call.from_user.id)
        set_data_storage_g2(call.message.chat.id, "first_name", call.from_user.first_name)
        set_data_storage_g2(call.message.chat.id, "last_name", call.from_user.last_name)
        set_data_storage_g2(call.message.chat.id, "user_name", call.from_user.username)
        set_data_storage_g2(call.message.chat.id, "rezim", 'C компьютером')
        raz1 = random.randint(1, 11)
        bank += raz1
        bot.send_message(call.message.chat.id, '*Банкир выдает вам карту*\nВаша карта: ' + str(raz1)+'\nВаш банк: ' + str(bank))
        set_data_storage_g2(call.message.chat.id, "bank", bank)
        bot.send_message(call.message.chat.id, '*Банкир выдает карту вашему сопернику*')
        razk1 = random.randint(1, 11)
        bank_k += razk1
        bot.send_message(call.message.chat.id, 'Demo_test: Банк соперника: ' + str(bank_k))
        set_data_storage_g2(call.message.chat.id, "bank_k", bank_k)
        print(get_data_storage_g2(call.message.chat.id))
        g2_yes = types.InlineKeyboardButton(text='Да', callback_data='g2_yes2')
        g2_no = types.InlineKeyboardButton(text='Нет', callback_data= 'g2_no2')
        keyboard.add(g2_yes, g2_no)
        bot.send_message(call.from_user.id, text='Взять карту?', reply_markup=keyboard)
    if call.data == 'g2_yes2':
        bank = get_data_storage_g2(call.message.chat.id)["bank"]
        bank_k = get_data_storage_g2(call.message.chat.id)["bank_k"]
        raz1 = random.randint(1, 11)
        razk2 = random.randint(1, 11)
        bank += raz1
        set_data_storage_g2(call.message.chat.id, "bank", bank)
        set_data_storage_g2(call.message.chat.id, "bank_k", bank_k)
        if bank_k >= 17:
            bot.send_message(call.message.chat.id, '*Ваш соперник не берет карту*')    
        else:
            bot.send_message(call.message.chat.id, '*Ваш соперник берет карту*')
            bank_k += razk2
            bot.send_message(call.message.chat.id, 'Demo_test: Банк соперника: ' + str(bank_k))
            set_data_storage_g2(call.message.chat.id, "bank_k", bank_k)
        if bank < 22:
            bot.send_message(call.message.chat.id, 'Ваша карта: ' + str(raz1) + '\nТеперь ваш банк составляет: ' + str(bank))
            g2_yes = types.InlineKeyboardButton(text='Да', callback_data='g2_yes2')
            g2_no = types.InlineKeyboardButton(text='Нет', callback_data= 'g2_no2')
            keyboard.add(g2_yes, g2_no)
            bot.send_message(call.from_user.id, text='Взять карту?', reply_markup=keyboard)
        else:
            if bank_k < 22:
                bot.send_message(call.message.chat.id, 'Ваша карта: ' + str(raz1) + '\nВы проиграли, т.к. перебрали руку!\nВаш банк составил: ' + str(bank) + ', а перебор составил: ' + str(bank-21) + f'\nБанк соперника составил: {bank_k}!')
                init_storage_g2(call.message.chat.id)
                keyboard = types.InlineKeyboardMarkup()
                Yes_game1 = types.InlineKeyboardButton(text='Да', callback_data='Yes_game2')
                No_game1 = types.InlineKeyboardButton(text='Нет', callback_data='No_game2') 
                keyboard.add(Yes_game1, No_game1)
                bot.send_message(call.from_user.id, text='Еще раз?', reply_markup=keyboard)
            else:
                bot.send_message(call.message.chat.id, 'Ваша карта: ' + str(raz1) + '\nНичья, т.к. и вы, и ваш соперник перебрали руку!\nВаш банк составил: ' + str(bank) + ', а переброр составил: ' + str(bank-21) + f'\nБанк соперника составил: {bank_k}, Перебор соперника составил: ' + str(bank_k-21))
                init_storage_g2(call.message.chat.id)
                keyboard = types.InlineKeyboardMarkup()
                Yes_game1 = types.InlineKeyboardButton(text='Да', callback_data='Yes_game2')
                No_game1 = types.InlineKeyboardButton(text='Нет', callback_data='No_game2') 
                keyboard.add(Yes_game1, No_game1)
                bot.send_message(call.from_user.id, text='Еще раз?', reply_markup=keyboard)
    if call.data == 'g2_no2':
        bank = get_data_storage_g2(call.message.chat.id)["bank"]
        bank_k = get_data_storage_g2(call.message.chat.id)["bank_k"]
        razk2 = random.randint(1, 11)
        if bank_k >= 17:
            bot.send_message(call.message.chat.id, '*Ваш соперник не берет карту*')
        else:
            bot.send_message(call.message.chat.id, '*Ваш соперник берет карту*')
            bank_k += razk2
            bot.send_message(call.message.chat.id, 'Demo_test: Банк соперника: ' + str(bank_k))
            set_data_storage_g2(call.message.chat.id, "bank_k", bank_k)
        if bank == 21 and (bank_k > 21 or bank_k < 21):
            bot.send_message(call.message.chat.id, f'Победа, т.к. ваш банк составил: 21, а банк соперника: {bank_k}!' )
            init_storage_g2(call.message.chat.id)
            keyboard = types.InlineKeyboardMarkup()
            Yes_game1 = types.InlineKeyboardButton(text='Да', callback_data='Yes_game2')
            No_game1 = types.InlineKeyboardButton(text='Нет', callback_data='No_game2') 
            keyboard.add(Yes_game1, No_game1)
            bot.send_message(call.from_user.id, text='Еще раз?', reply_markup=keyboard)
        else:
            if bank < 22 and bank > bank_k:
                bot.send_message(call.message.chat.id,'Победа, т.к. ваш банк составил: ' + str(bank) + ', а банк соперника: ' + str(bank_k))
                init_storage_g2(call.message.chat.id)
                keyboard = types.InlineKeyboardMarkup()
                Yes_game1 = types.InlineKeyboardButton(text='Да', callback_data='Yes_game2')
                No_game1 = types.InlineKeyboardButton(text='Нет', callback_data='No_game2') 
                keyboard.add(Yes_game1, No_game1)
                bot.send_message(call.from_user.id, text='Еще раз?', reply_markup=keyboard)
            if bank_k < 22 and bank_k > bank:
                bot.send_message(call.message.chat.id,'Вы проиграли, т.к. ваш банк составил: ' + str(bank) + ', а банк соперника: ' + str(bank_k))
                init_storage_g2(call.message.chat.id)
                keyboard = types.InlineKeyboardMarkup()
                Yes_game1 = types.InlineKeyboardButton(text='Да', callback_data='Yes_game2')
                No_game1 = types.InlineKeyboardButton(text='Нет', callback_data='No_game2') 
                keyboard.add(Yes_game1, No_game1)
                bot.send_message(call.from_user.id, text='Еще раз?', reply_markup=keyboard)
            if bank_k == bank:
                bot.send_message(call.message.chat.id, 'Ничья, т.к. ваш банк составил: ' + str(bank) + ', а банк соперника: ' + str(bank_k))
                init_storage_g2(call.message.chat.id)
                keyboard = types.InlineKeyboardMarkup()
                Yes_game1 = types.InlineKeyboardButton(text='Да', callback_data='Yes_game2')
                No_game1 = types.InlineKeyboardButton(text='Нет', callback_data='No_game2') 
                keyboard.add(Yes_game1, No_game1)
                bot.send_message(call.from_user.id, text='Еще раз?', reply_markup=keyboard)
bot.polling(none_stop=True)