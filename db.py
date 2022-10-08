import sqlite3
from sqlite3 import Error


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path, check_same_thread=False)
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def execute_query(connection, query, dict=''):
    cursor = connection.cursor()
    try:
        cursor.execute(query, dict)
        connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_read_query(connection, query, dict=''):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query, dict)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


def create_table1(connection):
    create_note_table = """
    CREATE TABLE IF NOT EXISTS notes (
      id INTEGER,
      name TEXT,
      note TEXT,
      user_id INTEGER
    );
    """
    execute_query(connection, create_note_table)


def create_table2(connection):
    create_note_table = """
    CREATE TABLE IF NOT EXISTS id (
      user_id INTEGER,
      num INTEGER
    );
    """
    execute_query(connection, create_note_table)


def create_table3(connection):
    create_note_table = """
    CREATE TABLE IF NOT EXISTS names (
      user_id INTEGER,
      name TEXT,
      note_text TEXT
    );
    """
    execute_query(connection, create_note_table)


def show_notes(connection, user_id):
    select_notes = f"SELECT * from notes WHERE user_id = {user_id}"
    notes = execute_read_query(connection, select_notes)
    all_notes = ""
    if notes:
        for note in notes:
            all_notes += f"\nЗаметка {note[0]}"
            all_notes += f"\nНазвание: {note[1]}"
            all_notes += f"\n{note[2]}"
            all_notes += "\n"
        return all_notes.strip()
    else:
        return "Заметок нет"


def is_int(id):
    try:
        id = int(id)
        return True
    except BaseException:
        return False


def show_certain_note_id(connection, user_id, id):
    select_note = f"SELECT * from notes WHERE user_id = {user_id} AND id = {id}"
    note = execute_read_query(connection, select_note)
    return_note = ""
    if note:
        return_note += f"\nЗаметка {note[0][0]}"
        return_note += f"\nНазвание: {note[0][1]}"
        return_note += f"\n{note[0][2]}"
        return return_note
    else:
        return "Заметки с таким id не существует"


def show_certain_note_name(connection, user_id, name):
    select_note = f"SELECT * from notes WHERE user_id = {user_id} AND name = (:name)"
    dict = {'name': name}
    notes = execute_read_query(connection, select_note, dict)
    all_notes = ""
    if notes:
        for note in notes:
            all_notes += f"\nЗаметка {note[0]}"
            all_notes += f"\nНазвание: {note[1]}"
            all_notes += f"\n{note[2]}"
            all_notes += "\n"
        return all_notes.strip()
    else:
        return "Заметки с таким названием не существует"


def get_id(user_id, connection2):
    select_id = f"SELECT num from id WHERE user_id = {user_id}"
    id = execute_read_query(connection2, select_id)
    if id:
        id = int(id[0][0])
        change_id = f"UPDATE id SET num={id + 1} WHERE user_id = {user_id}"
        execute_query(connection2, change_id)
        return id + 1
    else:
        create_id = f"""
            INSERT INTO
              id (user_id, num)
            VALUES
              (:user_id, :num)
            """
        dict = {'user_id': user_id, 'num': 1}
        execute_query(connection2, create_id, dict)
        return 1


def add_note(connection1, connection2, connection3, user_id):
    id = get_id(user_id, connection2)
    name = get_name(user_id, connection3)
    note = get_note(user_id, connection3)
    delete = f"DELETE FROM names WHERE user_id = {user_id}"
    execute_query(connection3, delete)
    create_note = f"""
    INSERT INTO
      notes (id, name, note, user_id)
    VALUES
      (:id, :name, :note, :user_id)
    """
    dict = {'id': id, 'name': name, 'note': note, 'user_id': user_id}
    execute_query(connection1, create_note, dict)
    return f"Заметка '{name}' успешно создана"


def get_name(user_id, connection3):
    select_name = f"SELECT name from names WHERE user_id = {user_id}"
    name = execute_read_query(connection3, select_name)
    return name[0][0]


def get_note(user_id, connection3):
    select_note = f"SELECT note_text from names WHERE user_id = {user_id}"
    name = execute_read_query(connection3, select_note)
    return name[0][0]


def delete_note_id(user_id, id, connection1, connection2):
    if show_certain_note_id(connection1, user_id, id) == "Заметки с таким id не существует":
        return "Заметки с таким id не существует"
    else:
        delete_note = f"DELETE FROM notes WHERE id = {id} AND user_id = {user_id}"
        execute_query(connection1, delete_note)
        change_num(user_id, connection1, connection2)
        return f"Заметка с id {id} успешно удалена"


def delete_note_name(user_id, name, connection1, connection2):
    if show_certain_note_name(connection1, user_id, name) == "Заметки с таким названием не существует":
        return "Заметки с таким названием не существует"
    else:
        delete_note = f"DELETE FROM notes WHERE name = (:name) AND user_id = {user_id}"
        dict = {'name': name}
        execute_query(connection1, delete_note, dict)
        change_num(user_id, connection1, connection2)
        return f"Заметка '{name}' успешно удалена"


def change_num(user_id, connection1, connection2):
    select_notes = f"SELECT * from notes WHERE user_id = {user_id}"
    notes = execute_read_query(connection1, select_notes)
    max_id = 1
    if notes:
        for note in notes:
            if int(note[0]) > max_id:
                max_id = int(note[0])
        change_id = f"UPDATE id SET num={max_id} WHERE user_id = {user_id}"
        execute_query(connection2, change_id)
    else:
        delete_num = f"DELETE FROM id WHERE user_id = {user_id}"
        execute_query(connection2, delete_num)


def save_name(name, user_id, connection3):
    create_name = f"""
        INSERT INTO
          names (user_id, name, note_text)
        VALUES
          (:user_id, :name, :note_text)
        """
    dict = {'user_id': user_id, 'name': name, 'note_text': ""}
    execute_query(connection3, create_name, dict)


def save_note_text(text, user_id, connection3):
    save_text = f"UPDATE names SET note_text=(:text) WHERE user_id = (:user_id)"
    dict = {'text': text, 'user_id': user_id}
    execute_query(connection3, save_text, dict)
