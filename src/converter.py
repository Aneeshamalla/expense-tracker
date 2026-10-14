import os
import time

import requests
from dotenv import load_dotenv

# Read the secret API key from the .env file
load_dotenv()
API_KEY = os.getenv("EXCHANGE_API_KEY")

API_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/NPR"

MAX_TRIES = 3


def get_rates():
    if not API_KEY:
        print("EXCHANGE_API_KEY is missing in the .env file.")
        return None

    for attempt in range(1, MAX_TRIES + 1):
        if attempt > 1:
            print("Trying again in 2 seconds...")
            time.sleep(2)

        try:
            response = requests.get(API_URL, timeout=5)

            if response.status_code == 429:
                print("API rate limit reached. Please try again later.")
                return None

            if response.status_code >= 500:
                print(f"API server is down (error {response.status_code}). Try {attempt} of {MAX_TRIES}.")
                continue

            data = response.json()

            if data["result"] != "success":
                print(f"API error: {data['error-type']}")
                return None

            return data["conversion_rates"]

        except requests.exceptions.Timeout:
            print(f"API took too long to answer. Try {attempt} of {MAX_TRIES}.")
        except requests.exceptions.ConnectionError:
            print(f"Could not connect. Check your internet. Try {attempt} of {MAX_TRIES}.")
        except requests.exceptions.RequestException:
            print("Something went wrong with the request.")
            return None
        except ValueError:
            print("API sent back data that is not JSON.")
            return None
        except KeyError:
            print("API response is missing some data.")
            return None

    print("Could not reach the API.")
    return None


def convert_to_npr(amount, currency, rates):
    if currency == "NPR":
        return amount

    if rates is None or currency not in rates:
        return None

    return round(amount / rates[currency], 2)


def view_in_npr(expenses):
    if len(expenses) == 0:
        print("No expenses yet.")
        return

    rates = get_rates()

    total = 0
    count = 1
    for e in expenses:
        npr = convert_to_npr(e["amount"], e["currency"], rates)
        if npr is None:
            print(f"{count}. {e['amount']} {e['currency']} - {e['category']} (could not convert)")
        else:
            print(f"{count}. {e['amount']} {e['currency']} = {npr} NPR - {e['category']}")
            total = total + npr
        count = count + 1

    print(f"Total: {round(total, 2)} NPR")
