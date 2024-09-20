from faker import Faker
import psycopg2
import random
from datetime import datetime

# Ініціалізація Faker
fake = Faker()

# Підключення до бази даних
conn = psycopg2.connect("dbname=postgres user=postgres password=2210")
cursor = conn.cursor()

# Додавання груп
groups = ["Group A", "Group B", "Group C"]
for group in groups:
    cursor.execute("INSERT INTO groups (group_name) VALUES (%s)", (group,))

# Додавання викладачів
for _ in range(5):
    cursor.execute("INSERT INTO teachers (name) VALUES (%s)", (fake.name(),))

# Додавання предметів
subjects = ["Math", "Physics", "Chemistry", "History", "Literature"]
for subject in subjects:
    teacher_id = random.randint(1, 5)
    cursor.execute(
        "INSERT INTO subjects (subject_name, teacher_id) VALUES (%s, %s)",
        (subject, teacher_id),
    )

# Додавання студентів
for _ in range(50):
    name = fake.name()
    group_id = random.randint(1, 3)
    cursor.execute(
        "INSERT INTO students (name, group_id) VALUES (%s, %s)", (name, group_id)
    )

# Додавання оцінок
for _ in range(1000):
    student_id = random.randint(1, 50)
    subject_id = random.randint(1, len(subjects))
    grade = random.randint(1, 5)
    date = fake.date_between(start_date="-2y", end_date="today")
    cursor.execute(
        "INSERT INTO grades (student_id, subject_id, grade, date) VALUES (%s, %s, %s, %s)",
        (student_id, subject_id, grade, date),
    )

# Збереження змін
conn.commit()

# Закриття з'єднання
cursor.close()
conn.close()
