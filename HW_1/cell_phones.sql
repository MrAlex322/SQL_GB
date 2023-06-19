-- 1)Создайте таблицу с мобильными телефонами, 
-- используя графический интерфейс. Заполните БД данными
-- CREATE TABLE cell_phones_table
-- (
-- Id INT PRIMARY KEY AUTO_INCREMENT,
-- ProductName varchar(20),
-- Manufacture varchar(20),
-- ProductCount int,
-- Price int
-- );

-- insert cell_phones_table (ProductName, Manufacture, ProductCount, Price)
-- values
-- ('Iphone X', 'Apple', 3, 76000),
-- ('Iphone 8', 'Apple', 2, 54000),
-- ('Iphone 7', 'Apple', 6, 40000),
-- ('Sumsung S9', 'Sumsung', 2, 64000),
-- ('Sumsung S8', 'Sumsung', 1, 44000),
-- ('P20 Pro', 'Huawei', 5, 36000)								
-- ;

-- 2)Выведите название, производителя и цену для товаров, количество которых превышает 2

select ProductName, Manufacture, Price 
from cell_phones_table
where ProductCount > 2;

-- 3) Выведите весь ассортимент товаров марки “Samsung”
select ProductName, Manufacture, Price 
from cell_phones_table
where Manufacture = "Sumsung";
