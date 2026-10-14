from expenses import expenses, add_expense, view_expenses, update_expense, delete_expense
from converter import view_in_npr
from report import category_report
from storage import save_expenses, load_expenses
from emailer import send_report


def show_menu():
    print("\n===== Expense Tracker =====")
    print("1. Add expense")
    print("2. View expenses")
    print("3. Update expense")
    print("4. Delete expense")
    print("5. View in NPR")
    print("6. Category report")
    print("7. Email report")
    print("8. Exit")


# Load saved expenses when the app starts
expenses.extend(load_expenses())

while True:
    show_menu()
    choice = input("Choose an option: ")

    try:
        if choice == "1":
            add_expense()
            save_expenses(expenses)
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            update_expense()
            save_expenses(expenses)
        elif choice == "4":
            delete_expense()
            save_expenses(expenses)
        elif choice == "5":
            view_in_npr(expenses)
        elif choice == "6":
            category_report(expenses)
        elif choice == "7":
            send_report(expenses)
        elif choice == "8":
            print("Thank You!")
            break
        else:
            print("Invalid choice. Please try again.")
    except ValueError as error:
        print(f"Invalid input: {error}")
    except KeyboardInterrupt:
        print("\nThank You!")
        break