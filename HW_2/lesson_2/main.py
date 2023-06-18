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
        cursor.execute("drop table if exists connect;")
        #create table
        create_query =  "create table if not exists connect (" \
	                    "id INT primary key auto_increment," \
                        "firstName varchar(45));" 
        cursor.execute(create_query)
        print("table create")
        connection.commit()

        #insert table
        insert_query = "insert connect (firstNAme)" \
                        "values ('Антон'), ('Alex'), ('Иван'), ('Dima');"
        cursor.execute(insert_query)
        connection.commit()
        print("Insert Successfully")

        #update table
        update_query = "update connect set firstNAme = 'Mike' where id = 1;" 
        cursor.execute(update_query)
        connection.commit()
        print("update Successfully")

        #delete table
        delete_query = "delete from connect where id = 1;" 
        cursor.execute(delete_query)
        connection.commit()
        print("delete Successfully")

        #select table
        select_query = "select * from connect;" 
        cursor.execute(select_query)
        rows = cursor.fetchall()
        for row in rows:
            print(row)


    finally:
        connection.close()


except Exception as ex:
    print("Disconect")
    print(ex)