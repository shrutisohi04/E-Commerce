from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor


def innerAdminMenu() -> int:
    print("\n1. View all users")
    print("2. View all products")
    print("3. Add product")
    print("4. Edit product")
    print("5. Delete product")
    print("6. Exit")
    return int(input("Enter your choice = "))


def innerAdminSection(mydb: MySQLConnection, cursor: MySQLCursor, userId: int):
    while True:
        choice = innerAdminMenu()
        if choice == 1:
            viewAllUsers(cursor)
        elif choice == 2:
            viewAllProducts(cursor)
        elif choice == 3:
            addProduct(mydb, cursor)
        elif choice == 4:
            editProduct(mydb, cursor)
        elif choice == 5:
            deleteProduct(mydb, cursor)
        elif choice == 6:
            break
        else:
            print("Invalid choice")


def viewAllUsers(cursor: MySQLCursor):
    sql_query = f"""
    SELECT * FROM
    users
    WHERE
    admin=0
    """
    cursor.execute(sql_query)
    result = cursor.fetchall()
    if len(result) == 0:
        print("No users found")
    else:
        for index, user in enumerate(result):
            print(
                f"{index+1}. Name = {user[1]}, Email = {user[2]}, Phone = {user[3]}, Gender = {user[4]}"
            )


def viewAllProducts(cursor: MySQLCursor):
    sql_query = f"""
    SELECT * FROM
    products
    """
    cursor.execute(sql_query)
    result = cursor.fetchall()
    if len(result) == 0:
        print("No products found")
    else:
        for index, p in enumerate(result):
            print(f"{index+1}. {p[1]}, Rs.{p[2]}, {p[3]} left")


def addProduct(mydb: MySQLConnection, cursor: MySQLCursor):
    product_name = input("Enter product name = ").title()
    product_price = int(input("Enter product price = "))
    stock = int(input("Enter stock = "))
    sql_query = f"""
    INSERT INTO products
    (name,price,stock)
    VALUES
    ('{product_name}',{product_price},{stock})
    """
    cursor.execute(sql_query)
    mydb.commit()
    print("Product added successfully")


def deleteProduct(mydb: MySQLConnection, cursor: MySQLCursor):
    product_name = input("Enter product name to delete = ").title()
    sql_query = f"SELECT * FROM products WHERE name='{product_name}'"
    cursor.execute(sql_query)
    result = cursor.fetchall()
    if len(result) == 0:
        print("Product does not exists")
    else:
        sql_query = f"DELETE FROM products WHERE name='{product_name}'"
        cursor.execute(sql_query)
        mydb.commit()
        print("Product deleted sucessfully")


def editProduct(mydb: MySQLConnection, cursor: MySQLCursor):
    product_name = input("Enter product name to delete = ").title()
    sql_query = f"SELECT * FROM products WHERE name='{product_name}'"
    cursor.execute(sql_query)
    result = cursor.fetchall()
    if len(result) == 0:
        print("Product does not exists")
    else:
        print("1. Edit name")
        print("2. Edit price")
        print("3. Edit stock")
        choice = int(input("Enter choice = "))
        if choice == 1:
            new_name = input("Enter new product name = ").title()
            sql_query = (
                f"UPDATE products SET name='{new_name}' WHERE name='{product_name}'"
            )
            cursor.execute(sql_query)
            mydb.commit()
            print("Name updated successfully")
        elif choice == 2:
            new_price = int(input("Enter new product price = "))
            sql_query = (
                f"UPDATE products SET price={new_price} WHERE name='{product_name}'"
            )
            cursor.execute(sql_query)
            mydb.commit()
            print("Price updated successfully")
        elif choice == 3:
            new_stock = int(input("Enter new product stock = "))
            sql_query = (
                f"UPDATE products SET stock={new_stock} WHERE name='{product_name}'"
            )
            cursor.execute(sql_query)
            mydb.commit()
            print("Stock updated successfully")
