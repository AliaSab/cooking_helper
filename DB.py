import sqlite3

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('recipes.db')
cursor = connection.cursor()


# Создаем таблицу Recipes
cursor.execute('''
CREATE TABLE IF NOT EXISTS Recipes (
Name TEXT PRIMARY KEY,
Receipt TEXT NOT NULL,
Ingredients TEXT NOT NULL,
meal_time TEXT NOT NULL
)
''')



# Создаем таблицу Users
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
ID Integer PRIMARY KEY,
Name TEXT,
login TEXT NOT NULL,
password TEXT NOT NULL,
favorite TEXT
)
''')



# Сохраняем изменения и закрываем соединение
connection.commit()
connection.close()