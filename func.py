import sqlite3
from sqlite3 import Error


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        #print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        #print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


def create_table(connection):
    create_note_table = """
    CREATE TABLE IF NOT EXISTS notes (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT,
      note TEXT NOT NULL
    );
    """
    execute_query(connection, create_note_table)


def add_note(connection, name, note):
    create_note = f"""
    INSERT INTO
      notes (name, note)
    VALUES
      ('{name}', '{note}')
    """
    print("")
    execute_query(connection, create_note)


def show_notes(connection):
    select_notes = "SELECT * from notes"
    notes = execute_read_query(connection, select_notes)
    if notes:
        for note in notes:
            print(f"Заметка {note[0]}")
            print(f"Название: {note[1]}")
            print(note[2], "\n")
    else:
        print("Заметок нет\n")


def show_certain_note(connection):
    flag = 1
    while flag:
        b = input("Найти заметку по:"
                  "\n1 - id"
                  "\n2 - названию"
                  )
        if b == "1" or b == "2":
            print("")
            flag = 0
        else:
            print("\nВведено неверное значение\n")
    if b == '1':
        id = enter_id()
        select_note = f"SELECT * from notes WHERE ID = {id}"
        note = execute_read_query(connection, select_note)
        if note:
            print(note)
        else:
            print(f"Заметки с id {id} не существует")
    elif b == '2':
        name = input("Введите название заметки: ")
        select_note = f"SELECT * from notes WHERE name = '{name}'"
        note = execute_read_query(connection, select_note)
        if note:
            print(note)
        else:
            print(f"Заметки с именем {name} не существует")


def enter_id():
    flag = 1
    while flag:
        id = input("Введите id: ")
        try:
            id = int(id)
        except BaseException:
            print("Введено недопустимое значение")
        else:
            flag = 0
            return id


def delete_note(connection):
    flag = 1
    while flag:
        b = input("Удалить заметку по:"
                  "\n1 - id"
                  "\n2 - названию ")
        if b == "1" or b == "2":
            flag = 0
        else:
            print("\nВведено неверное значение\n")
    if b == '1':
        id = enter_id()
        delete_note = f"DELETE FROM notes WHERE id = {id}"
        execute_query(connection, delete_note)
        print("\nЗаметка удалена\n")
    elif b == '2':
        name = input("Введите название заметки: ")
        delete_note = f"DELETE FROM notes WHERE name = '{name}'"
        execute_query(connection, delete_note)
        print("\nЗаметка удалена\n")