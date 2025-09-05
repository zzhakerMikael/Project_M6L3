import sqlite3
import telebot
import random
from telebot import types

# Инициализация бота
TOKEN = 'ВАШ_ТОКЕН_БОТА'
bot = telebot.TeleBot(TOKEN)

# Подключение к базе данных
conn = sqlite3.connect('probability_tasks.db', check_same_thread=False)
cursor = conn.cursor()

# Создание таблицы если не существует
cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    solution TEXT NOT NULL
)
''')

# Функция для получения случайной задачи
def get_random_task():
    cursor.execute('SELECT * FROM tasks ORDER BY RANDOM() LIMIT 1')
    return cursor.fetchone()

# Хэндлер для команды /test
@bot.message_handler(commands=['test'])
def send_test(message):
    task = get_random_task()
    if task:
        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        keyboard.add(types.KeyboardButton('Показать решение'))
        
        bot.send_message(
            message.chat.id,
            f"Решите задачу:\n\n{task[1]}",
            reply_markup=keyboard
        )
        bot.register_next_step_handler(message, show_solution, task[2])
    else:
        bot.reply_to(message, "Задачи пока недоступны")

def show_solution(message, solution):
    if message.text == 'Показать решение':
        bot.reply_to(message, f"Решение:\n\n{solution}")
    else:
        bot.reply_to(message, "Команда не распознана")

# Добавление тестовых задач в базу данных
def add_test_tasks():
    tasks = [
        ('В коробке 10 синих и 6 красных шаров. Наудачу извлекают 2 шара. Найдите вероятность того, что они разного цвета.',
         'Решение:\nВсего шаров: 16\nБлагоприятные исходы: 10 * 6 = 60\nВсе возможные исходы: C(16,2) = 120\nP = 60/120 = 0.5'),
        
        ('В группе 12 студентов, среди которых 8 отличников. Случайным образом отобраны 9 студентов. Найдите вероятность того, что среди них 5 отличников.',
         'Решение:\nC(8,5) * C(4,4) / C(12,9) = 56/99'),
        
        ('Игральную кость бросают дважды. Найдите вероятность того, что оба раза выпадет число больше 3.',
         'Решение:\nP = (3/6) * (3/6) = 1/4')
    ]
    
    for task, solution in tasks:
        try:
            cursor.execute('INSERT INTO tasks (task, solution) VALUES (?, ?)', (task, solution))
            conn.commit()
        except:
            pass

# Запуск бота
if __name__ == '__main__':
     # Добавляем тестовые задачи при запуске
    bot.infinity_polling(skip_pending=True)


