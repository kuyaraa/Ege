import pymysql

def connect_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",  # Укажите ваш пароль
        database="ege",
        port=3306,
        cursorclass=pymysql.cursors.DictCursor
    )
