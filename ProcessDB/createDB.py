import sqlite3

sql_path = 'E:\BaiTapTriTueNhanTao\demo_chatbot_rasa_2\ProcessDB\database.db'

try:
    sqliteConnection = sqlite3.connect(sql_path)
    cursor = sqliteConnection.cursor()
    cursor.execute("create table if not exists User(user_id PRIMARY KEY, name, sex, bot_position)")
    cursor.execute("create table if not exists Diagnostic(user_id, date, symptom, prognosis)")
    print("create success")
except sqlite3.Error as error:
    print("Failed to create table: ", error)
finally:
    if (sqliteConnection):
        sqliteConnection.close()
        print("The sqlite connection is closed")
    