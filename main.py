
import os
while True:
    print("\n=== Main Menu ===")
    print("1. Chemistry")
    print("2. Physics")
    print("3. Biology")
    print("4. Exit")
    choice = input("Enter your choice (1-4): ")
    
    if choice == '1':
        os.system('cls')  
        while True:
            print("\n====== Chemistry Lab ======")
            print("1. Chemicals")
            print("2. Apparatus")
            print("3. Back to Main Menu")
            item_choice = input("Enter your choice (1-3): ")
            if item_choice == '1':
                print("\nYou selected Chemicals")
            elif item_choice == '2':
                print("\nYou selected Apparatus")
            elif item_choice == '3':
                os.system('cls')
                break
            else:
                print("\nInvalid choice! Please select 1, 2, or 3.")

    elif choice == '2':
        os.system('cls')
        while True:
            print("\n=== Physics Lab ===")
            print("1. Measuring Instruments")
            print("2. Optical Instruments")
            print("3. Electrical Instruments")
            print("4. Thermal Instruments")
            print("5. Acoustic Instruments")
            print("6. Back to Main Menu")
            settings_choice = input("Enter your choice (1-6): ")
            if settings_choice == '1':
                print("\nYou selected Measuring Instruments")
            elif settings_choice == '2':
                print("\nYou selected Optical Instruments")
            elif settings_choice == '3':
                print("\nYou selected Electrical Instruments")
            elif settings_choice == '4':
                print("\nYou selected Thermal Instruments")
            elif settings_choice == '5':
                print("\nYou selected Acoustic Instruments")
            elif settings_choice == '6':
                os.system('cls') 
                break
            else:
                print("\nInvalid choice! Please select 1, 2, 3, 4, 5, or 6.")
    elif choice == '3':
        os.system('cls')
        while True:
            print("\n=== Biology Lab ===")
            print("1. Microscopes")
            print("2. Specimens")
            print("3. Back to Main Menu")
            bio_choice = input("Enter your choice (1-3): ")
            if bio_choice == '1':
                print("\nYou selected Microscopes")
            elif bio_choice == '2':
                print("\nYou selected Specimens")
            elif bio_choice == '3':
                os.system('cls')
                break
            else:
                print("\nInvalid choice! Please select 1, 2, or 3.")
    elif choice == '4':
        print("\nGoodbye!")
        break
    else:
        print("\nInvalid choice! Please select 1, 2, 3, or 4.")
