from faker import Faker
import psycopg2
import random
from datetime import datetime

# Ініціалізація Faker для генерації випадкових даних
fake = Faker()

# Підключення до бази даних
try:
    conn = psycopg2.connect("dbname=postgres user=postgres password=2210")
    cursor = conn.cursor()

    # Перевіряємо з'єднання
    print("Підключення до бази даних успішне!")

    # Створення таблиць, якщо вони не існують
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS groups (
        id SERIAL PRIMARY KEY,
        group_name VARCHAR(50)
    );
    
    CREATE TABLE IF NOT EXISTS teachers (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(100)  -- Додавання стовпчика full_name для викладачів
    );
    
    CREATE TABLE IF NOT EXISTS subjects (
        id SERIAL PRIMARY KEY,
        subject_name VARCHAR(100),
        teacher_id INTEGER REFERENCES teachers(id)
    );
    
    CREATE TABLE IF NOT EXISTS students (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(100),
        group_id INTEGER REFERENCES groups(id)
    );
    
    CREATE TABLE IF NOT EXISTS grades (
        id SERIAL PRIMARY KEY,
        student_id INTEGER REFERENCES students(id),
        subject_id INTEGER REFERENCES subjects(id),
        grade INTEGER,
        date DATE
    );
"""
    )
    conn.commit()  # Зберігаємо зміни в базі
    print("Таблиці створено або вже існують.")

    # Додавання даних (якщо необхідно)
    # Додавання груп
    groups = ["Group A", "Group B", "Group C"]
    for group in groups:
        cursor.execute(
            "INSERT INTO groups (group_name) VALUES (%s) ON CONFLICT DO NOTHING;",
            (group,),
        )

    # Додавання викладачів
    for _ in range(5):
        cursor.execute("INSERT INTO teachers (full_name) VALUES (%s)", (fake.name(),))

    # Додавання предметів
    subjects = ["Math", "Physics", "Chemistry", "History", "Literature"]
    for subject in subjects:
        teacher_id = random.randint(1, 5)
        cursor.execute(
            "INSERT INTO subjects (subject_name, teacher_id) VALUES (%s, %s) ON CONFLICT DO NOTHING;",
            (subject, teacher_id),
        )

    # Додавання студентів
    for _ in range(50):
        full_name = fake.name()
        group_id = random.randint(1, 3)
        cursor.execute(
            "INSERT INTO students (full_name, group_id) VALUES (%s, %s) ON CONFLICT DO NOTHING;",
            (full_name, group_id),
        )

    # Додавання оцінок
    for _ in range(1000):
        student_id = random.randint(1, 50)
        subject_id = random.randint(1, len(subjects))
        grade = random.randint(1, 5)
        date = fake.date_between(start_date="-2y", end_date="today")
        cursor.execute(
            "INSERT INTO grades (student_id, subject_id, grade, date) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING;",
            (student_id, subject_id, grade, date),
        )

    # Збереження змін
    conn.commit()
    print("Дані успішно додані!")

    # 1. Топ 5 студентів із найбільшим середнім балом
    cursor.execute(
        """
        SELECT students.full_name, AVG(grades.grade) as avg_grade
        FROM students
        JOIN grades ON students.id = grades.student_id
        GROUP BY students.full_name
        ORDER BY avg_grade DESC
        LIMIT 5;
    """
    )
    top_students = cursor.fetchall()
    print("\nТоп 5 студентів із найбільшим середнім балом:")
    for student, avg_grade in top_students:
        print(f"Студент: {student}, Середній бал: {avg_grade:.2f}")

    # 2. Студент із найвищим середнім балом з певного предмета
    subject_name = "Math"
    cursor.execute(
        """
        SELECT students.full_name, AVG(grades.grade) as avg_grade
        FROM students
        JOIN grades ON students.id = grades.student_id
        JOIN subjects ON grades.subject_id = subjects.id
        WHERE subjects.subject_name = %s
        GROUP BY students.full_name
        ORDER BY avg_grade DESC
        LIMIT 1;
    """,
        (subject_name,),
    )
    best_student = cursor.fetchone()
    print(
        f"\nСтудент із найвищим середнім балом з предмета {subject_name}: {best_student[0]}, Середній бал: {best_student[1]:.2f}"
    )

    # 3. Середній бал у групах з певного предмета
    cursor.execute(
        """
        SELECT groups.group_name, AVG(grades.grade) as avg_grade
        FROM groups
        JOIN students ON groups.id = students.group_id
        JOIN grades ON students.id = grades.student_id
        JOIN subjects ON grades.subject_id = subjects.id
        WHERE subjects.subject_name = %s
        GROUP BY groups.group_name;
    """,
        (subject_name,),
    )
    group_grades = cursor.fetchall()
    print(f"\nСередній бал у групах з предмета {subject_name}:")
    for group, avg_grade in group_grades:
        print(f"Група: {group}, Середній бал: {avg_grade:.2f}")

    # 4. Середній бал на потоці
    cursor.execute(
        """
        SELECT AVG(grade) as avg_grade
        FROM grades;
    """
    )
    average_flow_grade = cursor.fetchone()
    print(f"\nСередній бал на потоці: {average_flow_grade[0]:.2f}")

    # 5. Курси, які читає певний викладач
    teacher_id = 1
    cursor.execute(
        """
        SELECT subjects.subject_name
        FROM subjects
        WHERE subjects.teacher_id = %s;
    """,
        (teacher_id,),
    )
    teacher_subjects = cursor.fetchall()
    print(f"\nКурси, які читає викладач з ID {teacher_id}:")
    for subject in teacher_subjects:
        print(f"Предмет: {subject[0]}")

    # 6. Список студентів у певній групі
    group_name = "Group A"
    cursor.execute(
        """
        SELECT students.full_name
        FROM students
        JOIN groups ON students.group_id = groups.id
        WHERE groups.group_name = %s;
    """,
        (group_name,),
    )
    students_in_group = cursor.fetchall()
    print(f"\nСписок студентів у групі {group_name}:")
    for student in students_in_group:
        print(f"Студент: {student[0]}")

except psycopg2.Error as e:
    print(f"Помилка підключення до бази даних: {e}")
finally:
    # Закриття з'єднання
    if conn:
        cursor.close()
        conn.close()
        print("З'єднання з базою даних закрито.")
