#Урок 6. SQL – Транзакции. Временные таблицы, управляющие конструкции, циклы

import pymysql
from config import host, user, db_name, password

try:
    connection = pymysql.connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    print("Successfully connected")

    try:
        cursor = connection.cursor()

        def format_seconds(seconds):
            query = """
            SELECT CONCAT(days, ' days ', hours, ' hours ', minutes, ' minutes ', seconds, ' seconds') AS result
            FROM (
                SELECT
                    FLOOR(%s / (24 * 3600)) AS days,
                    FLOOR((%s %% (24 * 3600)) / 3600) AS hours,
                    FLOOR((%s %% 3600) / 60) AS minutes,
                    %s %% 60 AS seconds
            ) AS formatted;
            """
            cursor.execute(query, (seconds, seconds, seconds, seconds))
            result = cursor.fetchone()
            if result:
                return result['result']
            else:
                return None

        seconds = 123456
        formatted_time = format_seconds(seconds)
        print(formatted_time)

        def get_even_numbers():
            query = """
            WITH RECURSIVE even_numbers AS (
                SELECT 2 AS num
                UNION ALL
                SELECT num + 2 FROM even_numbers WHERE num < 10
            )
            SELECT GROUP_CONCAT(num SEPARATOR ', ') AS even_numbers
            FROM even_numbers;
            """
            cursor.execute(query)
            result = cursor.fetchone()
            if result:
                return result['even_numbers']
            else:
                return None

        even_numbers = get_even_numbers()
        print(even_numbers)
        
    finally:
        connection.close()

except Exception as ex:
    print("Error occurred")
    print(ex)

