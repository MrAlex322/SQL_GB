# # Урок 2. SQL – создание объектов, простые запросы выборки
# # Используя операторы языка SQL, создайте табличку “sales”. Заполните ее данными
# # Сгруппируйте значений количества в 3 сегмента — меньше 100, 100-300 и больше 300.


import pymysql
from config import host,user,db_name,password

try:
    connection = pymysql.connect(
        host=host,
        port=3306,
        user= user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    print("Successfully connected")

    try:
        cursor = connection.cursor()

        cursor.execute("drop table if exists sales;")
        cursor = connection.cursor()

        create_query =  "create table if not exists sales (" \
	                    "id INT primary key auto_increment," \
                        "order_data date," \
                        "count_product int);" 
        cursor.execute(create_query)
        print("table create")
        connection.commit()


        insert_query = "INSERT INTO sales (order_data, count_product) VALUES " \
                    "('2022-01-01', 156), " \
                    "('2022-01-02', 180), " \
                    "('2022-01-03', 21), " \
                    "('2022-01-04', 124), " \
                    "('2022-01-05', 341);"
        cursor.execute(insert_query)
        connection.commit()
        print("Insert Successfully")


        alter_query = "ALTER TABLE sales ADD Тип_заказа VARCHAR(20);"
        cursor.execute(alter_query)
        connection.commit()
        print("Столбец Тип_заказа добавлен")


        update_query = "UPDATE sales " \
                    "SET Тип_заказа = CASE " \
                    "WHEN count_product < 100 THEN 'Маленький заказ' " \
                    "WHEN count_product BETWEEN 100 AND 300 THEN 'Средний заказ' " \
                    "WHEN count_product > 300 THEN 'Большой заказ' " \
                    "ELSE 'Не определено' END;"
        cursor.execute(update_query)
        connection.commit()

    finally:
        connection.close()


except Exception as ex:
    print("Disconect")
    print(ex)