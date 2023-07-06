#Урок 5. SQL – оконные функции

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
        # drop table
        cursor.execute("DROP TABLE IF EXISTS cars;")
        # Создание таблицы cars
        create_table_query = "CREATE TABLE IF NOT EXISTS cars (" \
                             "id INTEGER PRIMARY KEY, " \
                             "name TEXT, " \
                             "cost INTEGER);"
        cursor.execute(create_table_query)
        print("Table 'cars' created")
        connection.commit()
        
        # Вставка данных в таблицу cars
        insert_query = "INSERT INTO cars " \
                       "VALUES " \
                       "(1, 'Aud', 52642)," \
                       "(2, 'Mercedes', 57127)," \
                       "(3, 'Volvo', 29000)," \
                       "(4, 'Bentley', 350000)," \
                       "(5, 'Citroen', 21000)," \
                       "(6, 'Humme', 41400)," \
                       "(7, 'Volkswagen', 21600);"
        cursor.execute(insert_query)
        connection.commit()
        print("Data inserted into table 'cars'")
        
        # 1. Создание представления для автомобилей со стоимостью до 25 000 долларов
        create_view_query = "CREATE VIEW cars_view AS SELECT * FROM cars WHERE cost < 25000;"
        cursor.execute(create_view_query)
        print("View 'cars_view' created")
        
        # 2. Изменение порога стоимости в представлении на 30 000 долларов
        alter_view_query = "ALTER VIEW cars_view AS SELECT * FROM cars WHERE cost < 30000;"
        cursor.execute(alter_view_query)
        print("View 'cars_view' altered")
        
        # 3. Создание представления для автомобилей марки "Шкода" и "Ауди"
        create_filtered_view_query = "CREATE VIEW filtered_cars_view AS SELECT * FROM cars WHERE name IN ('Шкода', 'Ауди');"
        cursor.execute(create_filtered_view_query)
        print("View 'filtered_cars_view' created")
        

    finally:
        connection.close()

except Exception as ex:
    print("Disconnect")
    print(ex)
