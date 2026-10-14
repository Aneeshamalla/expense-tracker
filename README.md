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

| Concept | Where it is used |
|---|---|
| Data types and dictionaries | Each expense is a dictionary. The report builds nested dictionaries such as `{"food": {"total": 1650.0, "count": 2}}` |
| HTTP requests | `requests.get()` calls the exchange rate API with a 5-second timeout |
| Exception handling | `try`/`except` for network errors, bad JSON, missing data, invalid user input, file errors and email errors |
| JSON | Parses the API response and saves and loads expenses from `data/expenses.json` |
| File I/O | Reads and writes the expenses file with `pathlib` and `open()` |
| Environment variables | The API key and email login are read from `.env` with `python-dotenv` |
| Modular structure | Each file in `src/` has one job: menu, expenses, conversion, report, storage or email |

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
   git clone <your-repo-url>
   cd expense_tracker
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

<!-- Add screenshot here -->

**View in NPR**

<!-- Add screenshot here -->

**Category report**

<!-- Add screenshot here -->

**Error handling**

<!-- Add screenshot here -->

## Security

API keys and email passwords are kept in `.env`, which is listed in `.gitignore` and is never committed to Git.
