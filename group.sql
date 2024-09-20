-- Таблиця для студентів
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    group_id INTEGER REFERENCES groups(id)
);

-- Таблиця для груп
CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    group_name VARCHAR(100)
);

-- Таблиця для викладачів
CREATE TABLE teachers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

-- Таблиця для предметів
CREATE TABLE subjects (
    id SERIAL PRIMARY KEY,
    subject_name VARCHAR(100),
    teacher_id INTEGER REFERENCES teachers(id)
);

-- Таблиця для оцінок
CREATE TABLE grades (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id),
    subject_id INTEGER REFERENCES subjects(id),
    grade INTEGER CHECK (grade BETWEEN 1 AND 5),
    date DATE
);
