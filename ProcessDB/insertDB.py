import sqlite3

class InsertDB(object):
    def __init__(self, filename):
        self.sql_path = filename

    def InsertUser(self, user_id, name, sex, bot_position):
        try:
            sqlConnection = sqlite3.connect(self.sql_path)
            cursor = sqlConnection.cursor()
            print("Connected to SQLite")
            cursor.execute('INSERT INTO User(user_id, name, sex, bot_position) VALUES(?, ?, ?, ?)', (user_id, name, sex, bot_position))
            sqlConnection.commit()
            cursor.close()
        except sqlite3.Error as error:
            print("Failed to insert data: ", error)
        finally:
            if (sqlConnection):
                sqlConnection.close()
                print("The sqlite connection is closed")

    def InsertDiagnostic(self, user_id, date, symptom, prognosis):
        try:
            sqlConnection = sqlite3.connect(self.sql_path)
            cursor = sqlConnection.cursor()
            print("Connected to SQLite")
            cursor.execute('INSERT INTO Diagnostic(user_id, date, symptom, prognosis) VALUES(?, ?, ?, ?)', (user_id, date, symptom, prognosis))
            sqlConnection.commit()
            cursor.close()
            print("insert success")
        except sqlite3.Error as error:
            print("Failed to insert data: ", error)
        finally:
            if (sqlConnection):
                sqlConnection.close()
                print("The sqlite connection is closed")
    
    def SelectUser(self):
        sqlConnection = sqlite3.connect(self.sql_path)
        cursor = sqlConnection.execute("SELECT * FROM User")
        for row in cursor:
            print(row)
        sqlConnection.close()

# filename = 'E:\BaiTapTriTueNhanTao\demo_chatbot_rasa_2\ProcessDB\database.db'
# insert = InsertDB(filename)
# insert.SelectUser()
# insert.InsertUser('1hgcjjdyduccytxtyg87t679g98g898i', 'Cuong', 'Nam', 'Em')