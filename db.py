import sqlite3

# Создаем соединение с базой данных
conn = sqlite3.connect('movies.db')
cursor = conn.cursor()

movies = [
    ('99', '1+1', 'https://www.kinopoisk.ru/lists/movies/top250/?utm_referrer=yandex.ru'),
    ('100', 'Фильм_2', 'ссылка_на_Фильм_2'),
    # Добавьте другие фильмы по аналогии
]

for code, title, link in movies:
    cursor.execute("INSERT INTO movies (code, title, link) VALUES (?, ?, ?)", (code, title, link))

# Сохраняем изменения в базе данных
conn.commit()

# Закрываем соединение
conn.close()
