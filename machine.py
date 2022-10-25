from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import KeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3
from secret import TOKEN
# Выше импортируем всякие разные библиотеки

bot = Bot(token=TOKEN)  # Тут подключаем самого бота
storage = MemoryStorage()  # Хранилище для машины состояний
dp = Dispatcher(bot, storage=storage)
class Form2(StatesGroup):
    valute = State()


class Greeting(StatesGroup):  # Объявляем класс для машины состояний
    nickname = State()  # А это сами состояния
    time = State()
    city = State()


class Form(StatesGroup):
    otvet = State()


@dp.message_handler(state=Form2.valute)
async def valute(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3).add(  # Добавляем клавиатуру обратно
            KeyboardButton(text='Настроить время приветствия'),
            KeyboardButton(text='Настроить форму обращения'),
            KeyboardButton(text='Настроить город'),
            KeyboardButton(text='Настроить отображение блоков'),
            KeyboardButton(text='Настроить Выбор Валюты'))
        data['valute'] = message.text
        data['uid'] = message.from_user.id
        await message.answer(f'Валюты: {data["valute"]}\nВалюты успешно установлены!', reply_markup=keyboard)
        with sqlite3.connect('data.db', timeout=60) as connect:
            cursor = connect.cursor()
            cursor.execute("UPDATE settings SET valutes = ? WHERE uid = ? ", (data["valute"] ,data['uid'],))
        await state.finish()

@dp.message_handler(state=Greeting.time)  # Тут уже идёт обработка машиной состояний для смены времени
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3).add(  # Добавляем клавиатуру обратно
            KeyboardButton(text='Настроить время приветствия'),
            KeyboardButton(text='Настроить форму обращения'),
            KeyboardButton(text='Настроить город'),
            KeyboardButton(text='Настроить отображение блоков'),
            KeyboardButton(text='Настроить Выбор Валюты'))
        data['time'] = message.text  # Бот записывает в своё хранилище время, которое ввёл юзер
        data['uid'] = message.from_user.id  # Записываем id юзера туда же
        # Ниже отвечаем, что всё хорошо
        await message.answer(f'Время приветствий: {data["time"]}\nВремя успешно установлено!', reply_markup=keyboard)
        with sqlite3.connect('data.db', timeout=60) as connect:
            cursor = connect.cursor()
            cursor.execute("SELECT * FROM time WHERE uid = ? ", (data['uid'],))
            mass = cursor.fetchall()
            connect.commit()
        info = list(sum(mass, ()))
        if data['uid'] in info:  # Если есть, то:
            with sqlite3.connect('data.db', timeout=60) as connect:
                cursor = connect.cursor()
                cursor.execute("UPDATE time SET greeting_timeh = ? WHERE uid = ? ",
                               (data['time'], data['uid']))  # Обновляем время в бд
                connect.commit()

        else:  # Если нет, то заносим
            with sqlite3.connect('data.db', timeout=60) as connect:
                cursor = connect.cursor()
                cursor.execute("INSERT INTO time (greeting_timeh,uid) VALUES (?,?)", (data["time"], data["uid"]))
                connect.commit()
        await state.finish()  # Всё классно, завершаем состояние и бот теперь может принимать новые команды


@dp.message_handler(state=Greeting.nickname)  # Тут идёт опять обработка машиной состояний, но уже для обращения
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3).add(  # Добавляем клавиатуру обратно
            KeyboardButton(text='Настроить время приветствия'),
            KeyboardButton(text='Настроить форму обращения'),
            KeyboardButton(text='Настроить город'),
            KeyboardButton(text='Настроить отображение блоков'),
            KeyboardButton(text='Настроить Выбор Валюты'))
        data['nickname'] = message.text  # Бот записывает в своё хранилище обращение, которое ввёл юзер
        data['uid'] = message.from_user.id
        with sqlite3.connect('data.db', timeout=60) as connect:
            cursor = connect.cursor()
            cursor.execute("SELECT nickname FROM time WHERE uid = ? ", (data['uid'],))
            # Смотрим, есть ли в бд наш id
            massn = cursor.fetchall()
            connect.commit()
        infon = list(sum(massn, ()))
        if data['nickname'] in infon:  # Если есть, то:
            with sqlite3.connect('data.db', timeout=60) as connect:
                cursor = connect.cursor()
                cursor.execute("UPDATE time SET nickname = ? WHERE uid = ? ",
                               (data['nickname'], data['uid']))  # Обновляем ник в бд
                connect.commit()
        else:  # Если нет, то заносим
            with sqlite3.connect('data.db', timeout=60) as connect:
                cursor = connect.cursor()
                cursor.execute("UPDATE time SET nickname = ? WHERE uid = ?", (data["nickname"], data["uid"]))
                connect.commit()
        # Ниже отвечаем, что всё хорошо
        await message.answer(f'Форма обращения: {data["nickname"]}\n'
                             f'Форма обращений успешно установлена!', reply_markup=keyboard)
        await state.finish()  # Завершаем состояние и работаем дальше


@dp.message_handler(state=Greeting.city)  # Тут идёт опять обработка машиной состояний, но уже для обращения
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3).add(  # Добавляем клавиатуру обратно
            KeyboardButton(text='Настроить время приветствия'),
            KeyboardButton(text='Настроить форму обращения'),
            KeyboardButton(text='Настроить город'),
            KeyboardButton(text='Настроить отображение блоков'),
            KeyboardButton(text='Настроить Выбор Валюты'))
        data['city'] = message.text  # Бот записывает в своё хранилище обращение, которое ввёл юзер
        data['uid'] = message.from_user.id
        with sqlite3.connect('data.db', timeout=60) as connect:
            cursor = connect.cursor()
            # Смотрим, есть ли в бд наш id
            cursor.execute("SELECT city FROM time WHERE uid = ? ", (data['uid'],))
            massn = cursor.fetchall()
            connect.commit()
        infon = list(sum(massn, ()))
        if data['city'] in infon:  # Если есть, то:
            with sqlite3.connect('data.db', timeout=60) as connect:
                cursor = connect.cursor()
                cursor.execute("UPDATE time SET city = ? WHERE uid = ? ",
                               (data['city'], data['uid']))  # Обновляем ник в бд
                cursor.execute("UPDATE cache SET city = ? WHERE uid = ? ",
                               (data['city'], data['uid']))
                connect.commit()
        else:  # Если нет, то заносим
            with sqlite3.connect('data.db', timeout=60) as connect:
                cursor = connect.cursor()
                cursor.execute("UPDATE time SET city = ? WHERE uid = ? ", (data["city"], data["uid"]))
                cursor.execute("UPDATE cache SET city = ? WHERE uid = ? ", (data["city"], data["uid"]))
                connect.commit()
        # Ниже отвечаем, что всё хорошо
        await message.answer(f'Ваш город: {data["city"]}\n'
                             f'Город успешно установлен!', reply_markup=keyboard)
        await state.finish()  # Завершаем состояние и работаем дальше