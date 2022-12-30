import pyodbc
import schedule
import time
import threading


from config import *

"""Соединение с базой данных"""

try:
    strCon = "Driver=" + driver + ";SERVER=" + srv + ";DATABASE=" + db + ";UID=" + user + ";PWD=" + pwd + ";"
    lnk = pyodbc.connect(strCon)
    db = lnk.cursor()
except:
    print('Нет связи с базой данных')

"""Запрос к базе данных"""

sql_query = '''SELECT name, count FROM project_db
WHERE count>0'''

db.execute(sql_query)
objects = db.fetchall()

"""Обработка запроса"""
print(time.ctime())

def query(sql_query):
    global objects
    lnk = pyodbc.connect(strCon)
    db = lnk.cursor()
    db.execute(sql_query)
    new_objects = db.fetchall()
    print(objects)
    print(new_objects)
    if new_objects != objects:
        objects = new_objects
    return objects


schedule.every(20).seconds.do(query, sql_query)


def send_message():
    for object in objects:
        print(f"Уважаемый {object[0]} у Вас {object[1]} сообщений")
        print(time.ctime())


# timers = [1, 2, 3, 4]
# for timer in timers:
#     schedule.every(timer).minutes.do(send_message)

timers = [1, 2, 3, 4]
for timer in timers:
    t = threading.Timer(timer, send_message)
    t.start()
    t.cancel()


"""Запуск цикла"""


while True:
    schedule.run_pending()
    time.sleep(1)
