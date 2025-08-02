import mysql.connector
from datetime import datetime

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="lab_eq_tracker"
)
print("Connected to MySQL database")

while True:
    print("Lab Equipment Tracker")
    print("1. Chemistry")
    print("2. Physics")
    print("3. Biology")
    print("4. Exit")
    choice = input("Enter choice: ")
    
    if choice == '1':
        while True:
            print("Chemistry Lab")
            print("1. Chemicals")
            print("2. Apparatus")
            print("3. Back")
            chem_choice = input("Enter choice: ")
            
            if chem_choice == '1':
                table = "chem_chemicals"
                lab = "Chemistry"
                category = "Chemicals"
                while True:
                    print(f"{lab} Lab - {category}")
                    print("1. Add Equipment")
                    print("2. View Equipment")
                    print("3. Update Equipment")
                    print("4. Delete Equipment")
                    print("5. Reserve Equipment")
                    print("6. View Reservations")
                    print("7. Back")
                    sub_choice = input("Enter choice: ")
                    
                    if sub_choice == '1':
                        cursor = connection.cursor()
                        cursor.execute(f"SELECT COUNT(*) FROM {table}")
                        count = cursor.fetchone()[0]
                        if count >= 900:
                            print("Cannot add more equipment: ID limit reached")
                            cursor.close()
                            continue
                        name = input("Enter equipment name: ")
                        status = input("Enter status (In Use, Free, Damaged): ")
                        if status not in ["In Use", "Free", "Damaged"]:
                            print("Invalid status! Must be 'In Use', 'Free', or 'Damaged'")
                            cursor.close()
                            continue
                        cursor.execute("SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute(f"INSERT INTO {table} (name, status) VALUES (%s, %s)", (name, status))
                        connection.commit()
                        print("Equipment added successfully")
                        cursor.close()
                    
                    elif sub_choice == '2':
                        cursor = connection.cursor()
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute(f"SELECT * FROM {table}")
                        results = cursor.fetchall()
                        if results:
                            print(f"\n{lab} - {category} Equipment List:")
                            print("ID | Name | Status")
                            print("-" * 40)
                            for row in results:
                                print(f"{row[0]} | {row[1]} | {row[2]}")
                        else:
                            print(f"No equipment found in {lab} - {category}")
                        cursor.close()
                    
                    elif sub_choice == '3':
                        equipment_id = input("Enter equipment ID to update: ")
                        name = input("Enter new name (or press Enter to keep unchanged): ")
                        status = input("Enter new status (In Use, Free, Damaged, or press Enter to keep unchanged): ")
                        if status and status not in ["In Use", "Free", "Damaged"]:
                            print("Invalid status! Must be 'In Use', 'Free', or 'Damaged'")
                            continue
                        cursor = connection.cursor()
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        query = f"UPDATE {table} SET "
                        updates = []
                        values = []
                        if name:
                            updates.append("name = %s")
                            values.append(name)
                        if status:
                            updates.append("status = %s")
                            values.append(status)
                        if updates:
                            query += ", ".join(updates) + " WHERE id = %s"
                            values.append(equipment_id)
                            cursor.execute(query, values)
                            connection.commit()
                            if cursor.rowcount > 0:
                                print("Equipment updated successfully")
                            else:
                                print("No equipment found with that ID")
                        else:
                            print("No updates provided")
                        cursor.close()
                    
                    elif sub_choice == '4':
                        equipment_id = input("Enter equipment ID to delete: ")
                        cursor = connection.cursor()
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute(f"DELETE FROM {table} WHERE id = %s", (equipment_id,))
                        connection.commit()
                        if cursor.rowcount > 0:
                            print("Equipment deleted successfully")
                        else:
                            print("No equipment found with that ID")
                        cursor.close()
                    
                    elif sub_choice == '5':
                        equipment_id = input("Enter equipment ID to reserve: ")
                        user_name = input("Enter your name: ")
                        reservation_date = input("Enter reservation date (YYYY-MM-DD): ")
                        if not reservation_date or len(reservation_date) != 10 or reservation_date[4] != '-' or reservation_date[7] != '-':
                            print("Invalid date format! Use YYYY-MM-DD")
                            continue
                        cursor = connection.cursor()
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute(f"SELECT status FROM {table} WHERE id = %s", (equipment_id,))
                        result = cursor.fetchone()
                        if not result:
                            print("No equipment found with that ID")
                            cursor.close()
                            continue
                        if result[0] != "Free":
                            print("Equipment is not available for reservation (must be Free)")
                            cursor.close()
                            continue
                        cursor.execute("INSERT INTO reservations (equipment_id, lab, category, user_name, reservation_date) VALUES (%s, %s, %s, %s, %s)",
                                      (equipment_id, lab, category, user_name, reservation_date))
                        cursor.execute(f"UPDATE {table} SET status = 'In Use' WHERE id = %s", (equipment_id,))
                        connection.commit()
                        print("Equipment reserved successfully")
                        cursor.close()
                    
                    elif sub_choice == '6':
                        cursor = connection.cursor()
                        cursor.execute("SHOW TABLES LIKE 'reservations'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute("SELECT reservation_id, equipment_id, user_name, reservation_date FROM reservations WHERE lab = %s AND category = %s", (lab, category))
                        results = cursor.fetchall()
                        if results:
                            print(f"\n{lab} - {category} Reservations:")
                            print("Reservation ID | Equipment ID | User | Date")
                            print("-" * 50)
                            for row in results:
                                print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")
                        else:
                            print(f"No reservations found in {lab} - {category}")
                        cursor.close()
                    
                    elif sub_choice == '7':
                        break
                    else:
                        print("Invalid choice! Please try again.")
            
            elif chem_choice == '2':
                table = "chem_apparatus"
                lab = "Chemistry"
                category = "Apparatus"
                while True:
                    print(f"\n{lab} Lab - {category}")
                    print("1. Add Equipment")
                    print("2. View Equipment")
                    print("3. Update Equipment")
                    print("4. Delete Equipment")
                    print("5. Reserve Equipment")
                    print("6. View Reservations")
                    print("7. Back")
                    sub_choice = input("Enter choice: ")
                    
                    if sub_choice == '1':
                        cursor = connection.cursor()
                        cursor.execute(f"SELECT COUNT(*) FROM {table}")
                        count = cursor.fetchone()[0]
                        if count >= 900:
                            print("Cannot add more equipment: ID limit reached")
                            cursor.close()
                            continue
                        name = input("Enter equipment name: ")
                        status = input("Enter status (In Use, Free, Damaged): ")
                        if status not in ["In Use", "Free", "Damaged"]:
                            print("Invalid status! Must be 'In Use', 'Free', or 'Damaged'")
                            cursor.close()
                            continue
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute(f"INSERT INTO {table} (name, status) VALUES (%s, %s)", (name, status))
                        connection.commit()
                        print("Equipment added successfully")
                        cursor.close()
                    
                    elif sub_choice == '2':
                        cursor = connection.cursor()
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute(f"SELECT * FROM {table}")
                        results = cursor.fetchall()
                        if results:
                            print(f"\n{lab} - {category} Equipment List:")
                            print("ID | Name | Status")
                            print("-" * 40)
                            for row in results:
                                print(f"{row[0]} | {row[1]} | {row[2]}")
                        else:
                            print(f"No equipment found in {lab} - {category}")
                        cursor.close()
                    
                    elif sub_choice == '3':
                        equipment_id = input("Enter equipment ID to update: ")
                        name = input("Enter new name (or press Enter to keep unchanged): ")
                        status = input("Enter new status (In Use, Free, Damaged, or press Enter to keep unchanged): ")
                        if status and status not in ["In Use", "Free", "Damaged"]:
                            print("Invalid status! Must be 'In Use', 'Free', or 'Damaged'")
                            continue
                        cursor = connection.cursor()
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        query = f"UPDATE {table} SET "
                        updates = []
                        values = []
                        if name:
                            updates.append("name = %s")
                            values.append(name)
                        if status:
                            updates.append("status = %s")
                            values.append(status)
                        if updates:
                            query += ", ".join(updates) + " WHERE id = %s"
                            values.append(equipment_id)
                            cursor.execute(query, values)
                            connection.commit()
                            if cursor.rowcount > 0:
                                print("Equipment updated successfully")
                            else:
                                print("No equipment found with that ID")
                        else:
                            print("No updates provided")
                        cursor.close()
                    
                    elif sub_choice == '4':
                        equipment_id = input("Enter equipment ID to delete: ")
                        cursor = connection.cursor()
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute(f"DELETE FROM {table} WHERE id = %s", (equipment_id,))
                        connection.commit()
                        if cursor.rowcount > 0:
                            print("Equipment deleted successfully")
                        else:
                            print("No equipment found with that ID")
                        cursor.close()
                    
                    elif sub_choice == '5':
                        equipment_id = input("Enter equipment ID to reserve: ")
                        user_name = input("Enter your name: ")
                        reservation_date = input("Enter reservation date (YYYY-MM-DD): ")
                        if not reservation_date or len(reservation_date) != 10 or reservation_date[4] != '-' or reservation_date[7] != '-':
                            print("Invalid date format! Use YYYY-MM-DD")
                            continue
                        cursor = connection.cursor()
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute(f"SELECT status FROM {table} WHERE id = %s", (equipment_id,))
                        result = cursor.fetchone()
                        if not result:
                            print("No equipment found with that ID")
                            cursor.close()
                            continue
                        if result[0] != "Free":
                            print("Equipment is not available for reservation (must be Free)")
                            cursor.close()
                            continue
                        cursor.execute("INSERT INTO reservations (equipment_id, lab, category, user_name, reservation_date) VALUES (%s, %s, %s, %s, %s)",
                                      (equipment_id, lab, category, user_name, reservation_date))
                        cursor.execute(f"UPDATE {table} SET status = 'In Use' WHERE id = %s", (equipment_id,))
                        connection.commit()
                        print("Equipment reserved successfully")
                        cursor.close()
                    
                    elif sub_choice == '6':
                        cursor = connection.cursor()
                        cursor.execute("SHOW TABLES LIKE 'reservations'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute("SELECT reservation_id, equipment_id, user_name, reservation_date FROM reservations WHERE lab = %s AND category = %s", (lab, category))
                        results = cursor.fetchall()
                        if results:
                            print(f"\n{lab} - {category} Reservations:")
                            print("Reservation ID | Equipment ID | User | Date")
                            print("-" * 50)
                            for row in results:
                                print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")
                        else:
                            print(f"No reservations found in {lab} - {category}")
                        cursor.close()
                    
                    elif sub_choice == '7':
                        break
                    else:
                        print("Invalid choice! Please try again.")
            
            elif chem_choice == '3':
                break
            else:
                print("Invalid choice! Please try again.")
    
    elif choice == '2':
        while True:
            print("\nPhysics Lab")
            print("1. Measuring Instruments")
            print("2. Optical Instruments")
            print("3. Electrical Instruments")
            print("4. Thermal Instruments")
            print("5. Acoustic Instruments")
            print("6. Back")
            phys_choice = input("Enter choice: ")
            
            if phys_choice == '1':
                table = "phys_measuring_instruments"
                lab = "Physics"
                category = "Measuring Instruments"
                while True:
                    print(f"\n{lab} Lab - {category}")
                    print("1. Add Equipment")
                    print("2. View Equipment")
                    print("3. Update Equipment")
                    print("4. Delete Equipment")
                    print("5. Reserve Equipment")
                    print("6. View Reservations")
                    print("7. Back")
                    sub_choice = input("Enter choice: ")
                    
                    if sub_choice == '1':
                        cursor = connection.cursor()
                        cursor.execute(f"SELECT COUNT(*) FROM {table}")
                        count = cursor.fetchone()[0]
                        if count >= 900:
                            print("Cannot add more equipment: ID limit reached")
                            cursor.close()
                            continue
                        name = input("Enter equipment name: ")
                        status = input("Enter status (In Use, Free, Damaged): ")
                        if status not in ["In Use", "Free", "Damaged"]:
                            print("Invalid status! Must be 'In Use', 'Free', 'Damaged'")
                            cursor.close()
                            continue
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute(f"INSERT INTO {table} (name, status) VALUES (%s, %s)", (name, status))
                        connection.commit()
                        print("Equipment added successfully")
                        cursor.close()
                    
                    elif sub_choice == '2':
                        cursor = connection.cursor()
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute(f"SELECT * FROM {table}")
                        results = cursor.fetchall()
                        if results:
                            print(f"\n{lab} - {category} Equipment List:")
                            print("ID | Name | Status")
                            print("-" * 40)
                            for row in results:
                                print(f"{row[0]} | {row[1]} | {row[2]}")
                        else:
                            print(f"No equipment found in {lab} - {category}")
                        cursor.close()
                    
                    elif sub_choice == '3':
                        equipment_id = input("Enter equipment ID to update: ")
                        name = input("Enter new name (or press Enter to keep unchanged): ")
                        status = input("Enter new status (In Use, Free, Damaged, or press Enter to keep unchanged): ")
                        if status and status not in ["In Use", "Free", "Damaged"]:
                            print("Invalid status! Must be 'In Use', 'Free', 'Damaged'")
                            continue
                        cursor = connection.cursor()
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        query = f"UPDATE {table} SET "
                        updates = []
                        values = []
                        if name:
                            updates.append("name = %s")
                            values.append(name)
                        if status:
                            updates.append("status = %s")
                            values.append(status)
                        if updates:
                            query += ", ".join(updates) + " WHERE id = %s"
                            values.append(equipment_id)
                            cursor.execute(query, values)
                            connection.commit()
                            if cursor.rowcount > 0:
                                print("Equipment updated successfully")
                            else:
                                print("No equipment found with that ID")
                        else:
                            print("No updates provided")
                        cursor.close()
                    
                    elif sub_choice == '4':
                        equipment_id = input("Enter equipment ID to delete: ")
                        cursor = connection.cursor()
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute(f"DELETE FROM {table} WHERE id = %s", (equipment_id,))
                        connection.commit()
                        if cursor.rowcount > 0:
                            print("Equipment deleted successfully")
                        else:
                            print("No equipment found with that ID")
                        cursor.close()
                    
                    elif sub_choice == '5':
                        equipment_id = input("Enter equipment ID to reserve: ")
                        user_name = input("Enter your name: ")
                        reservation_date = input("Enter reservation date (YYYY-MM-DD): ")
                        if not reservation_date or len(reservation_date) != 10 or reservation_date[4] != '-' or reservation_date[7] != '-':
                            print("Invalid date format! Use YYYY-MM-DD")
                            continue
                        cursor = connection.cursor()
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute(f"SELECT status FROM {table} WHERE id = %s", (equipment_id,))
                        result = cursor.fetchone()
                        if not result:
                            print("No equipment found with that ID")
                            cursor.close()
                            continue
                        if result[0] != "Free":
                            print("Equipment is not available for reservation (must be Free)")
                            cursor.close()
                            continue
                        cursor.execute("INSERT INTO reservations (equipment_id, lab, category, user_name, reservation_date) VALUES (%s, %s, %s, %s, %s)",
                                      (equipment_id, lab, category, user_name, reservation_date))
                        cursor.execute(f"UPDATE {table} SET status = 'In Use' WHERE id = %s", (equipment_id,))
                        connection.commit()
                        print("Equipment reserved successfully")
                        cursor.close()
                    
                    elif sub_choice == '6':
                        cursor = connection.cursor()
                        cursor.execute("SHOW TABLES LIKE 'reservations'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute("SELECT reservation_id, equipment_id, user_name, reservation_date FROM reservations WHERE lab = %s AND category = %s", (lab, category))
                        results = cursor.fetchall()
                        if results:
                            print(f"\n{lab} - {category} Reservations:")
                            print("Reservation ID | Equipment ID | User | Date")
                            print("-" * 50)
                            for row in results:
                                print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")
                        else:
                            print(f"No reservations found in {lab} - {category}")
                        cursor.close()
                    
                    elif sub_choice == '7':
                        break
                    else:
                        print("Invalid choice! Please try again.")
            
            elif phys_choice == '2':
                table = "phys_optical_instruments"
                lab = "Physics"
                category = "Optical Instruments"
                while True:
                    print(f"\n{lab} Lab - {category}")
                    print("1. Add Equipment")
                    print("2. View Equipment")
                    print("3. Update Equipment")
                    print("4. Delete Equipment")
                    print("5. Reserve Equipment")
                    print("6. View Reservations")
                    print("7. Back")
                    sub_choice = input("Enter choice: ")
                    
                    if sub_choice == '1':
                        cursor = connection.cursor()
                        cursor.execute(f"SELECT COUNT(*) FROM {table}")
                        count = cursor.fetchone()[0]
                        if count >= 900:
                            print("Cannot add more equipment: ID limit reached")
                            cursor.close()
                            continue
                        name = input("Enter equipment name: ")
                        status = input("Enter status (In Use, Free, Damaged): ")
                        if status not in ["In Use", "Free", "Damaged"]:
                            print("Invalid status! Must be 'In Use', 'Free', 'Damaged'")
                            cursor.close()
                            continue
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute(f"INSERT INTO {table} (name, status) VALUES (%s, %s)", (name, status))
                        connection.commit()
                        print("Equipment added successfully")
                        cursor.close()
                    
                    elif sub_choice == '2':
                        cursor = connection.cursor()
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute(f"SELECT * FROM {table}")
                        results = cursor.fetchall()
                        if results:
                            print(f"\n{lab} - {category} Equipment List:")
                            print("ID | Name | Status")
                            print("-" * 40)
                            for row in results:
                                print(f"{row[0]} | {row[1]} | {row[2]}")
                        else:
                            print(f"No equipment found in {lab} - {category}")
                        cursor.close()
                    
                    elif sub_choice == '3':
                        equipment_id = input("Enter equipment ID to update: ")
                        name = input("Enter new name (or press Enter to keep unchanged): ")
                        status = input("Enter new status (In Use, Free, Damaged, or press Enter to keep unchanged): ")
                        if status and status not in ["In Use", "Free", "Damaged"]:
                            print("Invalid status! Must be 'In Use', 'Free', 'Damaged'")
                            continue
                        cursor = connection.cursor()
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        query = f"UPDATE {table} SET "
                        updates = []
                        values = []
                        if name:
                            updates.append("name = %s")
                            values.append(name)
                        if status:
                            updates.append("status = %s")
                            values.append(status)
                        if updates:
                            query += ", ".join(updates) + " WHERE id = %s"
                            values.append(equipment_id)
                            cursor.execute(query, values)
                            connection.commit()
                            if cursor.rowcount > 0:
                                print("Equipment updated successfully")
                            else:
                                print("No equipment found with that ID")
                        else:
                            print("No updates provided")
                        cursor.close()
                    
                    elif sub_choice == '4':
                        equipment_id = input("Enter equipment ID to delete: ")
                        cursor = connection.cursor()
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute(f"DELETE FROM {table} WHERE id = %s", (equipment_id,))
                        connection.commit()
                        if cursor.rowcount > 0:
                            print("Equipment deleted successfully")
                        else:
                            print("No equipment found with that ID")
                        cursor.close()
                    
                    elif sub_choice == '5':
                        equipment_id = input("Enter equipment ID to reserve: ")
                        user_name = input("Enter your name: ")
                        reservation_date = input("Enter reservation date (YYYY-MM-DD): ")
                        if not reservation_date or len(reservation_date) != 10 or reservation_date[4] != '-' or reservation_date[7] != '-':
                            print("Invalid date format! Use YYYY-MM-DD")
                            continue
                        cursor = connection.cursor()
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute(f"SELECT status FROM {table} WHERE id = %s", (equipment_id,))
                        result = cursor.fetchone()
                        if not result:
                            print("No equipment found with that ID")
                            cursor.close()
                            continue
                        if result[0] != "Free":
                            print("Equipment is not available for reservation (must be Free)")
                            cursor.close()
                            continue
                        cursor.execute("INSERT INTO reservations (equipment_id, lab, category, user_name, reservation_date) VALUES (%s, %s, %s, %s, %s)",
                                      (equipment_id, lab, category, user_name, reservation_date))
                        cursor.execute(f"UPDATE {table} SET status = 'In Use' WHERE id = %s", (equipment_id,))
                        connection.commit()
                        print("Equipment reserved successfully")
                        cursor.close()
                    
                    elif sub_choice == '6':
                        cursor = connection.cursor()
                        cursor.execute("SHOW TABLES LIKE 'reservations'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute("SELECT reservation_id, equipment_id, user_name, reservation_date FROM reservations WHERE lab = %s AND category = %s", (lab, category))
                        results = cursor.fetchall()
                        if results:
                            print(f"\n{lab} - {category} Reservations:")
                            print("Reservation ID | Equipment ID | User | Date")
                            print("-" * 50)
                            for row in results:
                                print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")
                        else:
                            print(f"No reservations found in {lab} - {category}")
                        cursor.close()
                    
                    elif sub_choice == '7':
                        break
                    else:
                        print("Invalid choice! Please try again.")
            
            elif phys_choice == '3':
                table = "phys_electrical_instruments"
                lab = "Physics"
                category = "Electrical Instruments"
                while True:
                    print(f"\n{lab} Lab - {category}")
                    print("1. Add Equipment")
                    print("2. View Equipment")
                    print("3. Update Equipment")
                    print("4. Delete Equipment")
                    print("5. Reserve Equipment")
                    print("6. View Reservations")
                    print("7. Back")
                    sub_choice = input("Enter choice: ")
                    
                    if sub_choice == '1':
                        cursor = connection.cursor()
                        cursor.execute(f"SELECT COUNT(*) FROM {table}")
                        count = cursor.fetchone()[0]
                        if count >= 900:
                            print("Cannot add more equipment: ID limit reached")
                            cursor.close()
                            continue
                        name = input("Enter equipment name: ")
                        status = input("Enter status (In Use, Free, Damaged): ")
                        if status not in ["In Use", "Free", "Damaged"]:
                            print("Invalid status! Must be 'In Use', 'Free', 'Damaged'")
                            cursor.close()
                            continue
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute(f"INSERT INTO {table} (name, status) VALUES (%s, %s)", (name, status))
                        connection.commit()
                        print("Equipment added successfully")
                        cursor.close()
                    
                    elif sub_choice == '2':
                        cursor = connection.cursor()
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute(f"SELECT * FROM {table}")
                        results = cursor.fetchall()
                        if results:
                            print(f"\n{lab} - {category} Equipment List:")
                            print("ID | Name | Status")
                            print("-" * 40)
                            for row in results:
                                print(f"{row[0]} | {row[1]} | {row[2]}")
                        else:
                            print(f"No equipment found in {lab} - {category}")
                        cursor.close()
                    
                    elif sub_choice == '3':
                        equipment_id = input("Enter equipment ID to update: ")
                        name = input("Enter new name (or press Enter to keep unchanged): ")
                        status = input("Enter new status (In Use, Free, Damaged, or press Enter to keep unchanged): ")
                        if status and status not in ["In Use", "Free", "Damaged"]:
                            print("Invalid status! Must be 'In Use', 'Free', 'Damaged'")
                            continue
                        cursor = connection.cursor()
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        query = f"UPDATE {table} SET "
                        updates = []
                        values = []
                        if name:
                            updates.append("name = %s")
                            values.append(name)
                        if status:
                            updates.append("status = %s")
                            values.append(status)
                        if updates:
                            query += ", ".join(updates) + " WHERE id = %s"
                            values.append(equipment_id)
                            cursor.execute(query, values)
                            connection.commit()
                            if cursor.rowcount > 0:
                                print("Equipment updated successfully")
                            else:
                                print("No equipment found with that ID")
                        else:
                            print("No updates provided")
                        cursor.close()
                    
                    elif sub_choice == '4':
                        equipment_id = input("Enter equipment ID to delete: ")
                        cursor = connection.cursor()
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute(f"DELETE FROM {table} WHERE id = %s", (equipment_id,))
                        connection.commit()
                        if cursor.rowcount > 0:
                            print("Equipment deleted successfully")
                        else:
                            print("No equipment found with that ID")
                        cursor.close()
                    
                    elif sub_choice == '5':
                        equipment_id = input("Enter equipment ID to reserve: ")
                        user_name = input("Enter your name: ")
                        reservation_date = input("Enter reservation date (YYYY-MM-DD): ")
                        if not reservation_date or len(reservation_date) != 10 or reservation_date[4] != '-' or reservation_date[7] != '-':
                            print("Invalid date format! Use YYYY-MM-DD")
                            continue
                        cursor = connection.cursor()
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute(f"SELECT status FROM {table} WHERE id = %s", (equipment_id,))
                        result = cursor.fetchone()
                        if not result:
                            print("No equipment found with that ID")
                            cursor.close()
                            continue
                        if result[0] != "Free":
                            print("Equipment is not available for reservation (must be Free)")
                            cursor.close()
                            continue
                        cursor.execute("INSERT INTO reservations (equipment_id, lab, category, user_name, reservation_date) VALUES (%s, %s, %s, %s, %s)",
                                      (equipment_id, lab, category, user_name, reservation_date))
                        cursor.execute(f"UPDATE {table} SET status = 'In Use' WHERE id = %s", (equipment_id,))
                        connection.commit()
                        print("Equipment reserved successfully")
                        cursor.close()
                    
                    elif sub_choice == '6':
                        cursor = connection.cursor()
                        cursor.execute("SHOW TABLES LIKE 'reservations'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute("SELECT reservation_id, equipment_id, user_name, reservation_date FROM reservations WHERE lab = %s AND category = %s", (lab, category))
                        results = cursor.fetchall()
                        if results:
                            print(f"\n{lab} - {category} Reservations:")
                            print("Reservation ID | Equipment ID | User | Date")
                            print("-" * 50)
                            for row in results:
                                print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")
                        else:
                            print(f"No reservations found in {lab} - {category}")
                        cursor.close()
                    
                    elif sub_choice == '7':
                        break
                    else:
                        print("Invalid choice! Please try again.")
            
            elif phys_choice == '4':
                table = "phys_thermal_instruments"
                lab = "Physics"
                category = "Thermal Instruments"
                while True:
                    print(f"\n{lab} Lab - {category}")
                    print("1. Add Equipment")
                    print("2. View Equipment")
                    print("3. Update Equipment")
                    print("4. Delete Equipment")
                    print("5. Reserve Equipment")
                    print("6. View Reservations")
                    print("7. Back")
                    sub_choice = input("Enter choice: ")
                    
                    if sub_choice == '1':
                        cursor = connection.cursor()
                        cursor.execute(f"SELECT COUNT(*) FROM {table}")
                        count = cursor.fetchone()[0]
                        if count >= 900:
                            print("Cannot add more equipment: ID limit reached")
                            cursor.close()
                            continue
                        name = input("Enter equipment name: ")
                        status = input("Enter status (In Use, Free, Damaged): ")
                        if status not in ["In Use", "Free", "Damaged"]:
                            print("Invalid status! Must be 'In Use', 'Free', 'Damaged'")
                            cursor.close()
                            continue
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute(f"INSERT INTO {table} (name, status) VALUES (%s, %s)", (name, status))
                        connection.commit()
                        print("Equipment added successfully")
                        cursor.close()
                    
                    elif sub_choice == '2':
                        cursor = connection.cursor()
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute(f"SELECT * FROM {table}")
                        results = cursor.fetchall()
                        if results:
                            print(f"\n{lab} - {category} Equipment List:")
                            print("ID | Name | Status")
                            print("-" * 40)
                            for row in results:
                                print(f"{row[0]} | {row[1]} | {row[2]}")
                        else:
                            print(f"No equipment found in {lab} - {category}")
                        cursor.close()
                    
                    elif sub_choice == '3':
                        equipment_id = input("Enter equipment ID to update: ")
                        name = input("Enter new name (or press Enter to keep unchanged): ")
                        status = input("Enter new status (In Use, Free, Damaged, or press Enter to keep unchanged): ")
                        if status and status not in ["In Use", "Free", "Damaged"]:
                            print("Invalid status! Must be 'In Use', 'Free', 'Damaged'")
                            continue
                        cursor = connection.cursor()
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        query = f"UPDATE {table} SET "
                        updates = []
                        values = []
                        if name:
                            updates.append("name = %s")
                            values.append(name)
                        if status:
                            updates.append("status = %s")
                            values.append(status)
                        if updates:
                            query += ", ".join(updates) + " WHERE id = %s"
                            values.append(equipment_id)
                            cursor.execute(query, values)
                            connection.commit()
                            if cursor.rowcount > 0:
                                print("Equipment updated successfully")
                            else:
                                print("No equipment found with that ID")
                        else:
                            print("No updates provided")
                        cursor.close()
                    
                    elif sub_choice == '4':
                        equipment_id = input("Enter equipment ID to delete: ")
                        cursor = connection.cursor()
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute(f"DELETE FROM {table} WHERE id = %s", (equipment_id,))
                        connection.commit()
                        if cursor.rowcount > 0:
                            print("Equipment deleted successfully")
                        else:
                            print("No equipment found with that ID")
                        cursor.close()
                    
                    elif sub_choice == '5':
                        equipment_id = input("Enter equipment ID to reserve: ")
                        user_name = input("Enter your name: ")
                        reservation_date = input("Enter reservation date (YYYY-MM-DD): ")
                        if not reservation_date or len(reservation_date) != 10 or reservation_date[4] != '-' or reservation_date[7] != '-':
                            print("Invalid date format! Use YYYY-MM-DD")
                            continue
                        cursor = connection.cursor()
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute(f"SELECT status FROM {table} WHERE id = %s", (equipment_id,))
                        result = cursor.fetchone()
                        if not result:
                            print("No equipment found with that ID")
                            cursor.close()
                            continue
                        if result[0] != "Free":
                            print("Equipment is not available for reservation (must be Free)")
                            cursor.close()
                            continue
                        cursor.execute("INSERT INTO reservations (equipment_id, lab, category, user_name, reservation_date) VALUES (%s, %s, %s, %s, %s)",
                                      (equipment_id, lab, category, user_name, reservation_date))
                        cursor.execute(f"UPDATE {table} SET status = 'In Use' WHERE id = %s", (equipment_id,))
                        connection.commit()
                        print("Equipment reserved successfully")
                        cursor.close()
                    
                    elif sub_choice == '6':
                        cursor = connection.cursor()
                        cursor.execute("SHOW TABLES LIKE 'reservations'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute("SELECT reservation_id, equipment_id, user_name, reservation_date FROM reservations WHERE lab = %s AND category = %s", (lab, category))
                        results = cursor.fetchall()
                        if results:
                            print(f"\n{lab} - {category} Reservations:")
                            print("Reservation ID | Equipment ID | User | Date")
                            print("-" * 50)
                            for row in results:
                                print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")
                        else:
                            print(f"No reservations found in {lab} - {category}")
                        cursor.close()
                    
                    elif sub_choice == '7':
                        break
                    else:
                        print("Invalid choice! Please try again.")
            
            elif phys_choice == '5':
                table = "phys_acoustic_instruments"
                lab = "Physics"
                category = "Acoustic Instruments"
                while True:
                    print(f"\n{lab} Lab - {category}")
                    print("1. Add Equipment")
                    print("2. View Equipment")
                    print("3. Update Equipment")
                    print("4. Delete Equipment")
                    print("5. Reserve Equipment")
                    print("6. View Reservations")
                    print("7. Back")
                    sub_choice = input("Enter choice: ")
                    
                    if sub_choice == '1':
                        cursor = connection.cursor()
                        cursor.execute(f"SELECT COUNT(*) FROM {table}")
                        count = cursor.fetchone()[0]
                        if count >= 900:
                            print("Cannot add more equipment: ID limit reached")
                            cursor.close()
                            continue
                        name = input("Enter equipment name: ")
                        status = input("Enter status (In Use, Free, Damaged): ")
                        if status not in ["In Use", "Free", "Damaged"]:
                            print("Invalid status! Must be 'In Use', 'Free', 'Damaged'")
                            cursor.close()
                            continue
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute(f"INSERT INTO {table} (name, status) VALUES (%s, %s)", (name, status))
                        connection.commit()
                        print("Equipment added successfully")
                        cursor.close()
                    
                    elif sub_choice == '2':
                        cursor = connection.cursor()
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute(f"SELECT * FROM {table}")
                        results = cursor.fetchall()
                        if results:
                            print(f"\n{lab} - {category} Equipment List:")
                            print("ID | Name | Status")
                            print("-" * 40)
                            for row in results:
                                print(f"{row[0]} | {row[1]} | {row[2]}")
                        else:
                            print(f"No equipment found in {lab} - {category}")
                        cursor.close()
                    
                    elif sub_choice == '3':
                        equipment_id = input("Enter equipment ID to update: ")
                        name = input("Enter new name (or press Enter to keep unchanged): ")
                        status = input("Enter new status (In Use, Free, Damaged, or press Enter to keep unchanged): ")
                        if status and status not in ["In Use", "Free", "Damaged"]:
                            print("Invalid status! Must be 'In Use', 'Free', 'Damaged'")
                            continue
                        cursor = connection.cursor()
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        query = f"UPDATE {table} SET "
                        updates = []
                        values = []
                        if name:
                            updates.append("name = %s")
                            values.append(name)
                        if status:
                            updates.append("status = %s")
                            values.append(status)
                        if updates:
                            query += ", ".join(updates) + " WHERE id = %s"
                            values.append(equipment_id)
                            cursor.execute(query, values)
                            connection.commit()
                            if cursor.rowcount > 0:
                                print("Equipment updated successfully")
                            else:
                                print("No equipment found with that ID")
                        else:
                            print("No updates provided")
                        cursor.close()
                    
                    elif sub_choice == '4':
                        equipment_id = input("Enter equipment ID to delete: ")
                        cursor = connection.cursor()
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute(f"DELETE FROM {table} WHERE id = %s", (equipment_id,))
                        connection.commit()
                        if cursor.rowcount > 0:
                            print("Equipment deleted successfully")
                        else:
                            print("No equipment found with that ID")
                        cursor.close()
                    
                    elif sub_choice == '5':
                        equipment_id = input("Enter equipment ID to reserve: ")
                        user_name = input("Enter your name: ")
                        reservation_date = input("Enter reservation date (YYYY-MM-DD): ")
                        if not reservation_date or len(reservation_date) != 10 or reservation_date[4] != '-' or reservation_date[7] != '-':
                            print("Invalid date format! Use YYYY-MM-DD")
                            continue
                        cursor = connection.cursor()
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute(f"SELECT status FROM {table} WHERE id = %s", (equipment_id,))
                        result = cursor.fetchone()
                        if not result:
                            print("No equipment found with that ID")
                            cursor.close()
                            continue
                        if result[0] != "Free":
                            print("Equipment is not available for reservation (must be Free)")
                            cursor.close()
                            continue
                        cursor.execute("INSERT INTO reservations (equipment_id, lab, category, user_name, reservation_date) VALUES (%s, %s, %s, %s, %s)",
                                      (equipment_id, lab, category, user_name, reservation_date))
                        cursor.execute(f"UPDATE {table} SET status = 'In Use' WHERE id = %s", (equipment_id,))
                        connection.commit()
                        print("Equipment reserved successfully")
                        cursor.close()
                    
                    elif sub_choice == '6':
                        cursor = connection.cursor()
                        cursor.execute("SHOW TABLES LIKE 'reservations'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute("SELECT reservation_id, equipment_id, user_name, reservation_date FROM reservations WHERE lab = %s AND category = %s", (lab, category))
                        results = cursor.fetchall()
                        if results:
                            print(f"\n{lab} - {category} Reservations:")
                            print("Reservation ID | Equipment ID | User | Date")
                            print("-" * 50)
                            for row in results:
                                print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")
                        else:
                            print(f"No reservations found in {lab} - {category}")
                        cursor.close()
                    
                    elif sub_choice == '7':
                        break
                    else:
                        print("Invalid choice! Please try again.")
            
            elif phys_choice == '6':
                break
            else:
                print("Invalid choice! Please try again.")
    
    elif choice == '3':
        while True:
            print("\nBiology Lab")
            print("1. Microscopes")
            print("2. Specimens and Slides")
            print("3. Dissection Tools")
            print("4. Back")
            bio_choice = input("Enter choice: ")
            
            if bio_choice == '1':
                table = "bio_microscopes"
                lab = "Biology"
                category = "Microscopes"
                while True:
                    print(f"\n{lab} Lab - {category}")
                    print("1. Add Equipment")
                    print("2. View Equipment")
                    print("3. Update Equipment")
                    print("4. Delete Equipment")
                    print("5. Reserve Equipment")
                    print("6. View Reservations")
                    print("7. Back")
                    sub_choice = input("Enter choice: ")
                    
                    if sub_choice == '1':
                        cursor = connection.cursor()
                        cursor.execute(f"SELECT COUNT(*) FROM {table}")
                        count = cursor.fetchone()[0]
                        if count >= 900:
                            print("Cannot add more equipment: ID limit reached")
                            cursor.close()
                            continue
                        name = input("Enter equipment name: ")
                        status = input("Enter status (In Use, Free, Damaged): ")
                        if status not in ["In Use", "Free", "Damaged"]:
                            print("Invalid status! Must be 'In Use', 'Free', 'Damaged'")
                            cursor.close()
                            continue
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute(f"INSERT INTO {table} (name, status) VALUES (%s, %s)", (name, status))
                        connection.commit()
                        print("Equipment added successfully")
                        cursor.close()
                    
                    elif sub_choice == '2':
                        cursor = connection.cursor()
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute(f"SELECT * FROM {table}")
                        results = cursor.fetchall()
                        if results:
                            print(f"\n{lab} - {category} Equipment List:")
                            print("ID | Name | Status")
                            print("-" * 40)
                            for row in results:
                                print(f"{row[0]} | {row[1]} | {row[2]}")
                        else:
                            print(f"No equipment found in {lab} - {category}")
                        cursor.close()
                    
                    elif sub_choice == '3':
                        equipment_id = input("Enter equipment ID to update: ")
                        name = input("Enter new name (or press Enter to keep unchanged): ")
                        status = input("Enter new status (In Use, Free, Damaged, or press Enter to keep unchanged): ")
                        if status and status not in ["In Use", "Free", "Damaged"]:
                            print("Invalid status! Must be 'In Use', 'Free', 'Damaged'")
                            continue
                        cursor = connection.cursor()
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        query = f"UPDATE {table} SET "
                        updates = []
                        values = []
                        if name:
                            updates.append("name = %s")
                            values.append(name)
                        if status:
                            updates.append("status = %s")
                            values.append(status)
                        if updates:
                            query += ", ".join(updates) + " WHERE id = %s"
                            values.append(equipment_id)
                            cursor.execute(query, values)
                            connection.commit()
                            if cursor.rowcount > 0:
                                print("Equipment updated successfully")
                            else:
                                print("No equipment found with that ID")
                        else:
                            print("No updates provided")
                        cursor.close()
                    
                    elif sub_choice == '4':
                        equipment_id = input("Enter equipment ID to delete: ")
                        cursor = connection.cursor()
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute(f"DELETE FROM {table} WHERE id = %s", (equipment_id,))
                        connection.commit()
                        if cursor.rowcount > 0:
                            print("Equipment deleted successfully")
                        else:
                            print("No equipment found with that ID")
                        cursor.close()
                    
                    elif sub_choice == '5':
                        equipment_id = input("Enter equipment ID to reserve: ")
                        user_name = input("Enter your name: ")
                        reservation_date = input("Enter reservation date (YYYY-MM-DD): ")
                        if not reservation_date or len(reservation_date) != 10 or reservation_date[4] != '-' or reservation_date[7] != '-':
                            print("Invalid date format! Use YYYY-MM-DD")
                            continue
                        cursor = connection.cursor()
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute(f"SELECT status FROM {table} WHERE id = %s", (equipment_id,))
                        result = cursor.fetchone()
                        if not result:
                            print("No equipment found with that ID")
                            cursor.close()
                            continue
                        if result[0] != "Free":
                            print("Equipment is not available for reservation (must be Free)")
                            cursor.close()
                            continue
                        cursor.execute("INSERT INTO reservations (equipment_id, lab, category, user_name, reservation_date) VALUES (%s, %s, %s, %s, %s)",
                                      (equipment_id, lab, category, user_name, reservation_date))
                        cursor.execute(f"UPDATE {table} SET status = 'In Use' WHERE id = %s", (equipment_id,))
                        connection.commit()
                        print("Equipment reserved successfully")
                        cursor.close()
                    
                    elif sub_choice == '6':
                        cursor = connection.cursor()
                        cursor.execute("SHOW TABLES LIKE 'reservations'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute("SELECT reservation_id, equipment_id, user_name, reservation_date FROM reservations WHERE lab = %s AND category = %s", (lab, category))
                        results = cursor.fetchall()
                        if results:
                            print(f"\n{lab} - {category} Reservations:")
                            print("Reservation ID | Equipment ID | User | Date")
                            print("-" * 50)
                            for row in results:
                                print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")
                        else:
                            print(f"No reservations found in {lab} - {category}")
                        cursor.close()
                    
                    elif sub_choice == '7':
                        break
                    else:
                        print("Invalid choice! Please try again.")
            
            elif bio_choice == '2':
                table = "bio_specimens_slides"
                lab = "Biology"
                category = "Specimens and Slides"
                while True:
                    print(f"\n{lab} Lab - {category}")
                    print("1. Add Equipment")
                    print("2. View Equipment")
                    print("3. Update Equipment")
                    print("4. Delete Equipment")
                    print("5. Reserve Equipment")
                    print("6. View Reservations")
                    print("7. Back")
                    sub_choice = input("Enter choice: ")
                    
                    if sub_choice == '1':
                        cursor = connection.cursor()
                        cursor.execute(f"SELECT COUNT(*) FROM {table}")
                        count = cursor.fetchone()[0]
                        if count >= 900:
                            print("Cannot add more equipment: ID limit reached")
                            cursor.close()
                            continue
                        name = input("Enter equipment name: ")
                        status = input("Enter status (In Use, Free, Damaged): ")
                        if status not in ["In Use", "Free", "Damaged"]:
                            print("Invalid status! Must be 'In Use', 'Free', 'Damaged'")
                            cursor.close()
                            continue
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute(f"INSERT INTO {table} (name, status) VALUES (%s, %s)", (name, status))
                        connection.commit()
                        print("Equipment added successfully")
                        cursor.close()
                    
                    elif sub_choice == '2':
                        cursor = connection.cursor()
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute(f"SELECT * FROM {table}")
                        results = cursor.fetchall()
                        if results:
                            print(f"\n{lab} - {category} Equipment List:")
                            print("ID | Name | Status")
                            print("-" * 40)
                            for row in results:
                                print(f"{row[0]} | {row[1]} | {row[2]}")
                        else:
                            print(f"No equipment found in {lab} - {category}")
                        cursor.close()
                    
                    elif sub_choice == '3':
                        equipment_id = input("Enter equipment ID to update: ")
                        name = input("Enter new name (or press Enter to keep unchanged): ")
                        status = input("Enter new status (In Use, Free, Damaged, or press Enter to keep unchanged): ")
                        if status and status not in ["In Use", "Free", "Damaged"]:
                            print("Invalid status! Must be 'In Use', 'Free', 'Damaged'")
                            continue
                        cursor = connection.cursor()
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        query = f"UPDATE {table} SET "
                        updates = []
                        values = []
                        if name:
                            updates.append("name = %s")
                            values.append(name)
                        if status:
                            updates.append("status = %s")
                            values.append(status)
                        if updates:
                            query += ", ".join(updates) + " WHERE id = %s"
                            values.append(equipment_id)
                            cursor.execute(query, values)
                            connection.commit()
                            if cursor.rowcount > 0:
                                print("Equipment updated successfully")
                            else:
                                print("No equipment found with that ID")
                        else:
                            print("No updates provided")
                        cursor.close()
                    
                    elif sub_choice == '4':
                        equipment_id = input("Enter equipment ID to delete: ")
                        cursor = connection.cursor()
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute(f"DELETE FROM {table} WHERE id = %s", (equipment_id,))
                        connection.commit()
                        if cursor.rowcount > 0:
                            print("Equipment deleted successfully")
                        else:
                            print("No equipment found with that ID")
                        cursor.close()
                    
                    elif sub_choice == '5':
                        equipment_id = input("Enter equipment ID to reserve: ")
                        user_name = input("Enter your name: ")
                        reservation_date = input("Enter reservation date (YYYY-MM-DD): ")
                        if not reservation_date or len(reservation_date) != 10 or reservation_date[4] != '-' or reservation_date[7] != '-':
                            print("Invalid date format! Use YYYY-MM-DD")
                            continue
                        cursor = connection.cursor()
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute(f"SELECT status FROM {table} WHERE id = %s", (equipment_id,))
                        result = cursor.fetchone()
                        if not result:
                            print("No equipment found with that ID")
                            cursor.close()
                            continue
                        if result[0] != "Free":
                            print("Equipment is not available for reservation (must be Free)")
                            cursor.close()
                            continue
                        cursor.execute("INSERT INTO reservations (equipment_id, lab, category, user_name, reservation_date) VALUES (%s, %s, %s, %s, %s)",
                                      (equipment_id, lab, category, user_name, reservation_date))
                        cursor.execute(f"UPDATE {table} SET status = 'In Use' WHERE id = %s", (equipment_id,))
                        connection.commit()
                        print("Equipment reserved successfully")
                        cursor.close()
                    
                    elif sub_choice == '6':
                        cursor = connection.cursor()
                        cursor.execute("SHOW TABLES LIKE 'reservations'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute("SELECT reservation_id, equipment_id, user_name, reservation_date FROM reservations WHERE lab = %s AND category = %s", (lab, category))
                        results = cursor.fetchall()
                        if results:
                            print(f"\n{lab} - {category} Reservations:")
                            print("Reservation ID | Equipment ID | User | Date")
                            print("-" * 50)
                            for row in results:
                                print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")
                        else:
                            print(f"No reservations found in {lab} - {category}")
                        cursor.close()
                    
                    elif sub_choice == '7':
                        break
                    else:
                        print("Invalid choice! Please try again.")
            
            elif bio_choice == '3':
                table = "bio_dissection_tools"
                lab = "Biology"
                category = "Dissection Tools"
                while True:
                    print(f"\n{lab} Lab - {category}")
                    print("1. Add Equipment")
                    print("2. View Equipment")
                    print("3. Update Equipment")
                    print("4. Delete Equipment")
                    print("5. Reserve Equipment")
                    print("6. View Reservations")
                    print("7. Back")
                    sub_choice = input("Enter choice: ")
                    
                    if sub_choice == '1':
                        cursor = connection.cursor()
                        cursor.execute(f"SELECT COUNT(*) FROM {table}")
                        count = cursor.fetchone()[0]
                        if count >= 900:
                            print("Cannot add more equipment: ID limit reached")
                            cursor.close()
                            continue
                        name = input("Enter equipment name: ")
                        status = input("Enter status (In Use, Free, Damaged): ")
                        if status not in ["In Use", "Free", "Damaged"]:
                            print("Invalid status! Must be 'In Use', 'Free', 'Damaged'")
                            cursor.close()
                            continue
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute(f"INSERT INTO {table} (name, status) VALUES (%s, %s)", (name, status))
                        connection.commit()
                        print("Equipment added successfully")
                        cursor.close()
                    
                    elif sub_choice == '2':
                        cursor = connection.cursor()
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute(f"SELECT * FROM {table}")
                        results = cursor.fetchall()
                        if results:
                            print(f"\n{lab} - {category} Equipment List:")
                            print("ID | Name | Status")
                            print("-" * 40)
                            for row in results:
                                print(f"{row[0]} | {row[1]} | {row[2]}")
                        else:
                            print(f"No equipment found in {lab} - {category}")
                        cursor.close()
                    
                    elif sub_choice == '3':
                        equipment_id = input("Enter equipment ID to update: ")
                        name = input("Enter new name (or press Enter to keep unchanged): ")
                        status = input("Enter new status (In Use, Free, Damaged, or press Enter to keep unchanged): ")
                        if status and status not in ["In Use", "Free", "Damaged"]:
                            print("Invalid status! Must be 'In Use', 'Free', 'Damaged'")
                            continue
                        cursor = connection.cursor()
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        query = f"UPDATE {table} SET "
                        updates = []
                        values = []
                        if name:
                            updates.append("name = %s")
                            values.append(name)
                        if status:
                            updates.append("status = %s")
                            values.append(status)
                        if updates:
                            query += ", ".join(updates) + " WHERE id = %s"
                            values.append(equipment_id)
                            cursor.execute(query, values)
                            connection.commit()
                            if cursor.rowcount > 0:
                                print("Equipment updated successfully")
                            else:
                                print("No equipment found with that ID")
                        else:
                            print("No updates provided")
                        cursor.close()
                    
                    elif sub_choice == '4':
                        equipment_id = input("Enter equipment ID to delete: ")
                        cursor = connection.cursor()
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute(f"DELETE FROM {table} WHERE id = %s", (equipment_id,))
                        connection.commit()
                        if cursor.rowcount > 0:
                            print("Equipment deleted successfully")
                        else:
                            print("No equipment found with that ID")
                        cursor.close()
                    
                    elif sub_choice == '5':
                        equipment_id = input("Enter equipment ID to reserve: ")
                        user_name = input("Enter your name: ")
                        reservation_date = input("Enter reservation date (YYYY-MM-DD): ")
                        if not reservation_date or len(reservation_date) != 10 or reservation_date[4] != '-' or reservation_date[7] != '-':
                            print("Invalid date format! Use YYYY-MM-DD")
                            continue
                        cursor = connection.cursor()
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute(f"SELECT status FROM {table} WHERE id = %s", (equipment_id,))
                        result = cursor.fetchone()
                        if not result:
                            print("No equipment found with that ID")
                            cursor.close()
                            continue
                        if result[0] != "Free":
                            print("Equipment is not available for reservation (must be Free)")
                            cursor.close()
                            continue
                        cursor.execute("INSERT INTO reservations (equipment_id, lab, category, user_name, reservation_date) VALUES (%s, %s, %s, %s, %s)",
                                      (equipment_id, lab, category, user_name, reservation_date))
                        cursor.execute(f"UPDATE {table} SET status = 'In Use' WHERE id = %s", (equipment_id,))
                        connection.commit()
                        print("Equipment reserved successfully")
                        cursor.close()
                    
                    elif sub_choice == '6':
                        cursor = connection.cursor()
                        cursor.execute("SHOW TABLES LIKE 'reservations'")
                        if not cursor.fetchone():
                            print("Table not found")
                            cursor.close()
                            continue
                        cursor.execute("SELECT reservation_id, equipment_id, user_name, reservation_date FROM reservations WHERE lab = %s AND category = %s", (lab, category))
                        results = cursor.fetchall()
                        if results:
                            print(f"\n{lab} - {category} Reservations:")
                            print("Reservation ID | Equipment ID | User | Date")
                            print("-" * 50)
                            for row in results:
                                print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")
                        else:
                            print(f"No reservations found in {lab} - {category}")
                        cursor.close()
                    
                    elif sub_choice == '7':
                        break
                    else:
                        print("Invalid choice! Please try again.")
            
            elif bio_choice == '4':
                break
            else:
                print("Invalid choice! Please try again.")
    
    elif choice == '4':
        print("Exiting program")
        connection.close()
        break
    else:
        print("Invalid choice! Please try again.")
