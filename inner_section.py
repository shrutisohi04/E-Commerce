from mysql.connector.cursor import MySQLCursor
from mysql.connector.connection import MySQLConnection


def printInnerMenu() -> int:
    print("\n1. Show products")
    print("2. Show my orders")
    print("3. Add product to cart")
    print("4. Show my cart")
    print("5. Place order in my cart")
    print("6. Create address")
    print("7. View my addresses")
    print("8. Exit")
    choice = int(input("Enter your choice = "))
    return choice


def createAddress(mydb: MySQLConnection, cursor: MySQLCursor, userId: int):
    address = input("Enter address = ").title()
    landmark = input("Enter landmark = ").title()
    city = input("Enter city = ").title()
    state = input("Enter state = ").title()
    pincode = int(input("Enter pincode = "))
    sql_query = f"""
    INSERT INTO address
    (user_id,address,landmark,city,state,pincode)
    VALUES
    ('{userId}','{address}','{landmark}','{city}','{state}','{pincode}')
    """
    cursor.execute(sql_query)
    mydb.commit()
    print("Address added successfully")


def viewAddress(cursor: MySQLCursor, userId: int):
    sql_query = f"""
    SELECT * FROM
    address
    WHERE
    user_id={userId}
    """
    cursor.execute(sql_query)
    result = cursor.fetchall()
    if len(result) == 0:
        print("You have not added any address")
    else:
        for index, address in enumerate(result):
            print(
                f"{index+1}. {address[2]}, {address[3]}, {address[4]}, {address[5]}, {address[6]}"
            )


def viewOrders(cursor: MySQLCursor, userId: int):
    sql_query = f"select orders.quantity,orders.amount,orders.payment_type,products.name from orders JOIN products ON orders.product_id=products.product_id WHERE user_id={userId}"
    cursor.execute(sql_query)
    orderResult = cursor.fetchall()
    if len(orderResult) == 0:
        print("No orders found")
    else:
        for index, order in enumerate(orderResult):
            print(
                f"{index+1}. {order[3]} (Rs.{order[1]}) ({order[0]} quantity) ({order[2]})"
            )


def placeOrdersInCart(mydb: MySQLConnection, cursor: MySQLCursor, userId: int):
    sql_query = f"select cartitems.quantity,cart.user_id,products.product_id,products.price,cartitems.cart_item_id FROM cartitems JOIN cart ON cartitems.cart_id=cart.cart_id JOIN products ON cartitems.product_id=products.product_id WHERE cart.user_id={userId}"
    cursor.execute(sql_query)
    cartResult = cursor.fetchall()
    if len(cartResult) == 0:
        print("No products found in your cart, cannot order anything")
    else:
        sql_query = f"SELECT * FROM address WHERE user_id={userId}"
        cursor.execute(sql_query)
        addressResult = cursor.fetchall()
        if len(addressResult) == 0:
            print("Cannot order, because you dont have any address added")
        else:
            print("SELECT ADDRESS FROM BELOW")
            for index, add in enumerate(addressResult):
                print(f"{index+1}. {add[2]}, {add[3]}, {add[4]}, {add[5]}, {add[6]}")
            address_id = addressResult[int(input("Choose address = ")) - 1]
            payment_type = input("Enter payment type (Cash/Card/UPI) = ").title()
            for cart in cartResult:
                sql_query = f"INSERT INTO orders (user_id,product_id,address_id,quantity,amount,payment_type) VALUES ({cart[1]},{cart[2]},{address_id[0]},{cart[0]},{int(cart[3])*int(cart[0])},'{payment_type}')"
                cursor.execute(sql_query)
                mydb.commit()
                sql_query = f"SELECT stock FROM products WHERE product_id={cart[2]}"
                cursor.execute(sql_query)
                productQuantity = cursor.fetchone()[0]
                productQuantity -= int(cart[0])
                sql_query = f"UPDATE products SET stock={productQuantity} WHERE product_id={cart[2]}"
                cursor.execute(sql_query)
                mydb.commit()
                sql_query = f"DELETE FROM cartitems WHERE cart_item_id={cart[4]}"
                cursor.execute(sql_query)
                mydb.commit()


def viewProductsInMyCart(cursor: MySQLCursor, userId: int):
    sql_query = f"select cartitems.quantity,cart.user_id,products.name,products.price FROM cartitems JOIN cart ON cartitems.cart_id=cart.cart_id JOIN products ON cartitems.product_id=products.product_id WHERE cart.user_id={userId}"
    cursor.execute(sql_query)
    cartResult = cursor.fetchall()
    if len(cartResult) == 0:
        print("No products found in your cart")
    else:
        for index, c in enumerate(cartResult):
            print(f"{index+1}. {c[2]} (Rs.{c[3]} X {c[0]})")


def addProductToCart(mydb: MySQLConnection, cursor: MySQLCursor, userId: int):
    product_name = input("Enter product name = ")
    sql_query = f"""
    SELECT * FROM
    products
    WHERE
    name='{product_name}'
    """
    cursor.execute(sql_query)
    productResult = cursor.fetchone()
    if productResult == None:
        print("No products found")
    else:
        print(f"The price of {product_name} is Rs.{productResult[2]}")
        sql_query = f"SELECT * FROM cart WHERE user_id={userId}"
        cursor.execute(sql_query)
        cartResult = cursor.fetchone()
        if cartResult == None:
            sql_query = f"INSERT INTO cart (user_id) VALUES ({userId})"
            cursor.execute(sql_query)
            mydb.commit()
        # ....
        sql_query = f"SELECT * FROM cart WHERE user_id={userId}"
        cursor.execute(sql_query)
        cartResult = cursor.fetchone()
        sql_query = f"SELECT * FROM cartitems WHERE cart_id={cartResult[0]}"
        cursor.execute(sql_query)
        result = cursor.fetchone()
        if result == None:
            quantity = int(input(f"Enter quantity ({productResult[3]} left) = "))
            sql_query = f"INSERT INTO cartitems (cart_id,product_id,quantity) VALUES ({cartResult[0]},{productResult[0]},{quantity})"
            cursor.execute(sql_query)
            mydb.commit()
            print(f"{product_name} has been added to your cart")
        else:
            new_quantity = int(input("Enter new quantity = "))
            sql_query = f"UPDATE cartitems SET quantity={new_quantity} WHERE cart_id={cartResult[0]} and product_id={productResult[0]}"
            cursor.execute(sql_query)
            mydb.commit()
            print(f"{product_name} in your cart has been updated")
