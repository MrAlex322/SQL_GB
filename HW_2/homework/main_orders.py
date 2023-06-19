# Создайте таблицу “orders”, заполните ее значениями. Покажите “полный” статус заказа, используя оператор CASE

import pymysql
from config import host,user, db_name, password

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

        cursor.execute("drop table if exists orders;")
        cursor = connection.cursor()

        create_query =  "create table if not exists orders (" \
	                    "id INT primary key auto_increment," \
                        "employee_id varchar(10)," \
                        "amount DECIMAL," \
                        "order_status ENUM('open', 'closed', 'cancelled'));"
        cursor.execute(create_query)
        print("table create")
        connection.commit()

        insert_query = "INSERT INTO orders (employee_id, amount, order_status) VALUES " \
                "('e03', 15, 'open'), " \
                "('e01', 15.50, 'open'), " \
                "('e05', 100.70, 'closed'), " \
                "('e02', 22.18, 'open'), " \
                "('e04', 9.50, 'cancelled');"
        cursor.execute(insert_query)
        connection.commit()
        print("Insert Successfully")

        alter_query = "ALTER TABLE orders ADD full_order_status VARCHAR(45);"
        cursor.execute(alter_query)
        connection.commit()
        print("Столбец full_order_status добавлен")


        update_query = "UPDATE orders " \
                    "SET full_order_status = CASE " \
                    "WHEN order_status = 'open' THEN 'Order is in open state.' " \
                    "WHEN order_status = 'closed' THEN 'Order is closed.' " \
                    "ELSE 'Order is cancelled.' " \
                    "END;"       
        cursor.execute(update_query)
        connection.commit()
        print("ssss Successfully")

    finally:
        connection.close()


except Exception as ex:
    print("Disconect")
    print(ex)