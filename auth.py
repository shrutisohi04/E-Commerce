from email_send import sendResetOTPOnEmail
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor


def loginAdminUser(cursor: MySQLCursor) -> int:
    email = input("Enter admin email = ").lower()
    password = input("Enter admin password = ")
    sql_query = f"""
    SELECT * FROM 
    users
    WHERE 
    email='{email}' and password='{password}' and admin=1
    """
    cursor.execute(sql_query)
    result = cursor.fetchall()
    if len(result) == 0:
        print("Wrong username/password")
        return 0
    else:
        print("Login Successfull")
        return result[0][0]


def loginUser(cursor: MySQLCursor) -> int:
    email = input("Enter your email = ").lower()
    password = input("Enter password = ")
    sql_query = f"""
    SELECT * FROM 
    users
    WHERE 
    email='{email}' and password='{password}'
    """
    cursor.execute(sql_query)
    result = cursor.fetchall()
    if len(result) == 0:
        print("Wrong username/password")
        return 0
    else:
        print(result)
        print("Login Successfull")
        return result[0][0]


def resetPassword(mydb: MySQLConnection, cursor: MySQLCursor):
    user_email = input("Enter email = ").lower()
    sql_query = f"SELECT * FROM users WHERE email='{user_email}'"
    cursor.execute(sql_query)
    authResult = cursor.fetchone()
    if authResult == None:
        print("Email does not exists")
    else:
        generated_otp = sendResetOTPOnEmail(user_email)
        chances = 3
        while True:
            user_otp = int(input("Enter your OTP to reset your password = "))
            if user_otp != generated_otp:
                print("Invalid OTP, try again.\n")
                chances -= 1
            if chances == 0:
                print("Too many tries, please try again")
                break
            if user_otp == generated_otp:
                new_password = input("Enter new password = ")
                sql_query = f"UPDATE users SET password='{new_password}' WHERE user_id={authResult[0]}"
                cursor.execute(sql_query)
                mydb.commit()
                print("Password has been reset")
                break


def createAccount(mydb: MySQLConnection, cursor: MySQLCursor):
    name = input("Enter name = ").title()
    email = input("Enter email = ").lower()
    phone = int(input("Enter phonenumber = "))
    gender = input("Enter gender = ").title()
    password = input("Enter password = ")
    sql_query = f"""
    SELECT * FROM
    users
    WHERE
    email='{email}'
    """
    cursor.execute(sql_query)
    result = cursor.fetchall()
    if len(result) == 0:
        sql_query = f"""
        INSERT INTO users
        (name,email,phone,gender,password) 
        VALUES 
        ('{name}','{email}',{phone},'{gender}','{password}')
        """
        cursor.execute(sql_query)
        mydb.commit()
        print(f"User with Email ({email}) created successfully")

    else:
        print("Account with this email already exists")
