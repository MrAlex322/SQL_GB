# Урок 4. SQL – работа с несколькими таблицами

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
        cursor.execute("DROP TABLE IF EXISTS cats;")
        cursor.execute("DROP TABLE IF EXISTS shops;")
        # create table shops
        create_query_shops = "CREATE TABLE shops (" \
                             "id INT," \
                             "shopname VARCHAR(100)," \
                             "PRIMARY KEY (id));"
        cursor.execute(create_query_shops)
        print("Table create 1")
        connection.commit()
        # create table cats
        create_query_cats = "CREATE TABLE cats (" \
                            "name VARCHAR(100)," \
                            "id INT," \
                            "PRIMARY KEY (id)," \
                            "shops_id INT," \
                            "CONSTRAINT fk_cats_shops_id FOREIGN KEY (shops_id) " \
                            "REFERENCES shops (id));"
        cursor.execute(create_query_cats)
        print("Table create 2")
        connection.commit()
        # insert table shops
        insert_query_shops = "INSERT INTO shops " \
                             "VALUES " \
                             "(1, 'Четыре лапы')," \
                             "(2, 'Мистер Зоо')," \
                             "(3, 'МурзиЛЛа')," \
                             "(4, 'Кошки и собаки');"
        cursor.execute(insert_query_shops)
        connection.commit()
        print("Insert Successfully 1")
        # insert table cats
        insert_query_cats = "INSERT INTO cats " \
                            "VALUES " \
                            "('Murzik', 1, 1)," \
                            "('Nemo', 2, 2)," \
                            "('Vicont', 3, 1)," \
                            "('Zuza', 4, 3);"
        cursor.execute(insert_query_cats)
        connection.commit()
        print("Insert Successfully 2")

        # Вывести всех котиков по магазинам по id (условие соединения shops.id = cats.shops_id)
        select_query_cats_shops = "SELECT cats.name, shops.shopname " \
                                  "FROM cats " \
                                  "JOIN shops ON shops.id = cats.shops_id"
        cursor.execute(select_query_cats_shops)
        cats_shops = cursor.fetchall()
        print("All Cats by Shops:")
        for row in cats_shops:
            print(f"Cat: {row['name']}, Shop: {row['shopname']}")
        print()
        
        # Вывести магазин, в котором продается кот "Мурзик" (первый способ)
        select_query_shop_by_cat = "SELECT shops.shopname " \
                                   "FROM cats " \
                                   "JOIN shops ON shops.id = cats.shops_id " \
                                   "WHERE cats.name = 'Мурзик'"
        cursor.execute(select_query_shop_by_cat)
        shop_by_cat = cursor.fetchone()
        if shop_by_cat:
            print(f"Shop where 'Мурзик' is sold: {shop_by_cat['shopname']}")
        else:
            print("'Мурзик' is not sold in any shop")
        print()
        
        # Вывести магазин, в котором продается кот "Murzik" (второй способ)
        select_query_shop_by_cat_subquery = "SELECT shopname " \
                                            "FROM shops " \
                                            "WHERE id = (" \
                                            "SELECT shops_id " \
                                            "FROM cats " \
                                            "WHERE name = 'Murzik')"
        cursor.execute(select_query_shop_by_cat_subquery)
        shop_by_cat_subquery = cursor.fetchone()
        if shop_by_cat_subquery:
            print(f"Shop where 'Мурзик' is sold (using subquery): {shop_by_cat_subquery['shopname']}")
        else:
            print("'Мурзик' is not sold in any shop (using subquery)")
        print()
        
        # Вывести магазины, в которых НЕ продаются коты "Murzik" и "Zuza"
        select_query_shops_without_cats = "SELECT shopname " \
                                          "FROM shops " \
                                          "WHERE id NOT IN (" \
                                          "SELECT shops_id " \
                                          "FROM cats " \
                                          "WHERE name IN ('Murzik', 'Zuza'))"
        cursor.execute(select_query_shops_without_cats)
        shops_without_cats = cursor.fetchall()
        print("Shops without 'Мурзик' and 'Zuza':")
        for row in shops_without_cats:
            print(row['shopname'])
    finally:
        connection.close()

except Exception as ex:
    print("Disconnect")
    print(ex)
