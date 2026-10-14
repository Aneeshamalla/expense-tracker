# List to store all expenses
expenses = []

# Currencies the app accepts
CURRENCIES = ["NPR", "USD", "INR"]


def show_expense(expense):
    return f"{expense['amount']} {expense['currency']} - {expense['category']}"


def ask_amount(message):
    try:
        amount = float(input(message))
    except ValueError:
        raise ValueError("Amount must be a number")

    if amount <= 0:
        raise ValueError("Amount must be greater than 0")
    return amount


def ask_currency(message):
    currency = input(message).strip().upper()
    if currency not in CURRENCIES:
        raise ValueError(f"Currency must be one of {CURRENCIES}")
    return currency


def ask_category(message):
    category = input(message).strip().lower()
    if category == "":
        raise ValueError("Category cannot be empty")
    return category


def ask_expense_number(message):
    try:
        number = int(input(message))
    except ValueError:
        raise ValueError("Please enter a whole number")

    if number < 1 or number > len(expenses):
        raise ValueError(f"Number must be between 1 and {len(expenses)}")
    return number


def add_expense():
    amount = ask_amount("Enter amount: ")
    currency = ask_currency("Enter currency (NPR/USD/INR): ")
    category = ask_category("Enter category: ")

    expense = {"amount": amount, "currency": currency, "category": category}
    expenses.append(expense)
    print(f"Added: {show_expense(expense)}")


def view_expenses():
    if len(expenses) == 0:
        print("No expenses yet.")
        return

    count = 1
    for e in expenses:
        print(f"{count}. {show_expense(e)}")
        count = count + 1


def update_expense():
    view_expenses()
    if len(expenses) == 0:
        return

    number = ask_expense_number("Enter expense number to update: ")
    index = number - 1

    amount = ask_amount("Enter new amount: ")
    currency = ask_currency("Enter new currency (NPR/USD/INR): ")
    category = ask_category("Enter new category: ")

    expenses[index] = {"amount": amount, "currency": currency, "category": category}
    print(f"Updated: {show_expense(expenses[index])}")


def delete_expense():
    view_expenses()
    if len(expenses) == 0:
        return

    number = ask_expense_number("Enter expense number to delete: ")
    index = number - 1

    removed = expenses.pop(index)
    print(f"Deleted: {show_expense(removed)}")
