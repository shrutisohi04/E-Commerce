from mysql.connector.cursor import MySQLCursor
from mysql.connector.connection import MySQLConnection


def createTables(dbConnection: MySQLConnection, cursor: MySQLCursor):
    createUserTable(dbConnection, cursor)
    createAddressTable(dbConnection, cursor)
    createProductsTable(dbConnection, cursor)
    createOrdersTable(dbConnection, cursor)
    createCartsTable(dbConnection, cursor)
    createCartItemsTable(dbConnection, cursor)


def createUserTable(dbConnection: MySQLConnection, cursor: MySQLCursor):
    sql_query = "CREATE TABLE IF NOT EXISTS users(user_id int auto_increment, name varchar(100) NOT NULL, email varchar(100) NOT NULL UNIQUE, phone BIGINT NOT NULL UNIQUE, gender VARCHAR(10) NOT NULL, password varchar(30) NOT NULL, admin bool DEFAULT 0, PRIMARY KEY(user_id))"
    cursor.execute(sql_query)
    sql_query = "SELECT * FROM users WHERE admin=1"
    cursor.execute(sql_query)
    result = cursor.fetchall()
    if len(result) == 0:
        print("-------WELCOME TO ECOMMERCE-------")
        print("SET YOUR ADMIN DATA\n")
        name = input("Enter admin name = ").title()
        email = input("Enter admin email = ").lower()
        phone = int(input("Enter phonenumber = "))
        gender = input("Enter gender = ").title()
        password = input("Enter password = ")
        sql_query = f"""INSERT INTO 
        users 
        (name,email,phone,gender,password,admin) 
        VALUES 
        ('{name}','{email}',{phone},'{gender}','{password}',1)"""
        cursor.execute(sql_query)
    dbConnection.commit()


def createAddressTable(dbConnection: MySQLConnection, cursor: MySQLCursor):
    sql_query = """CREATE TABLE IF NOT EXISTS address(
        address_id int auto_increment, 
        user_id int NOT NULL, 
        address VARCHAR(100) NOT NULL, 
        landmark VARCHAR(30) NOT NULL, 
        city VARCHAR(30) NOT NULL, 
        state VARCHAR(20) NOT NULL, 
        pincode int NOT NULL, 
        PRIMARY KEY (address_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id))"""
    cursor.execute(sql_query)
    dbConnection.commit()


def createProductsTable(dbConnection: MySQLConnection, cursor: MySQLCursor):
    sql_query = """CREATE TABLE IF NOT EXISTS products(
        product_id int auto_increment, 
        name varchar(100) NOT NULL UNIQUE,
        price int NOT NULL,
        stock int NOT NULL,
        PRIMARY KEY (product_id))"""
    cursor.execute(sql_query)
    dbConnection.commit()


def createOrdersTable(dbConnection: MySQLConnection, cursor: MySQLCursor):
    sql_query = """CREATE TABLE IF NOT EXISTS orders(
        order_id int auto_increment, 
        user_id int NOT NULL, 
        product_id int NOT NULL, 
        address_id int NOT NULL, 
        quantity int NOT NULL,
        amount int NOT NULL,
        payment_type VARCHAR(20) NOT NULL,
        PRIMARY KEY (order_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id),
        FOREIGN KEY (address_id) REFERENCES address(address_id))"""
    cursor.execute(sql_query)
    dbConnection.commit()


def createCartsTable(dbConnection: MySQLConnection, cursor: MySQLCursor):
    sql_query = """CREATE TABLE IF NOT EXISTS cart(
        cart_id int auto_increment, 
        user_id int NOT NULL, 
        PRIMARY KEY (cart_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id))"""
    cursor.execute(sql_query)
    dbConnection.commit()


def createCartItemsTable(dbConnection: MySQLConnection, cursor: MySQLCursor):
    sql_query = """CREATE TABLE IF NOT EXISTS cartitems(
        cart_item_id int auto_increment, 
        cart_id int NOT NULL, 
        product_id int NOT NULL,
        quantity int NOT NULL, 
        PRIMARY KEY (cart_item_id),
        FOREIGN KEY (cart_id) REFERENCES cart(cart_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id))"""
    cursor.execute(sql_query)
    dbConnection.commit()
