# Урок 3. SQL – выборка данных, сортировка, агрегатные функции

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
        #drop table
        cursor.execute("drop table if exists staff;")
        #create table
        create_query =  "create table if not exists staff (" \
	                    "id INT primary key auto_increment," \
                        "firstName varchar(45)," \
                        "lastName varchar(45)," \
                        "post varchar(45)," \
                        "seniority int," \
                        "salary decimal(8,2)," \
                        "age int);" 
        cursor.execute(create_query)
        print("table create")
        connection.commit()

        #insert table
        insert_query = "insert staff (firstname, lastname, post, seniority, salary, age)" \
                        "values ('Вася', 'Петров', 'Начальник', 40, 100000, 60)," \
                                "('Петр', 'Власов', 'Начальник', 8, 70000, 30)," \
                                "('Катя', 'Катина', 'Инженер', 2, 70000, 25)," \
                                "('Саша', 'Сасин', 'Инженер', 12, 50000, 35)," \
                                "('Иван', 'Петров', 'Рабочий', 40, 30000, 59)," \
                                "('Петр', 'Петров', 'Рабочий', 20, 55000, 60)," \
                                "('Сидр', 'Сидоров', 'Рабочий', 10, 20000, 35)," \
                                "('Антон', 'Антонов', 'Рабочий', 8, 19000, 28)," \
                                "('Юрий', 'Юрков', 'Рабочий', 5, 15000, 25)," \
                                "('Максим', 'Петров', 'Рабочий', 2, 11000, 19)," \
                                "('Юрий', 'Петров', 'Рабочий', 3, 12000, 24)," \
                                "('Людмила', 'Маркина', 'Уборщик', 10, 10000, 49);"
        cursor.execute(insert_query)
        connection.commit()
        print("Insert Successfully")

# Отсортируйте данные по полю заработная плата (salary) в порядке: возрастания; 

        select_salary_up = "SELECT salary " \
                            "FROM staff " \
                            "order by salary;" 
        cursor.execute(select_salary_up)
        connection.commit()
        result = cursor.fetchall()

        print("Сортировка зп по возрастанию.")
        for row in result:
            print(row)  
# Отсортируйте данные по полю заработная плата (salary) в порядке: убывания;   
        select_salary_low = "SELECT salary " \
                            "FROM staff " \
                            "order by salary desc;" 
        cursor.execute(select_salary_low)
        connection.commit()
        result = cursor.fetchall()

        print("Сортировка зп по убыванию.")
        for row in result:
            print(row)  
# Посчитайте суммарную зарплату (salary) по каждой специальности (роst)
        select_total_salary = "SELECT post, SUM(salary) as total_salary " \
                            "FROM staff " \
                            "GROUP BY post;" 
        cursor.execute(select_total_salary)
        connection.commit()
        result = cursor.fetchall()

        print("Cуммарная зп по каждой специальности.")
        for row in result:
            print(row) 

# Найдите кол-во сотрудников с специальностью (post) «Рабочий» в возрасте от 24 до 49 лет включительно.
        select_emloyee_count = "SELECT COUNT(*) AS employee_count " \
                            "FROM staff " \
                            "WHERE post = 'Рабочий' AND age BETWEEN 24 AND 49;" 
        cursor.execute(select_emloyee_count)
        connection.commit()
        result = cursor.fetchall()

        print("Количество сотрудников с специальностью «Рабочий» в возрасте от 24 до 49 лет")
        for row in result:
            print(row) 
# Найдите количество специальностей
        select_post_count = "SELECT COUNT(DISTINCT post) AS specialty_count " \
                            "FROM staff;" 
        cursor.execute(select_post_count)
        connection.commit()
        result = cursor.fetchall()

        print("Количество специальностей")
        for row in result:
            print(row) 
# Выведите специальности, у которых средний возраст сотрудников меньше 30 лет
        select_emloyee_avg = "SELECT post " \
                            "FROM staff " \
                            "GROUP BY post " \
                            "HAVING AVG(age) < 30;" 
        cursor.execute(select_emloyee_avg)
        connection.commit()
        result = cursor.fetchall()

        print("Специальности, у которых средний возраст сотрудников меньше 30 лет")
        for row in result:
            print(row) 
# Внутри каждой должности вывести ТОП-2 по ЗП (2 самых высокооплачиваемых сотрудника по ЗП внутри каждой должности)  
        select_salary_rank = "SELECT post, firstName, lastName, salary " \
                            "FROM ( " \
                            "SELECT post, firstName, lastName, salary, " \
                                    "ROW_NUMBER() OVER (PARTITION BY post ORDER BY salary DESC) AS position " \
                            "FROM staff " \
                            ") AS ranked_staff " \
                            "WHERE position <= 2;" 
        cursor.execute(select_salary_rank)
        connection.commit()
        result = cursor.fetchall()

        print("Топ 2 сотрудников по ЗП")
        for row in result:
            print(row) 
          
    finally:
        connection.close()


except Exception as ex:
    print("Disconect")
    print(ex)