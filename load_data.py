import os
import pandas as pd

def read_csv_file(filename):
    """Ищем файл в папке data/ или рядом с main.py."""
    p1 = os.path.join('data', filename)
    p2 = filename

    if os.path.exists(p1):
        return pd.read_csv(p1)
    if os.path.exists(p2):
        return pd.read_csv(p2)

    raise FileNotFoundError(
        f"Не нашли файл {filename}. Положи его в папку data/ или рядом с main.py"
    )

def load_all():
    students = read_csv_file('students.csv')
    performance = read_csv_file('performance.csv')
    attendance = read_csv_file('attendance.csv')

    # эти файлы не обязательны для варианта 5, но если есть — тоже загрузим
    try:
        homework = read_csv_file('homework.csv')
    except:
        homework = None

    try:
        comm = read_csv_file('teacher_parent_communication.csv')
    except:
        comm = None

    return students, performance, attendance, homework, comm
