import pymysql
from config import db_name, host, user, password

def get_user(user_id):
    connect()
    f = 0
    with connection.cursor() as cursor:
        x = cursor.execute(f"SELECT * FROM `balance` WHERE user_id = {user_id}")
        if (x == 0):
            f = 0
        else:
            f = 1
    disconnect()
    if (f == 1):
        return True
    elif (f == 0):
        return False

def add_user(user_id):
    connect()
    with connection.cursor() as cursor:
        cursor.execute(f"INSERT INTO `balance` (user_id, balance) VALUES ({user_id}, 0.0)")
        cursor.execute(f"INSERT INTO `history` (user_id, history) VALUES ({user_id}, '')")
        connection.commit()
    disconnect()

def get_balance(user_id):
    connect()
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM `balance` WHERE user_id = {user_id}")
        data = cursor.fetchall()
    disconnect()
    return data

def edit_balance(user_id, new_balance):
    connect()
    with connection.cursor() as cursor:
        cursor.execute(f"UPDATE `balance` SET balance = {new_balance} WHERE user_id = {user_id}")
        connection.commit()
    disconnect()

def get_wallet():
    connect()
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM `wallets` WHERE able = 1")
        data = cursor.fetchall()
    disconnect()
    return data

def close_able(wallet):
    connect()
    with connection.cursor() as cursor:
        cursor.execute(f"UPDATE `wallets` SET able = 0 WHERE addr = '{wallet}'")
        connection.commit()
    disconnect()

def open_able(wallet):
    connect()
    with connection.cursor() as cursor:
        cursor.execute(f"UPDATE `wallets` SET able = 1 WHERE addr = `{wallet}`")
        connection.commit()
    disconnect()

def select_goods():
    connect()
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM `goods`")
        data = cursor.fetchall()
    disconnect()
    return data

def select_good(good_id):
    connect()
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM `goods` WHERE good_id = {good_id}")
        data = cursor.fetchall()
    disconnect()
    return data

def get_history(user_id):
    connect()
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM `history` WHERE user_id = {user_id}")
        data = cursor.fetchall()
    disconnect()
    return data

def get_good(good_id):
    connect()
    with connection.cursor() as cursor:
        print(f"SELECT * FROM `goods` WHERE good_id = {good_id}")
        cursor.execute(f"SELECT * FROM `goods` WHERE good_id = {good_id}")
        data = cursor.fetchall()
    disconnect()
    return data

def edit_history(user_id, good_id):
    data = get_history(user_id)
    new_history = str(data[0]['history'])
    new_history += str(good_id) + ' '
    connect()
    with connection.cursor() as cursor:
        cursor.execute(f"UPDATE `history` SET history = '{new_history}' WHERE user_id = {user_id}")
        connection.commit()
    disconnect()

def connect():
    try:
        global connection
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        print("connected")
    except Exception as e:
        print('failed to connect\n')
        print(e)

def disconnect():
    try:
        connection.close()
    finally:
        print('disconnected')