# Урок 4. SQL – работа с несколькими таблицами

import pymysql
from config import host, user, db_name, password
from datetime import datetime, timedelta

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

        # Drop table Analysis
        cursor.execute("DROP TABLE IF EXISTS Orders;")
        cursor.execute("DROP TABLE IF EXISTS GroupsAn;")
        cursor.execute("DROP TABLE IF EXISTS Analysis;")
        # Create table Analysis
        create_analysis_table = """
        CREATE TABLE Analysis (
            an_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
            an_name VARCHAR(50),
            an_cost INT,
            an_price INT,
            an_group INT
        );
        """
        cursor.execute(create_analysis_table)
        print("Table 'Analysis' created")

        # Insert into Analysis table
        insert_into_analysis = """
        INSERT INTO Analysis (an_name, an_cost, an_price, an_group)
        VALUES 
            ('Общий анализ крови', 30, 50, 1),
            ('Биохимия крови', 150, 210, 1),
            ('Анализ крови на глюкозу', 110, 130, 1),
            ('Общий анализ мочи', 25, 40, 2),
            ('Общий анализ кала', 35, 50, 2),
            ('Общий анализ мочи', 25, 40, 2),
            ('Тест на COVID-19', 160, 210, 3);
        """
        cursor.execute(insert_into_analysis)
        print("Inserted data into 'Analysis' table")

        # Create table GroupsAn
        create_groupsan_table = """
        CREATE TABLE GroupsAn (
            gr_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
            gr_name VARCHAR(50),
            gr_temp FLOAT(5,1),
            FOREIGN KEY (gr_id) REFERENCES Analysis (an_id)
            ON DELETE CASCADE ON UPDATE CASCADE
        );
        """
        cursor.execute(create_groupsan_table)
        print("Table 'GroupsAn' created")

        # Insert into GroupsAn table
        insert_into_groupsan = """
        INSERT INTO GroupsAn (gr_name, gr_temp)
        VALUES 
            ('Анализы крови', -12.2),
            ('Общие анализы', -20.0),
            ('ПЦР-диагностика', -20.5);
        """
        cursor.execute(insert_into_groupsan)
        print("Inserted data into 'GroupsAn' table")

        # Select from GroupsAn table
        select_groupsan = "SELECT * FROM GroupsAn;"
        cursor.execute(select_groupsan)
        groupsan_result = cursor.fetchall()
        print("Table 'GroupsAn':")
        for row in groupsan_result:
            print(row)
        print()
        

        # Create table Orders
        create_orders_table = """
        CREATE TABLE Orders (
            ord_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
            ord_datetime DATETIME,
            ord_an INT,
            FOREIGN KEY (ord_an) REFERENCES Analysis (an_id)
            ON DELETE CASCADE ON UPDATE CASCADE
        );
        """
        cursor.execute(create_orders_table)
        print("Table 'Orders' created")

        # Insert into Orders table
        insert_into_orders = """
        INSERT INTO Orders (ord_datetime, ord_an)
        VALUES 
            ('2020-02-04 07:15:25', 1),
            ('2020-02-04 07:20:50', 2),
            ('2020-02-04 07:30:04', 1),
            ('2020-02-04 07:40:57', 1),
            ('2020-02-05 07:05:14', 1),
            ('2020-02-05 07:15:15', 3),
            ('2020-02-05 07:30:49', 3),
            ('2020-02-06 07:10:10', 2),
            ('2020-02-06 07:20:38', 2),
            ('2020-02-07 07:05:09', 1),
            ('2020-02-07 07:10:54', 1),
            ('2020-02-07 07:15:25', 1),
            ('2020-02-08 07:05:44', 1),
            ('2020-02-08 07:10:39', 2),
            ('2020-02-08 07:20:36', 1),
            ('2020-02-08 07:25:26', 3),
            ('2020-02-09 07:05:06', 1),
            ('2020-02-09 07:10:34', 1),
            ('2020-02-09 07:20:19', 2),
            ('2020-02-10 07:05:55', 3),
            ('2020-02-10 07:15:08', 3),
            ('2020-02-10 07:25:07', 1),
            ('2020-02-11 07:05:33', 1),
            ('2020-02-11 07:10:32', 2),
            ('2020-02-11 07:20:17', 3),
            ('2020-02-12 07:05:36', 1),
            ('2020-02-12 07:10:54', 2),
            ('2020-02-12 07:20:19', 3),
            ('2020-02-12 07:35:38', 1);
        """
        cursor.execute(insert_into_orders)
        print("Inserted data into 'Orders' table")
        #Вывести название и цену для всех анализов, которые продавались 5 февраля 2020 и всю следующую неделю.
        start_date = datetime(2020, 2, 5)
        end_date = start_date + timedelta(days=7)

        select_query = "SELECT a.an_name, a.an_price " \
                       "FROM Analysis a " \
                       "JOIN Orders o ON a.an_id = o.ord_an " \
                       "WHERE o.ord_datetime >= %s AND o.ord_datetime < %s"
        cursor.execute(select_query, (start_date, end_date))
        analysis_data = cursor.fetchall()

        print("Analysis sold from", start_date, "to", end_date)
        for row in analysis_data:
            print("Name:", row['an_name'], ", Price:", row['an_price'])
    finally:
        connection.close()


except Exception as ex:
    print("Disconnect")
    print(ex)
