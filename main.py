# Импортируем библиотеки
import telebot
import sqlite3
from telebot import types

# Создаем соединение с базой данных
conn = sqlite3.connect('movies.db')
cursor = conn.cursor()

# Выполняем SQL-запрос для выборки всех записей из таблицы movies
cursor.execute("SELECT * FROM movies")

# Получаем все записи
movies = cursor.fetchall()

# Выводим результат
for movie in movies:
    print(movie)

# Закрываем соединение
conn.close()

# Создаем экземпляр бота и указываем токен бота
bot = telebot.TeleBot('6889335060:AAFG_2Syv8b--_cJaWVTk_zUsEytxGJ1cdk')

# Подключаемся к базе данных SQLite
conn = sqlite3.connect('movies.db')
cursor = conn.cursor()

# Создаем таблицу для фильмов, если она не существует
cursor.execute('''CREATE TABLE IF NOT EXISTS movies (code TEXT, title TEXT, link TEXT)''')
conn.commit()

check_subscription_markup = types.InlineKeyboardMarkup()
check_subscription_markup.add(types.InlineKeyboardButton("Проверить подписку", callback_data="check_subscription"))

# Клавиатура для основного меню
menu_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
menu_markup.row(
    telebot.types.KeyboardButton('Посмотреть фильм по номеру'),
    telebot.types.KeyboardButton('Показать список фильмов')
)



# Обработчик для команды /start
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # chat_id канала, который вы хотите проверить
    channel_chat_id = -1002096752895  # Замените на ID своего канала

    # user_id пользователя, для которого вы хотите проверить подписку
    user_id = message.from_user.id  # Замените на ID пользователя

    # Проверка подписки
    chat_member = bot.get_chat_member(channel_chat_id, user_id)

    # Проверяем статус участника (status) - 'member' означает, что пользователь подписан
    if chat_member.status == 'member':
        is_subscribed = True
    else:
        is_subscribed = False

    if is_subscribed:
        # Если подписка есть, отправляем приветственное сообщение и основное меню
        bot.send_message(chat_id, f'Привет, {message.from_user.first_name}! Теперь вы подписаны на наши каналы.',
                         reply_markup=menu_markup)
    else:
        # Если подписки нет, сообщаем пользователю о необходимости подписаться с кликабельной ссылкой на канал и кнопкой "проверить подписку"
        message_text = f'Привет! Для использования бота вам необходимо подписаться на наши каналы. ' \
                       f'Подпишитесь на <a href="https://t.me/dadadadada123123">наш канал</a> и нажмите кнопку "Проверить подписку".'
        sent_message = bot.send_message(chat_id, message_text, reply_markup=check_subscription_markup, parse_mode='HTML')

# Обработчик для кнопки "Проверить подписку"
@bot.callback_query_handler(func=lambda call: call.data == 'check_subscription')
def check_subscription_callback(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    user_id = call.from_user.id

    # chat_id канала, который вы хотите проверить
    channel_chat_id = -1002096752895  # Замените на ID своего канала

    # Проверка подписки
    chat_member = bot.get_chat_member(channel_chat_id, user_id)

    if chat_member.status == 'member':
        # Если пользователь подписан, удаляем сообщение с кнопкой "Проверить подписку"
        bot.delete_message(chat_id, message_id)

        # Отправляем сообщение о том, что подписка успешно проверена
        bot.send_message(chat_id,
                         'Ваша подписка успешно проверена. Теперь вы можете использовать бота. Для поиска отправьте название или код фильма/сериала.',
                         reply_markup=menu_markup)


@bot.message_handler(func=lambda message: message.text == 'Показать список фильмов')
def show_movie_list(message):
    chat_id = message.chat.id

    # Добавьте код для извлечения списка фильмов из базы данных
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute("SELECT code, title FROM movies")
    movie_list = cursor.fetchall()
    conn.close()

    if movie_list:
        movie_list_text = "Список фильмов:\n"
        for code, title in movie_list:
            movie_list_text += f"{code}: {title}\n"

        bot.send_message(chat_id, movie_list_text)
    else:
        bot.send_message(chat_id, "Список фильмов пуст.")

# Обработчик для кнопки "Посмотреть фильм по номеру"
@bot.message_handler(func=lambda message: message.text == 'Посмотреть фильм по номеру')
def ask_for_movie_code(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # chat_id канала, который вы хотите проверить
    channel_chat_id = -1002096752895  # Замените на ID своего канала

    # Проверка подписки
    chat_member = bot.get_chat_member(channel_chat_id, user_id)

    if chat_member.status == 'member':
        # Если подписка есть, предоставьте доступ к функционалу
        bot.send_message(chat_id, 'Введите код фильма:')
    else:
        # Если подписки нет, сообщите пользователю о необходимости подписаться
        message_text = f'Для использования этой функции вам необходимо подписаться на наш канал. ' \
                       f'Подпишитесь на <a href="https://t.me/dadadadada123123">наш канал</a> и нажмите кнопку "Проверить подписку" для доступа к функционалу.'
        sent_message = bot.send_message(chat_id, message_text, reply_markup=check_subscription_markup, parse_mode='HTML')

@bot.message_handler(func=lambda message: True)
def handle_movie_code(message):
    chat_id = message.chat.id
    code = message.text

    # chat_id канала, который вы хотите проверить
    channel_chat_id = -1002096752895  # Замените на ID своего канала

    # Проверка подписки
    user_id = message.from_user.id
    chat_member = bot.get_chat_member(channel_chat_id, user_id)

    if chat_member.status != 'member':
        # Если пользователь не подписан, отправляем сообщение о необходимости подписки
        message_text = f'Для использования этой функции вам необходимо подписаться на наш канал. ' \
                       f'Подпишитесь на <a href="https://t.me/dadadadada123123">наш канал</a> и нажмите кнопку "Проверить подписку" для доступа к функционалу.'
        sent_message = bot.send_message(chat_id, message_text, reply_markup=check_subscription_markup, parse_mode='HTML')
        return

    # Если пользователь подписан, продолжаем обработку сообщения
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()

    # Выполните запрос к базе данных для получения информации о фильме
    cursor.execute("SELECT title, link FROM movies WHERE code=?", (code,))
    movie = cursor.fetchone()

    if movie:
        title, link = movie
        bot.send_message(chat_id, f'Под кодом {code} находится фильм "{title}"\nПосмотреть можно здесь - {link}')
    else:
        bot.send_message(chat_id, f'Фильм с кодом {code} не найден.')

    conn.close()


# Запускаем бота
bot.polling(none_stop=True)
