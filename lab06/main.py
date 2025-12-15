# База даних SQLite створюється автоматично в файлі demo.db

import sqlite3
from pathlib import Path
from datetime import datetime

DB_NAME = "demo.db"
LOG_NAME = "attacks.log"

def log_event(text: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    Path(LOG_NAME).write_text("", encoding="utf-8") if not Path(LOG_NAME).exists() else None
    with open(LOG_NAME, "a", encoding="utf-8") as f:
        f.write(f"{ts} | {text}\n")

def connect():
    return sqlite3.connect(DB_NAME)

def init_db():
    con = connect()
    cur = con.cursor()

    # Створення таблиць з персональною інформацією
    cur.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        group_name TEXT NOT NULL,
        phone TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)

    # Наповнення тестовими даними (один раз)
    cur.execute("SELECT COUNT(*) FROM students")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO students(full_name, group_name, phone) VALUES(?,?,?)",
            [
                ("Maryna Pashchenko", "122-1", "+380501112233"),
                ("Oleksandr Teslenko", "122-1", "+380631234567"),
                ("Olha Khalina", "122-1", "+380971010101"),
                ("Yelezaveta Koltsova", "122-2", "+380981521302"),
            ],
        )

    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO users(username, password, role) VALUES(?,?,?)",
            [
                ("admin", "admin123", "administrator"),
                ("user", "qwerty", "user"),
            ],
        )

    con.commit()
    con.close()

# Вразливий пошук (пряме підставлення введення в SQL)
def search_students_vulnerable(name_part: str):
    con = connect()
    cur = con.cursor()
    sql = f"SELECT id, full_name, group_name, phone FROM students WHERE full_name LIKE '%{name_part}%'"
    log_event(f"VULN search SQL = {sql}")
    try:
        cur.execute(sql)
        rows = cur.fetchall()
    finally:
        con.close()
    return rows

# Захищений пошук (параметризований запит)
def search_students_safe(name_part: str):
    con = connect()
    cur = con.cursor()
    sql = "SELECT id, full_name, group_name, phone FROM students WHERE full_name LIKE ?"
    param = f"%{name_part}%"
    log_event(f"SAFE search SQL = {sql} | param={param!r}")
    try:
        cur.execute(sql, (param,))
        rows = cur.fetchall()
    finally:
        con.close()
    return rows

# Вразлива авторизація
def login_vulnerable(username: str, password: str):
    con = connect()
    cur = con.cursor()
    sql = f"SELECT username, role FROM users WHERE username='{username}' AND password='{password}'"
    log_event(f"VULN login SQL = {sql}")
    try:
        cur.execute(sql)
        row = cur.fetchone()
    finally:
        con.close()
    return row

# Захищена авторизація
def login_safe(username: str, password: str):
    con = connect()
    cur = con.cursor()
    sql = "SELECT username, role FROM users WHERE username=? AND password=?"
    log_event(f"SAFE login SQL = {sql} | params=({username!r}, {password!r})")
    try:
        cur.execute(sql, (username, password))
        row = cur.fetchone()
    finally:
        con.close()
    return row

def print_rows(rows):
    if not rows:
        print("Нічого не знайдено")
        return
    for r in rows:
        print(r)

def main():
    init_db()

    while True:
        print("\n1 - пошук студентів (уразливо)")
        print("2 - пошук студентів (захищено)")
        print("3 - логін (уразливо)")
        print("4 - логін (захищено)")
        print("5 - приклади ін’єкцій")
        print("6 - вихід")
        cmd = input("> ").strip()

        if cmd == "1":
            q = input("Пошук за ПІБ: ")
            rows = search_students_vulnerable(q)
            print_rows(rows)

        elif cmd == "2":
            q = input("Пошук за ПІБ: ")
            rows = search_students_safe(q)
            print_rows(rows)

        elif cmd == "3":
            u = input("Логін: ")
            p = input("Пароль: ")
            res = login_vulnerable(u, p)
            print("Успішний вхід:", res) if res else print("Невірні дані")

        elif cmd == "4":
            u = input("Логін: ")
            p = input("Пароль: ")
            res = login_safe(u, p)
            print("Успішний вхід:", res) if res else print("Невірні дані")

        elif cmd == "5":
            print("Для витоку даних у пошуку (уразливо) можна ввести:")
            print("  %' OR 1=1 --")
            print("Для обходу логіна (уразливо) можна спробувати:")
            print("  username: admin' --")
            print("  password: будь-що")

        elif cmd == "6":
            break

        else:
            print("Невірна команда")

if __name__ == "__main__":
    main()
