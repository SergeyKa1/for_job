import asyncio
import pyodbc
from config import *
import sqlite3

import time

objects = []

"""Запрос к базе данных"""

sql_query = '''SELECT name, count FROM project_db
WHERE count>0'''

"""Соединение с базой данных"""


async def conect_to():
    while True:
        await asyncio.sleep(1)
        strCon = "Driver=" + driver + ";SERVER=" + srv + ";DATABASE=" + DB + ";UID=" + user + ";PWD=" + pwd + ";"
        lnk = pyodbc.connect(strCon)
        db = lnk.cursor()
        db.execute(sql_query)
        global objects
        objects = db.fetchall()


# async def send_message():
#     global objects
#     while True:
#         await asyncio.sleep(1)
#         print(objects)


# async def response():
#     user_list = []
#     user_list_name = []
#     while True:
#         await asyncio.sleep(2)
#         global objects
#         print(objects)
#         for user in user_list:
#             user.active=False
#         user_list = [User(name, mas, active=True) for name, mas in objects if User(name, mas).name not in user_list_name]
#         user_list_name=[i.name for i in user_list]
#         print(user_list)
#         for i in user_list:
#             print(len(user_list))
#             print(i.name, i.mas, i.active)

async def response():
    while True:
        await asyncio.sleep(2)
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
           userid INTEGER PRIMARY KEY AUTOINCREMENT,
           login TEXT UNIQUE,
           email TEXT,
           msg INT,
           send INT DEFAULT 0);
        """)
        global objects
        print(objects)
        for email, msg in objects:
            user = (email.split('@')[0], email, msg)
            try:
                cur.execute("INSERT INTO users(login, email, msg) VALUES(?, ?, ?);", user)
                conn.commit()
            except sqlite3.IntegrityError:
                print('Есть такой')

        conn.commit()



async def main():
    tasks = [
        conect_to(),
        response(),
    ]
    await asyncio.gather(*tasks)


asyncio.run(main())
