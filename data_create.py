import sqlite3

# Создаем подключение к базе данных
conn = sqlite3.connect('probability_tasks.db')
cursor = conn.cursor()

# Создаем таблицу
cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    solution TEXT NOT NULL
)
''')

# Функция для добавления задачи
def add_task(task, solution):
    try:
        cursor.execute('''
        INSERT INTO tasks (task, solution) VALUES (?, ?)
        ''', (task, solution))
        conn.commit()
        print("Задача успешно добавлена!")
    except Exception as e:
        print(f"Ошибка при добавлении задачи: {e}")

# Функция для получения всех задач
def get_all_tasks():
    cursor.execute('SELECT * FROM tasks')
    return cursor.fetchall()

# Функция для поиска задачи по ID
def get_task_by_id(task_id):
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    return cursor.fetchone()

# Добавляем несколько примеров задач
tasks_data = [
    (
        "В коробке 10 синих и 6 красных шаров. Наудачу извлекают 2 шара. Найдите вероятность того, что они разного цвета.",
        "Решение:\n"
        "Всего шаров: 16\n"
        "Благоприятные исходы: 10 * 6 = 60\n"
        "Все возможные исходы: C(16,2) = 120\n"
        "P = 60/120 = 0.5"
    ),
    (
        "В группе 12 студентов, среди которых 8 отличников. Случайным образом отобраны 9 студентов. Найдите вероятность того, что среди них 5 отличников.",
        "Решение:\n"
        "C(8,5) * C(4,4) / C(12,9) = 56/99"
    ),
    (
        "Игральную кость бросают дважды. Найдите вероятность того, что оба раза выпадет число больше 3.",
        "Решение:\n"
        "P = (3/6) * (3/6) = 1/4"
    )
]

# Заполняем базу данных
for task, solution in tasks_data:
    add_task(task, solution)

# Пример получения всех задач
all_tasks = get_all_tasks()
for task in all_tasks:
    print(f"ID: {task[0]}")
    print(f"Задача: {task[1]}")
    print(f"Решение: {task[2]}\n")

# Закрываем соединение
conn.close()
