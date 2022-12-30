import asyncio
from config import *
import pyodbc
import operator

"""Запрос к базе данных"""

sql_query = '''SELECT name, count FROM project_db
WHERE count>0'''

"""Соединение с базой данных"""

list_for_send = []
list_class = []


async def connect_with_db():
    while True:
        await asyncio.sleep(1/100)
        strCon = "Driver=" + driver + ";SERVER=" + srv + ";DATABASE=" + DB + ";UID=" + user + ";PWD=" + pwd + ";"
        lnk = pyodbc.connect(strCon)
        db = lnk.cursor()
        db.execute(sql_query)
        objects = db.fetchall()
        await serialisation(objects)


async def serialisation(objects):
    global list_for_send
    global list_class
    new_users = []
    del_users = []
    for object in objects:
        if object not in list_for_send:
            new_users.append(object)
            list_for_send.append(object)
    for object in list_for_send:
        if object not in objects:
            del_users.append(object)
            list_for_send.remove(object)
    for user in new_users:
        list_class.append(User(user[0], user[1]))
    for del_user in del_users:
        for user in list_class:
            if del_user[0] == user.mail:
                list_class.remove(user)


async def send():
    while True:
        await asyncio.sleep(2)
        global list_class
        user_5 = list(filter(lambda s: s.send == 0, list_class))
        await rocketchat5(user_5)
        user_10 = list(filter(lambda s: s.send == 1, list_class))
        await rocketchat10(user_10)
        user_20 = list(filter(lambda s: s.send == 2, list_class))
        await rocketchat20(user_20)


async def rocketchat5(users):
    print(1, users)
    await asyncio.sleep(20)
    for user in users:
        print('5min')
        print(f'На почту {user.mail} отправлено о {user.msg} не утвержденных рассписаниях')
        user.send += 1


async def rocketchat10(users):
    print(2, users)

    await asyncio.sleep(30)
    for user in users:
        print('10min')
        print(f'На почту {user.mail} отправлено о {user.msg} не утвержденных рассписаниях')
        user.send += 1


async def rocketchat20(users):


        print(3, users)
        await asyncio.sleep(50)
        for user in users:
            print('20min')
            print(f'На почту {user.mail} отправлено о {user.msg} не утвержденных рассписаниях')


async def main():
    tasks = [
        connect_with_db(),
        send()
    ]
    await asyncio.gather(*tasks)


asyncio.run(main())
