from mysql.connector.cursor import MySQLCursor
import mysql.connector
from mysql.connector.connection import MySQLConnection
from settings import my_connection
import db
import auth
from inner_section import *
import admin


def checkConnection() -> MySQLConnection:
    try:
        mydb = mysql.connector.connect(**my_connection)
        mycursor = mydb.cursor()
        mycursor.execute("CREATE DATABASE IF NOT EXISTS ecommerce")
        mydb.disconnect()
        mydb = mysql.connector.connect(
            **my_connection,
            database="ecommerce",
        )
        return mydb
    except mysql.connector.DatabaseError:
        raise Exception("Cannot connect to database")
    except:
        raise Exception("Some unknown error occurred")


def authMenu() -> int:
    print("\n1. Login")
    print("2. Admin Login")
    print("3. Create Account")
    print("4. Reset Password")
    print("5. Exit")
    choice = int(input("Enter your choice = "))
    return choice


def innerSection(mydb: MySQLConnection, cursor: MySQLCursor, userId: int):
    while True:
        choice = printInnerMenu()
        if choice == 1:
            admin.viewAllProducts(cursor)
        elif choice == 2:
            viewOrders(cursor, userId)
        elif choice == 3:
            addProductToCart(mydb, cursor, userId)
        elif choice == 4:
            viewProductsInMyCart(cursor, userId)
        elif choice == 5:
            placeOrdersInCart(mydb, cursor, userId)
        elif choice == 6:
            createAddress(mydb, cursor, userId)
        elif choice == 7:
            viewAddress(cursor, userId)
        elif choice == 8:
            break
        else:
            print("Invalid choice")


try:
    mydb = checkConnection()
    mycursor = mydb.cursor(buffered=True)
    db.createTables(mydb, mycursor)
    while True:
        choice = authMenu()
        if choice == 1:
            user_id = auth.loginUser(mycursor)
            if user_id != 0:
                innerSection(mydb, mycursor, user_id)
        elif choice == 2:
            user_id = auth.loginAdminUser(mycursor)
            if user_id != 0:
                admin.innerAdminSection(mydb, mycursor, user_id)
        elif choice == 3:
            auth.createAccount(mydb, mycursor)
        elif choice == 4:
            auth.resetPassword(mydb, mycursor)
        elif choice == 5:
            print("\nThankyou for using Ecommerce App")
            break
        else:
            print("Invalid Choice")

except Exception as e:
    print(e)
