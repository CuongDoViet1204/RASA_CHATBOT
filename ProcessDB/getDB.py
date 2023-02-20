import sqlite3

class GetDB(object):
    def __init__(self, filename):
        self.sql_path = filename
    def get_user(self, sender_id):
        try:
            sqlConnection = sqlite3.connect(self.sql_path)
            cursor = sqlConnection.cursor()
            print("Connected to SQLite")
            cursor.execute('SELECT * FROM User where user_id = ?', [sender_id])
            row = cursor.fetchone()
            if row:
                return row
            else:
                return None
            sqlConnection.commit()
            cursor.close()
        except sqlite3.Error as error:
            print("Failed to get data: ", error)
        finally:
            if (sqlConnection):
                sqlConnection.close()
                print("The sqlite connection is closed")

    def get_diagnostic(self, sender_id):
        try:
            sqlConnection = sqlite3.connect(self.sql_path)
            cursor = sqlConnection.cursor()
            print("Connected to SQLite")
            cursor.execute('SELECT * FROM Diagnostic where user_id = ?', [sender_id])
            rows = cursor.fetchall()
            if rows:
                return rows
            else:
                return None
            # res = [[]]
            # i = 0
            # while True:
            #     row = cursor.fetchone()
            #     if row == None:
            #         break
            #     # res.append(row)
            #     res[i] = row.tolist()
            #     i += 1
            sqlConnection.commit()
            cursor.close()
        except sqlite3.Error as error:
            print("Failed to get data: ", error)
        finally:
            if (sqlConnection):
                sqlConnection.close()
                print("The sqlite connection is closed")
            
# filename = 'E:\BaiTapTriTueNhanTao\demo_chatbot_rasa_2\ProcessDB\database.db'
# getDB = GetDB(filename)
# diagnostics = getDB.get_diagnostic('8774910069248412')
# #     print(row)
# # print(rows)
# if diagnostics:
#             # for row in diagnostics:
#             #     ret_text = "Ngày: " + row[1] + '\n' + "Triệu chứng: "
#             #     i = -1
#             #     for idx in row[2]:
#             #         i = i + 1
#             #         if int(idx) != 0:
#             #             ret_text = ret_text + list_symptom[i] + ', '
#     for i in range (len(diagnostics)):
#         # ret_text = "Ngày: " + diagnostics[i][1] + '\n' + "Triệu chứng: "
#         # for idx in range(len(diagnostics[i][2])):
#         #     if diagnostics[i][2][idx] != 0:
#         #         ret_text = ret_text + str(diagnostics[i][2][idx]) + ', '
#         # ret_text += '\n' + 'Chẩn đoán: ' + diagnostics[i][3] +'\n*******************************'
#         print(len(diagnostics[i][2]) / 4)