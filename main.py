from func import *

connection = create_connection("sm_app.sqlite")

create_table(connection)

active = 1

while active:
    print("Выберите действие:"
          "\n1 - Просмотреть все заметки"
          "\n2 - Посмотреть конкретную заметку"
          "\n3 - Добавить заметку"
          "\n4 - Удалить заметку"
          "\n5 - Выход ")
    a = input()
    if a == '1':
        show_notes(connection)
    elif a == '2':
        show_certain_note(connection)
    elif a == '3':
        name = input("Введите название заметки: ")
        note = input("Введите текст заметки: ")
        add_note(connection, name, note)
    elif a == '4':
        delete_note(connection)
    elif a == '5':
        break