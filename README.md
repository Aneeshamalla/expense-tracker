# Real-Time Currency & Expense Tracker

A command-line app for tracking personal expenses in different currencies. You can record expenses in NPR, USD or INR. The app uses a live exchange rate API to convert every expense into Nepali Rupees (NPR), so you can see your total spending in one currency. It also shows how much you spent in each category.

If the API is slow, down or rate-limited, the app retries and shows a clear message instead of crashing.

## Key Features

- **Manage expenses:** add, view, update and delete expenses, each with an amount, currency and category
- **Live currency conversion:** converts all expenses into NPR using [ExchangeRate-API](https://www.exchangerate-api.com)
- **Category report:** shows total spending per category, its share of all spending as a percentage, and how many expenses it has, sorted from highest to lowest
- **Per-currency summary:** shows how much was spent in each original currency
- **Email report:** sends the category report to an email address through Gmail
- **Saved data:** expenses are stored in a JSON file and loaded again when the app starts
- **Error handling:**
  - Timeouts, lost connections and server errors (5xx): retries up to 3 times
  - Rate limits (HTTP 429): stops and asks the user to try later
  - Invalid API responses and wrong user input: shows a clear message instead of crashing

## Concepts Used

| Concept                     | Where it is used                                                                                                      |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| Data types and dictionaries | Each expense is a dictionary. The report builds nested dictionaries such as `{"food": {"total": 1650.0, "count": 2}}` |
| HTTP requests               | `requests.get()` calls the exchange rate API with a 5-second timeout                                                  |
| Exception handling          | `try`/`except` for network errors, bad JSON, missing data, invalid user input, file errors and email errors           |
| JSON                        | Parses the API response and saves and loads expenses from `data/expenses.json`                                        |
| File I/O                    | Reads and writes the expenses file with `pathlib` and `open()`                                                        |
| Environment variables       | The API key and email login are read from `.env` with `python-dotenv`                                                 |
| Modular structure           | Each file in `src/` has one job: menu, expenses, conversion, report, storage or email                                 |

## Project Structure

```
expense_tracker/
├── src/
│   ├── main.py         # menu and main loop
│   ├── expenses.py     # add, view, update, delete expenses and input checks
│   ├── converter.py    # API calls, retries and conversion to NPR
│   ├── report.py       # category and currency breakdown
│   ├── storage.py      # save and load expenses.json
│   └── emailer.py      # send the report by email
├── data/
│   └── expenses.json   # saved expenses
├── .env                # API key and email settings (not committed)
├── .gitignore
└── README.md
```

## Setup and Running

**Requirements:** Python 3.10 or newer, and a free API key from [exchangerate-api.com](https://www.exchangerate-api.com).

1. Clone the repository and go into the folder:

   ```bash
   git clone https://github.com/Aneeshamalla/expense-tracker.git
   cd expense-tracker

   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # macOS / Linux
   ```

3. Install the packages:

   ```bash
   pip install requests python-dotenv
   ```

4. Create a file named `.env` in the `expense_tracker` folder:

   ```
   EXCHANGE_API_KEY=your_api_key_here

   EMAIL_ADDRESS=your_gmail@gmail.com
   EMAIL_APP_PASSWORD=your_gmail_app_password
   EMAIL_TO=receiver@example.com
   ```

   The email settings are only needed for the "Email report" option. For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833), not your normal password.

5. Run the app:

   ```bash
   python src/main.py
   ```

## Sample Output

**Menu and adding an expense**

```
===== Expense Tracker =====
1. Add expense
2. View expenses
3. Update expense
4. Delete expense
5. View in NPR
6. Category report
7. Email report
8. Exit
Choose an option: 1
Enter amount: 500
Enter currency (NPR/USD/INR): usd
Enter category: shopping
Added: 500.0 USD - shopping
```

**View in NPR**

```
Choose an option: 5
1. 100.0 USD = 15250.88 NPR - travel
2. 300.0 NPR = 300.0 NPR - food
3. 1200.0 NPR = 1200.0 NPR - food
4. 800.0 INR = 1280.0 NPR - shopping
5. 450.0 NPR = 450.0 NPR - food
6. 500.0 USD = 76254.38 NPR - shopping
Total: 94735.26 NPR
```

**Category report**

```
Choose an option: 6

--- Spending by Category ---
shopping: 77534.38 NPR (81.8%, 2 expenses)
travel: 15250.88 NPR (16.1%, 1 expenses)
food: 1950.0 NPR (2.1%, 3 expenses)
Grand Total: 94735.26 NPR

--- Spent in Each Currency ---
USD: 600.0
NPR: 1950.0
INR: 800.0
```

**Email report**

```
===== Expense Tracker =====
1. Add expense
2. View expenses
3. Update expense
4. Delete expense
5. View in NPR
6. Category report
7. Email report
8. Exit
Choose an option: 7
Report sent to receiver@example.com!
```
<img width="362" height="275" alt="image" src="https://github.com/user-attachments/assets/36d82486-6dcd-40df-b966-e7bcaad8adeb" />



The email that arrives has the subject **Your Expense Report** and contains the same category report:

```
--- Spending by Category ---
shopping: 77534.38 NPR (81.8%, 2 expenses)
travel: 15250.88 NPR (16.1%, 1 expenses)
food: 1950.0 NPR (2.1%, 3 expenses)
Grand Total: 94735.26 NPR

--- Spent in Each Currency ---
USD: 600.0
NPR: 1950.0
INR: 800.0
```

**Error handling**

```
Choose an option: 1
Enter amount: abc
Invalid input: Amount must be a number

Choose an option: 1
Enter amount: 100
Enter currency (NPR/USD/INR): EUR
Invalid input: Currency must be one of ['NPR', 'USD', 'INR']

Choose an option: 4
1. 100.0 USD - travel
2. 300.0 NPR - food
3. 1200.0 NPR - food
4. 800.0 INR - shopping
5. 450.0 NPR - food
6. 500.0 USD - shopping
Enter expense number to delete: 8
Invalid input: Number must be between 1 and 6

Choose an option: 9
Invalid choice. Please try again.
```

Exchange rates change every day, so your numbers will be different.

## Security

API keys and email passwords are kept in `.env`, which is listed in `.gitignore` and is never committed to Git.
