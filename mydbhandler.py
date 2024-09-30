import mysql.connector

# Function to establish a connection to the MySQL database
def create_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="script",
        password="password",
        database="Food Delivery"
    )
    return connection

# Function to create a new menu item
def add_to_menu():
    name = input("Enter the name of the menu item: ")
    price = float(input("Enter the price of the menu item: "))
    quantity = int(input("Enter the quantity of the menu item: "))

    connection = create_connection()
    cursor = connection.cursor()

    sql = "INSERT INTO Menu (name, price, quantity) VALUES (%s, %s, %s)"
    values = (name, price, quantity)

    cursor.execute(sql, values)
    connection.commit()

    print("Menu item added successfully!")

# Function to add a menu item to an order
def add_to_order():
    menu_item_id = int(input("Enter the ID of the menu item: "))
    order_id = int(input("Enter the ID of the order: "))

    connection = create_connection()
    cursor = connection.cursor()

    sql = "INSERT INTO Orders_Menu_Items (menu_item_id, order_id) VALUES (%s, %s)"
    values = (menu_item_id, order_id)

    cursor.execute(sql, values)
    connection.commit()

    print("Menu item added to the order successfully!")

# Function to set rating for an existing order
def set_rating():
    order_id = int(input("Enter the ID of the order: "))
    rating = float(input("Enter the rating for the order: "))

    connection = create_connection()
    cursor = connection.cursor()

    sql = "UPDATE Orders SET rating = %s WHERE id = %s"
    values = (rating, order_id)

    cursor.execute(sql, values)
    connection.commit()

    print("Rating set successfully!")



def strange_things_happen():
    connection = create_connection()
    cursor = connection.cursor()

    # Select clients who have an order of another client as their current_order
    sql = """
    SELECT c1.id, c1.name
    FROM clients c1
    WHERE c1.current_order IN (
        SELECT DISTINCT o.id
        FROM Orders o
        INNER JOIN clients c2 ON o.client_id = c2.id
        WHERE c1.id <> c2.id
    )
    """

    SELECT c1.id, c1.name FROM clients c1 INNER JOIN orders o ON c1.current_order = o.id AND o.client_id <> c1.id
    cursor.execute(sql)
    result = cursor.fetchall()

    if result:
        print("Clients who have an order of another client as their current_order:")
        for row in result:
            print(f"Client ID: {row[0]}, Name: {row[1]}")
    else:
        print("No such clients found.")


# Function to list orders paid by a card whose owner is not the client who made the order
def get_foreign_paid_orders():
    connection = create_connection()
    cursor = connection.cursor()

    # Select orders paid by a card whose owner is not the client who made the order
    sql = """
    SELECT o.id, o.client_id, p.card_id
    FROM Orders o
    INNER JOIN payment_info p ON o.id = p.order_id
    INNER JOIN card_info c ON p.card_id = c.id
    WHERE c.owner_id <> o.client_id
    """

    cursor.execute(sql)
    result = cursor.fetchall()

    if result:
        print("Orders paid by a card whose owner is not the client who made the order:")
        for row in result:
            print(f"Order ID: {row[0]}, Client ID: {row[1]}, Card ID: {row[2]}")
    else:
        print("No such orders found.")

# Function to decrease checkout price for orders with a specific coupon
def apply_coupon():
    coupon_code = input("Enter the coupon code (e.g., SALE15 for 15% off): ")
    coupon_percentage = int(coupon_code.replace('SALE', ''))  # Extracting the percentage from the coupon code

    connection = create_connection()
    cursor = connection.cursor()

    # Update the checkout price for orders with the specified coupon
    sql = """
    UPDATE payment_info p
    INNER JOIN Coupons c ON p.Coupon_ifused = c.id
    SET p.checkout = p.checkout - (p.checkout * %s / 100)
    WHERE c.code = %s
    """

    values = (coupon_percentage, coupon_code)
    cursor.execute(sql, values)
    connection.commit()

    print(f"Checkout price decreased by {coupon_percentage}% for orders with {coupon_code} coupon.")

# Function to get pairs of clients who have cards with the same encrypted card number
def get_card_duplicates():
    connection = create_connection()
    cursor = connection.cursor()

    # Select pairs of clients who have cards with the same encrypted card number
    sql = """
    SELECT ci1.owner_id, ci2.owner_id, ci1.card_number_encrypted
    FROM card_info ci1
    INNER JOIN card_info ci2 ON ci1.card_number_encrypted = ci2.card_number_encrypted AND ci1.owner_id <> ci2.owner_id
    """

    cursor.execute(sql)
    result = cursor.fetchall()

    if result:
        print("Pairs of clients who have cards with the same encrypted card number:")
        for row in result:
            print(f"Client ID 1: {row[0]}, Client ID 2: {row[1]}, Encrypted Card Number: {row[2]}")
    else:
        print("No such pairs found.")

# Function to list couriers for a given branch ID
def get_couriers_for_branch():
    branch_id = int(input("Enter the branch ID: "))
    connection = create_connection()
    cursor = connection.cursor()

    # Select couriers for the given branch ID
    sql = """
    SELECT id, name
    FROM Courier
    WHERE branch = %s
    """

    cursor.execute(sql, (branch_id,))
    result = cursor.fetchall()

    if result:
        print(f"Couriers for Branch ID {branch_id}:")
        for row in result:
            print(f"Courier ID: {row[0]}, Name: {row[1]}")
    else:
        print("No couriers found for the given branch.")


# Function to list orders with the same address as their branches
def quick_delivery():
    connection = create_connection()
    cursor = connection.cursor()

    # Select orders with the same address as their branches
    sql = """
    SELECT o.id, o.address, o.branch_id AS branch_id
    FROM Orders o
    INNER JOIN branches b ON o.address = b.address
    WHERE o.branch_id = b.id
    """

    cursor.execute(sql)
    result = cursor.fetchall()

    if result:
        print("Orders with the same address as their branches:")
        for row in result:
            print(f"Order ID: {row[0]}, Address: {row[1]}, Branch ID: {row[2]}")
    else:
        print("No such orders found.")




# Function to decrypt card number based on card ID
def get_card_number():
    card_id = int(input("Enter the card ID to decrypt: "))
    connection = create_connection()
    cursor = connection.cursor()

    # Retrieve encrypted card number based on card ID
    sql = """
    SELECT AES_DECRYPT(card_number_encrypted, 'password') AS decrypted_card_number
    FROM card_info
    WHERE id = %s
    """

    cursor.execute(sql, (card_id,))
    result = cursor.fetchone()

    if result:
        decrypted_card_number = result[0]
        print(f"Decrypted Card Number for Card ID {card_id}: {decrypted_card_number.decode()}")
    else:
        print("Card ID not found or card number not available.")



# Function to register a new client according to the database structure
def register_new_client():
    connection = create_connection()
    cursor = connection.cursor()

    name = input("Enter your name: ")
    # Capture other necessary client information
    # For example: address, contact details, etc.

    # Example SQL command to insert a new client
    sql = "INSERT INTO clients (name) VALUES (%s)"
    values = (name,)
    
    cursor.execute(sql, values)
    connection.commit()

    print("New client registered successfully!")


def get_menu_item_price(item_id):
    connection = create_connection()
    cursor = connection.cursor()

    # Check if the menu item with the given ID exists
    check_sql = "SELECT * FROM Menu WHERE id = %s"
    cursor.execute(check_sql, (item_id,))
    result = cursor.fetchone()

    if result:
        # If the menu item exists, retrieve its price
        price_sql = "SELECT price FROM Menu WHERE id = %s"
        cursor.execute(price_sql, (item_id,))
        price = cursor.fetchone()[0]  # Assuming price is in the first column
        return price
    else:
        return 0;

# Function to create a new order
def create_new_order():
    connection = create_connection()
    cursor = connection.cursor()

    is_registered = input("Are you a registered client? (yes/no): ").lower()

    if is_registered == 'yes':
        client_id = int(input("Enter your client ID: "))  # Assuming the client knows their ID
    elif is_registered == 'no':
        register_new_client()  # Call the function to register a new client
        # Fetch the newly registered client's ID and assign it to 'client_id'
        # Example: client_id = get_newly_registered_client_id() 
        client_id = 123  # Replace this with the actual ID of the newly registered client
    else:
        print("Invalid input. Please enter 'yes' or 'no'.")
        return

    address = str(input("Please enter your address: "))

    # Gather information about the order
    # For example: branch_id, courier_id, address, etc.
    order_price = 0
    # Example SQL command to insert a new order
    while(True):
        menu_item_id = int(input("Enter the ID of the menu item or 0 if wanna exit : "))
        if (menu_item_id == 0):
            break
        order_price += get_menu_item_price(menu_item_id)
        if (order_price == 0):
            print("Item in Menu Not found")

    sql = """
    INSERT INTO Orders (client_id, address, status, price)
    VALUES (%s, %s, %s, %s)
    """
    values = (client_id, address, 'Pending', order_price)
    
    cursor.execute(sql, values)
    connection.commit()

    print("New order created successfully!")


def list_all_clients():
    connection = create_connection()
    cursor = connection.cursor()

    # Select all clients from the clients table
    sql = "SELECT id, name FROM clients"

    cursor.execute(sql)
    result = cursor.fetchall()

    if result:
        print("All Clients: \n")
        for row in result:
            print(f"Client ID: {row[0]}, Name: {row[1]}")
        print("\n")
    else:
        print("No clients found.")

# Function to list available operations
def list_operations():
    print("Available Operations:")
    print("1. Add to Menu")
    print("2. Add to Order")
    print("3. Set Rating")
    print("4. strange_things_happen")
    print("5. get_foreign_paid_orders")
    print("6. apply_coupon")
    print("7. get_card_duplicates")
    print("8. get_couriers_for_branch")
    print("9. quick_delivery")
    print("10. get_card_number")
    print("------------------- \n")
    print("11. create_new_order")
    print("12. register_new_client")
    print("13. list_all_clients")
# Main program loop
while True:
    list_operations()
    operation = int(input("Enter the operation number (or 0 to exit): "))

    if operation == 0:
        break
    elif operation == 1:
        add_to_menu()
    elif operation == 2:
        add_to_order()
    elif operation == 3:
        set_rating()
    elif operation == 4:
        strange_things_happen()
    elif operation == 5:
        get_foreign_paid_orders()
    elif operation == 6:
        apply_coupon()
    elif operation == 7:
        get_card_duplicates()
    elif operation == 8:
        get_couriers_for_branch()
    elif operation == 9:
        quick_delivery()
    elif operation == 10:
        get_card_number()
    elif operation == 11:
        create_new_order()
    elif operation == 12:
        register_new_client()
    elif operation == 13:
        list_all_clients()
    else:
        print("Invalid operation number. Please try again.")