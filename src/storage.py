import json
from pathlib import Path

DATA_FOLDER = Path(__file__).parent.parent / "data"
FILE_PATH = DATA_FOLDER / "expenses.json"


def save_expenses(expenses):
    try:
        DATA_FOLDER.mkdir(exist_ok=True)
        with open(FILE_PATH, "w") as f:
            json.dump(expenses, f, indent=4)
    except OSError:
        print("Could not save expenses to file.")


def load_expenses():
    try:
        with open(FILE_PATH, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Data file is damaged. Starting with an empty list.")
        return []

    if type(data) != list:
        print("Data file has the wrong format. Starting with an empty list.")
        return []

    good_expenses = []
    for e in data:
        if type(e) == dict and "amount" in e and "currency" in e and "category" in e:
            good_expenses.append(e)
        else:
            print(f"Skipping a broken expense in the data file: {e}")

    return good_expenses
