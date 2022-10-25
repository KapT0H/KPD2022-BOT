import datetime
import sqlite3
from datetime import *
from machine import *
import requests
import bs4
import asyncio
from aiogram import executor


async def run():
    with sqlite3.connect('data.db', timeout=60) as connect:
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM time")
        results = cursor.fetchall()
    fres = int(len(results))
    connect.commit()
    while True:
        with sqlite3.connect('data.db', timeout=60) as connect:
            cursor.execute("SELECT greeting_timeh FROM time WHERE id = ?", [fres])
            resultss = cursor.fetchall()
            infon = list(sum(resultss, ()))
            infonn = str(infon).replace("[", "").replace("'", "").replace("]", "")
            connect.commit()

        if infonn == datetime.now().strftime('%H:%M') and fres != 0:
            with sqlite3.connect('data.db', timeout=60) as connect:
                cursor.execute('SELECT uid FROM time WHERE id = ?', [fres])
                resultsss = cursor.fetchall()
                connect.commit()
                infonnn = list(sum(resultsss, ()))
                uid = str(infonnn).replace("[", "").replace("'", "").replace("]", "")
                print(fres)
                print(uid)
                now = datetime.now()  # Узнаем какое сейчас время вообще
                greet = 'Здравствуйте'  # Если что-то пойдет не так, то будет обращение просто "Здравствуйте, ..."
                if now.hour > 4 and now.hour <= 12:  # Если утро
                    greet = 'Доброе утро'  # Желаем доброго утра
                if now.hour > 12 and now.hour <= 16:  # Если день
                    greet = 'Добрый день'  # Желаем доброго дня
                if now.hour > 16 and now.hour <= 24:  # Если вечер
                    greet = 'Добрый вечер'  # Желаем доброго вечера
                if now.hour >= 0 and now.hour <= 4:  # Если ночь
                    greet = 'Доброй ночи'  # Желаем доброй ночи

            with sqlite3.connect('data.db', timeout=60) as connect:
                cursor = connect.cursor()
                # Вытаскиваем форму обращения из бд
                cursor.execute("SELECT nickname FROM time WHERE uid = ?", [uid])
                massnnn = cursor.fetchall()  # Отправляем запрос в бд
                infooon = list(sum(massnnn, ()))  # Ну тут опять этот костыль, ладно
                connect.commit()  # Завершаем работу с бд

                # Метод для получения курса валюты
            with sqlite3.connect('data.db', timeout=60) as connect:
                cursor = connect.cursor()
                cursor.execute("SELECT valutes FROM settings WHERE uid = ?", (uid,))
                valutes = list(sum(cursor.fetchall(), ()))
                a = "".join(valutes[0])
                b = a.replace(" ", "\n")
                c = b.split("\n")
                l = len(c)
                string = ""
                while l != 0:
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                                      'Chrome/80.0.3987.149 Safari/537.36'}
                    curs = f'https://www.google.com/search?client=opera-gx&q=курс+{c[l - 1]}&sourceid=opera&ie=UTF-8&oe=UTF-8'
                    full_page = requests.get(curs, headers=headers)
                    soup = bs4.BeautifulSoup(full_page.content, 'html.parser')
                    convertt = soup.findAll("span", {"class": "DFlfde SwHCTb", "data-precision": 2})
                    a = convertt[0].text
                    string = string + "1 " + c[l-1] + " " + a + " " + "₽" + "\n"
                    print(string)
                    l -= 1
                with sqlite3.connect('data.db', timeout=60) as connect:
                    cursor = connect.cursor()
                    # Берем из бд город, который указал юзер
                    cursor.execute("SELECT city FROM time WHERE uid = ?", [uid, ])
                    cursor.execute("UPDATE valute SET valutes = ? WHERE uid = ?", (str(string), uid,))
                    massss = cursor.fetchall()  # Выполнили запрос, всё круто
                    connect.commit()
                infonn = list(sum(massss, ()))  # Опять костыль)
                city = str(infonn).replace("[", "").replace("'", "").replace("]",
                                                                             "")  # Делаем чтоб красиво выводило из бд
                # Ссылка на гуголь откуда брать инфу (найти погоду можно почти на любой город)
                weather = f"https://www.google.ru/search?q=погода+{city}&newwindow=1&sxsrf=ALiCzsaVw67q9ZQh0QquKLiOnip6RK2B" \
                          f"-Q%3A1661270668674&ei=jPoEY-faKJGyrgSRsZKABg&ved=0ahUKEwjn0NPAq935AhURmYsKHZGYBGAQ4dUDCA0&uact=5&" \
                          f"oq=погода+рязань&gs_lcp=Cgdnd3Mtd2l6EAMyDAgjECcQnQIQRhCAAjIFCAAQgAQyBQgAEIAEMggIABCABBCxAzIFCAAQg" \
                          f"AQyCwgAEIAEELEDEIMBMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDoICAAQsQMQgwE6EQguEIAEELEDEIMBEMcBENEDOgc" \
                          f"IIxAnEJ0COgQIIxAnOhAILhCxAxCDARDHARDRAxBDOhAIABCABBCHAhCxAxCDARAUOg0IABCxAxCDARDJAxBDOgUIABCSAzoECA" \
                          f"AQQzoKCAAQgAQQhwIQFEoECEEYAEoECEYYAFAAWMMVYJkXaABwAXgAgAGbBYgB4wySAQgxMS4xLjUtMZgBAKABAcABAQ&sclient" \
                          f"=gws-wiz"
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/80.0.3987.149 Safari/537.36'}

                # Парсим всю страницу
                full_page = requests.get(weather, headers=headers)
                # Разбираем через BeautifulSoup
                soup = bs4.BeautifulSoup(full_page.content, 'html.parser')
                # Получаем нужное для нас значение и возвращаем его
                convert_temp = soup.findAll("span", {"class": "wob_t q8U8x", "style": "display:inline"})  # Температура
                convert_vo = soup.findAll("span", {"id": "wob_pp"})  # Вероятность осадков
                convert_vl = soup.findAll("span", {"id": "wob_hm"})  # Влажность
                convert_spd = soup.findAll("span", {"class": "wob_t", "id": "wob_ws"})  # Скорость ветра
                convert_wth = soup.findAll("span", {"id": "wob_dc"})  # ПОГОДА!
                with sqlite3.connect('data.db', timeout=60) as connect:
                    cursor = connect.cursor()
                    # Берем форму обращения к юзеру из бд
                    cursor.execute("SELECT nickname FROM time WHERE uid = ?", (uid,))
                    massn = cursor.fetchall()  # Отправили запрос в бд
                    connect.commit()
                infon = list(sum(massn, ()))  # Опять тот же самый костыль, будь ты проклят sqlite!!!
                otvett = (
                        str(infon).replace("[", "").replace("'", "").replace("]", "") + f', Погода в {city}:\n' +
                        convert_temp[
                            0].text + " °C\n" + 'Вероятность осадков: ' + convert_vo[
                            0].text + "\n" + 'Влажность: ' + convert_vl[0].text + "\n" + 'Ветер: ' + convert_spd[
                            0].text + "\n" +
                        convert_wth[
                            0].text)
            # Отправили юзеру сообщение
            with sqlite3.connect('data.db', timeout=60) as connect:
                cursor = connect.cursor()
                cursor.execute("SELECT weather FROM cache WHERE uid = ? ", (uid,))  # Смотрим, есть ли в бд наш id
                masssssn = cursor.fetchall()
                infonn = list(sum(masssssn, ()))
                connect.commit()
            if otvett in infonn:  # Если есть, то:
                with sqlite3.connect('data.db', timeout=60) as connect:
                    cursor = connect.cursor()
                    cursor.execute("UPDATE cache SET weather = ? WHERE uid = ? ",
                                   (otvett, uid))  # Обновляем ник в бд
                    connect.commit()
            else:
                with sqlite3.connect('data.db', timeout=60) as connect:
                    cursor = connect.cursor()
                    cursor.execute("UPDATE cache SET weather = ? WHERE uid = ? ",
                                   (otvett, uid))  # Обновляем ник в бд
                    connect.commit()
            new = 'https://ria.ru'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/80.0.3987.149 Safari/537.36'}

            # Парсим всю страницу
            def get_news():
                # Парсим всю страницу
                full_page = requests.get(new, headers=headers)
                # Разбираем через BeautifulSoup
                soup = bs4.BeautifulSoup(full_page.content, 'html.parser')
                # Получаем нужное для нас значение и возвращаем его
                news = soup.findAll("span", {"class": "cell-main-photo__title"})
                elems = soup.findAll('a', class_='cell-main-photo__link')
                numbers = []
                for i in elems:
                    numbers.append(str(i.attrs["href"][4:]))
                    return news[0].text, numbers

            news_suda = get_news()
            with sqlite3.connect('data.db', timeout=60) as connect:
                cursor = connect.cursor()
                cursor.execute("UPDATE cache SET news = ? WHERE uid = ? ",
                               (str(news_suda), uid,))  # Обновляем ник в бд
                connect.commit()
            fil = 'https://www.google.com/search?q=фильм&client=opera-gx&hs=rwJ&sxsrf=ALiCzsZlML87VLqlGBPJ4C8KhXRbM3LXlA%3A1665497214136&ei=fnhFY5j7B5eawPAP-qyK-AM&ved=0ahUKEwiYssrOrNj6AhUXDRAIHXqWAj8Q4dUDCA0&uact=5&oq=фильм&gs_lcp=Cgdnd3Mtd2l6EAMyBAgjECcyCggAELEDEIMBEEMyCwgAEIAEELEDEIMBMggIABCABBCxAzIICC4QsQMQgwEyCAgAELEDEIMBMgsIABCABBCxAxCDATIICAAQsQMQgwEyBQguEIAEMgsIABCABBCxAxCDAToKCAAQRxDWBBCwAzoHCAAQsAMQQzoHCCMQ6gIQJzoRCC4QgAQQsQMQgwEQxwEQ0QM6CggAEIAEEIcCEBQ6BQgAEIAEOgsILhCABBDHARCvAToNCAAQgAQQhwIQsQMQFDoOCAAQgAQQsQMQgwEQyQM6CwguEIAEELEDEIMBOgoILhCABBDUAhAKOgcIIxCxAhAnOg0IABCABBCxAxCDARAKOgoIABCABBCxAxAKOgcILhCABBAKSgQIQRgASgQIRhgAUJ4GWMccYJQdaARwAXgAgAFGiAG2A5IBATeYAQCgAQGwAQrIAQnAAQE&sclient=gws-wiz#wxpd=:true'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/80.0.3987.149 Safari/537.36'}

            # Парсим всю страницу
            def get_film():
                # Парсим всю страницу
                full_page = requests.get(fil, headers=headers)
                # Разбираем через BeautifulSoup
                soup = bs4.BeautifulSoup(full_page.content, 'html.parser')
                # Получаем нужное для нас значение и возвращаем его
                films = soup.findAll("div", {"class": "NJU16b"})
                return films[0].text

            film_suda = get_film()
            filmclear = film_suda.replace(" ", '+')
            with sqlite3.connect('data.db', timeout=60) as connect:
                cursor = connect.cursor()
                cursor.execute("UPDATE cache SET film = ? WHERE uid = ? ",
                               (str(filmclear), uid,))  # Обновляем ник в бд
                connect.commit()
            citata = 'https://quote-citation.com/random'  # ссылка на гуголь откуда надо парсить
            # Заголовки для передачи вместе с URL, чтоб сайт не посчитал нас ботом
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/80.0.3987.149 Safari/537.36'}

            # Метод для получения курса валюты
            def get_citata():
                # Парсим всю страницу
                full_page_citata = requests.get(citata, headers=headers)
                # Разбираем через BeautifulSoup
                soup = bs4.BeautifulSoup(full_page_citata.content, 'html.parser')
                # Получаем нужное для нас значение и возвращаем его
                citata_suda = soup.findAll('div', {"class": "quote-text"})
                return citata_suda[0].text

            citata_sudaa = get_citata()
            with sqlite3.connect('data.db', timeout=60) as connect:
                cursor = connect.cursor()
                cursor.execute("UPDATE cache SET citata = ? WHERE uid = ? ",
                               (str(citata_sudaa), uid,))  # Обновляем ник в бд
                connect.commit()
            with sqlite3.connect('data.db', timeout=60) as connect:
                cursor = connect.cursor()
                cursor.execute("SELECT * FROM settings WHERE uid = ? ",
                               (uid,))  # Обновляем ник в бд
                setting = cursor.fetchall()
                connect.commit()

            otvet_valute = ''
            otvet_weather = ''
            otvet_film = ''
            otvet_news = ''
            otvet_citata = ''

            if setting[0][0] == 1:
                otvet_valute = ('\n\nКурс валют: \n' + str(string))
            if setting[0][1] == 1:
                otvet_weather = (f'\n\nПогода в {city}:\n' + "Температура: " + convert_temp[
                    0].text + " °C\n" + 'Вероятность осадков: ' + convert_vo[
                                     0].text + "\n" + 'Влажность: ' + convert_vl[0].text + "\n" + 'Ветер: ' +
                                 convert_spd[
                                     0].text + "\n" + convert_wth[
                                     0].text)
            if setting[0][2] == 1:
                otvet_news = ("\n\nГлавная новость: \n" + str(news_suda).replace("(", "").replace("'", "").replace(",",
                                                                                                                   "").replace(
                    "[", "").replace("]",
                                     "").replace(
                    ")", "").replace("s://", ""))
            if setting[0][3] == 1:
                otvet_film = ("\n\nПопулярный фильм:\n" + str(film_suda).replace("(", "").replace("'", "").replace(",",
                                                                                                                   "").replace(
                    "[", "").replace("]",
                                     "").replace(
                    ")",
                    "") + '\n' + f'https://www.google.com/search?client=opera-gx&q={filmclear}&sourceid=opera&ie=UTF-8&oe=UTF-8')
            if setting[0][4] == 1:
                otvet_citata = ('\n\nЦитата дня:\n' +
                                str(citata_sudaa).replace("[", "").replace("'", "").replace("]", ""))

            otvet = (greet + ', ' + str(infooon).replace("[", "").replace("'", "").replace("]", "") + '!' + str(
                otvet_valute) + str(otvet_weather) + str(otvet_news) + str(otvet_film) + str(otvet_citata))
            fres -= 1
            await bot.send_message(uid, otvet)
        else:
            if fres != 0:
                fres -= 1
            if fres == 0:
                with sqlite3.connect('data.db', timeout=60) as connect:
                    cursor.execute("SELECT * FROM time")
                    resultssss = cursor.fetchall()
                    fres = int(len(resultssss))
                    connect.commit()
                    await asyncio.sleep(60)


async def on_startup(x):
    asyncio.create_task(run())


@dp.message_handler(commands='start')  # Приветственное сообщение при команде /start
async def cmd_start(message: types.Message):
    with sqlite3.connect('data.db', timeout=60) as connect:
        cursor = connect.cursor()
        cursor.execute("SELECT uid FROM time WHERE uid = ?", (message.from_user.id,))
        start = cursor.fetchall()
        infonn = list(sum(start, ()))
        connect.commit()
        if infonn == []:
            with sqlite3.connect('data.db', timeout=60) as connect:
                cursor = connect.cursor()
                cursor.execute("INSERT INTO time (uid) VALUES (?)",
                               (message.from_user.id,))
                cursor.execute("INSERT INTO cache (uid) VALUES (?)",
                               (message.from_user.id,))
                cursor.execute("INSERT INTO valute (uid) VALUES (?)",
                               (message.from_user.id,))
                cursor.execute(
                    "INSERT INTO settings (uid, valute, weather, news, film, citata) VALUES (?, ?, ?, ?, ?, ?)",
                    (message.from_user.id, '1', '1', '1', '1', '1'))
                connect.commit()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3).add(
        KeyboardButton(text='Настроить время приветствия'),
        KeyboardButton(text='Настроить форму обращения'),
        KeyboardButton(text='Настроить город'),
        KeyboardButton(text='Настроить отображение блоков'),
        KeyboardButton(text='Настроить Выбор Валюты'))  # Добавили клавиатуру
    await message.answer(
        f'🤖 {message.chat.first_name}, приветствую вас в нашем боте! 🤖\n'
        f'Пожалуйста, воспользуйтесь кнопками для навигации',
        reply_markup=keyboard)  # Выслали текст юзеру


@dp.message_handler(text='Настроить время приветствия')  # Обращение через кнопку настройки времени
async def greeting_time(message: types.Message):
    await message.answer('Введите время приветствия (в формате xx:yy): ',
                         reply_markup=types.ReplyKeyboardRemove())  # Выслали текст юзеру
    await Greeting.time.set()  # Поставили состояние в машине состояний


@dp.message_handler(text='Настроить форму обращения')  # Обращение через кнопку настройки обращений
async def greeting_nickname(message: types.Message):
    await message.answer('Введите форму обращения в приветствии: ',
                         reply_markup=types.ReplyKeyboardRemove())  # Отправили текст юзеру
    await Greeting.nickname.set()  # Поставили состояние в машине состояний


@dp.message_handler(text='Настроить город')  # Обращение через кнопку настройки обращений
async def greeting_city(message: types.Message):
    await message.answer('Введите ваш город: ', reply_markup=types.ReplyKeyboardRemove())  # Отправили текст юзеру
    await Greeting.city.set()  # Поставили состояние в машине состояний


@dp.message_handler(text='Настроить отображение блоков')  # Обращение через кнопку настройки обращений
async def greeting_settings(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3).add(
        KeyboardButton(text='Курс валют'),
        KeyboardButton(text='Погода'),
        KeyboardButton(text='Новости'),
        KeyboardButton(text='Фильм'),
        KeyboardButton(text='Цитата'),
        KeyboardButton(text='Назад'))
    await message.answer('Пожалуйста, воспользуйтесь командной клавиатурой для настройки блоков!',
                         reply_markup=keyboard)
    # await message.answer('🤖',
    #    reply_markup=keyboard)


@dp.message_handler(text='Назад')  # Обращение через кнопку настройки обращений
async def settings_back(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3).add(
        KeyboardButton(text='Настроить время приветствия'),
        KeyboardButton(text='Настроить форму обращения'),
        KeyboardButton(text='Настроить город'),
        KeyboardButton(text='Настроить отображение блоков'),
        KeyboardButton(text='Настроить Выбор Валюты'))
    await message.answer('Вы вернулись в главное меню!',
                         reply_markup=keyboard)
    # await message.answer('',
    #                     reply_markup=keyboard)


@dp.message_handler(text='Настроить Выбор Валюты')  # Обращение через кнопку настройки обращений
async def settings_currency(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        uid = message.from_user.id
        with sqlite3.connect('data.db', timeout=60) as connect:
            cursor = connect.cursor()
            cursor.execute("SELECT * FROM settings WHERE uid = ? ",
                       (uid,))  # Обновляем ник в бд
            setting = cursor.fetchall()
            connect.commit()
            if setting[0][0] == 1:

                await message.answer("Напишите необходимые вам валюты через пробел", reply_markup=types.ReplyKeyboardRemove())
                await Form2.valute.set()

            else:
                await message.answer("Включите блок курса валют")


@dp.message_handler(text='Курс валют')  # Обращение через кнопку настройки обращений
async def settings_currency(message: types.Message):
    uid = message.from_user.id
    with sqlite3.connect('data.db', timeout=60) as connect:
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM settings WHERE uid = ? ",
                       (uid,))  # Обновляем ник в бд
        setting = cursor.fetchall()
        connect.commit()
    if setting[0][0] == 1:
        with sqlite3.connect('data.db', timeout=60) as connect:
            cursor = connect.cursor()
            cursor.execute("UPDATE settings SET valute = 0 WHERE uid = ? ", (uid,))
            connect.commit()
        await message.answer('Блок курса валют успешно отключен!')
    else:
        with sqlite3.connect('data.db', timeout=60) as connect:
            cursor = connect.cursor()
            cursor.execute("UPDATE settings SET valute = 1 WHERE uid = ? ", (uid,))
            connect.commit()
        await message.answer('Блок курса валют успешно включен!')


@dp.message_handler(text='Погода')  # Обращение через кнопку настройки обращений
async def settings_weather(message: types.Message):
    uid = message.from_user.id
    with sqlite3.connect('data.db', timeout=60) as connect:
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM settings WHERE uid = ? ",
                       (uid,))  # Обновляем ник в бд
        setting = cursor.fetchall()
        connect.commit()
    if setting[0][1] == 1:
        with sqlite3.connect('data.db', timeout=60) as connect:
            cursor = connect.cursor()
            cursor.execute("UPDATE settings SET weather = 0 WHERE uid = ? ", (uid,))
            connect.commit()
        await message.answer('Блок погоды успешно отключен!')
    else:
        with sqlite3.connect('data.db', timeout=60) as connect:
            cursor = connect.cursor()
            cursor.execute("UPDATE settings SET weather = 1 WHERE uid = ? ", (uid,))
            connect.commit()
        await message.answer('Блок погоды успешно включен!')


@dp.message_handler(text='Новости')  # Обращение через кнопку настройки обращений
async def settings_news(message: types.Message):
    uid = message.from_user.id
    with sqlite3.connect('data.db', timeout=60) as connect:
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM settings WHERE uid = ? ",
                       (uid,))  # Обновляем ник в бд
        setting = cursor.fetchall()
        connect.commit()
    if setting[0][2] == 1:
        with sqlite3.connect('data.db', timeout=60) as connect:
            cursor = connect.cursor()
            cursor.execute("UPDATE settings SET news = 0 WHERE uid = ? ", (uid,))
            connect.commit()
        await message.answer('Блок новостей успешно отключен!')
    else:
        with sqlite3.connect('data.db', timeout=60) as connect:
            cursor = connect.cursor()
            cursor.execute("UPDATE settings SET news = 1 WHERE uid = ? ", (uid,))
            connect.commit()
        await message.answer('Блок новостей успешно включен!')


@dp.message_handler(text='Фильм')  # Обращение через кнопку настройки обращений
async def settings_film(message: types.Message):
    uid = message.from_user.id
    with sqlite3.connect('data.db', timeout=60) as connect:
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM settings WHERE uid = ? ",
                       (uid,))  # Обновляем ник в бд
        setting = cursor.fetchall()
        connect.commit()
    if setting[0][3] == 1:
        with sqlite3.connect('data.db', timeout=60) as connect:
            cursor = connect.cursor()
            cursor.execute("UPDATE settings SET film = 0 WHERE uid = ? ", (uid,))
            connect.commit()
        await message.answer('Блок фильмов успешно отключен!')
    else:
        with sqlite3.connect('data.db', timeout=60) as connect:
            cursor = connect.cursor()
            cursor.execute("UPDATE settings SET film = 1 WHERE uid = ? ", (uid,))
            connect.commit()
        await message.answer('Блок фильмов успешно включен!')


@dp.message_handler(text='Цитата')  # Обращение через кнопку настройки обращений
async def settings_citata(message: types.Message):
    uid = message.from_user.id
    with sqlite3.connect('data.db', timeout=60) as connect:
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM settings WHERE uid = ? ",
                       (uid,))  # Обновляем ник в бд
        setting = cursor.fetchall()
        connect.commit()
    if setting[0][4] == 1:
        with sqlite3.connect('data.db', timeout=60) as connect:
            cursor = connect.cursor()
            cursor.execute("UPDATE settings SET citata = 0 WHERE uid = ? ", (uid,))
            connect.commit()
        await message.answer('Блок цитат успешно отключен!')
    else:
        with sqlite3.connect('data.db', timeout=60) as connect:
            cursor = connect.cursor()
            cursor.execute("UPDATE settings SET citata = 1 WHERE uid = ? ", (uid,))
            connect.commit()
        await message.answer('Блок цитат успешно включен!')


@dp.message_handler()  # Логгирование сообщений если это не команда и не кнопка
async def echo(message: types.Message):
    with sqlite3.connect('data.db', timeout=60) as connect:
        cursor = connect.cursor()
        cursor.execute("INSERT INTO time (uid) VALUES (?)", [message.from_user.id, ])
        connect.commit()  # Завершаем работу с бд
    now = datetime.now()  # Узнаем время
    current_time = now.strftime("%d-%m-%Y %H:%M:%S")  # Ставим более удобный, для русского глаза, формат времени
    print(
        f'[{current_time}] {message.chat.first_name} {message.chat.last_name}: {message.text} [user id '
        f'{message.from_user.id}]')  # Выводим в консоль время, имя, фамилию, сообщение и айди пользователя


if __name__ == '__main__':  # Чтоб это всё не загнулось при ошибке
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
