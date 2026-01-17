import argparse
import sys
import os
import csv
import json
import requests
import time

# The file to store the flight prices
PRICE_HISTORY_FILE = "price_history.csv"
API_KEY = os.environ.get("HASDATA_API_KEY")
API_HOST = "https://api.hasdata.com/scrape/google/flights/search"

def get_flight_price(origin, destination, start_date, end_date):
    """
    Gets the flight price from the HasData Google Flights API.
    """
    if not API_KEY:
        print("Error: HASDATA_API_KEY environment variable not set.")
        print("Please get a free API key from https://hasdata.com/ and set the environment variable.")
        return None

    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "departureId": origin,
        "arrivalId": destination,
        "outboundDate": start_date,
        "inboundDate": end_date,
        "currency": "USD",
        "country": "US",
        "language": "en-US"
    }

    try:
        response = requests.post(API_HOST, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        data = response.json()

        if data.get("data") and data["data"]["flights"]:
            price = data["data"]["flights"][0].get("price")
            return price
        else:
            print("Could not find flight information in the API response.")
            return None

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 401:
            print("Authentication failed. Please check your API key.")
        else:
            print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    except (KeyError, IndexError):
        print("Could not parse the price from the API response.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return None

def get_last_price(origin, destination, start_date, end_date):
    """
    Gets the last recorded price for a flight from the price history file.
    """
    if not os.path.exists(PRICE_HISTORY_FILE):
        return None

    with open(PRICE_HISTORY_FILE, 'r') as f:
        reader = csv.reader(f)
        for row in reversed(list(reader)):
            if row and row[0] == origin and row[1] == destination and row[2] == start_date and row[3] == end_date:
                return float(row[4])
    return None

def save_price(origin, destination, start_date, end_date, price):
    """
    Saves the current price of a flight to the price history file.
    """
    with open(PRICE_HISTORY_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([origin, destination, start_date, end_date, price, time.strftime("%Y-%m-%d %H:%M:%S")])

def main():
    """
    Main function to parse arguments, initiate the scraping process, and track prices.
    """
    parser = argparse.ArgumentParser(description="Fare Tracker - A tool to track flight prices using the HasData Google Flights API.")
    parser.add_argument("origin", help="The origin airport code (e.g., 'SFO').")
    parser.add_argument("destination", help="The destination airport code (e.g., 'LAX').")
    parser.add_argument("start_date", help="The departure date in YYYY-MM-DD format.")
    parser.add_argument("end_date", help="The return date in YYYY-MM-DD format.")

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    print("Starting the fare tracker...")
    price = get_flight_price(args.origin, args.destination, args.start_date, args.end_date)

    if price is not None:
        last_price = get_last_price(args.origin, args.destination, args.start_date, args.end_date)
        save_price(args.origin, args.destination, args.start_date, args.end_date, price)

        if last_price is not None and price < last_price:
            print("\n" + "="*30)
            print("  PRICE DROP ALERT!")
            print(f"  The price for a flight from {args.origin} to {args.destination}")
            print(f"  has dropped from ${last_price} to ${price}.")
            print("="*30 + "\n")
        elif last_price is not None:
            print(f"\nThe price has not dropped. The current price is ${price}, and the last recorded price was ${last_price}.")
        else:
            print(f"\nThis is the first time you've tracked this flight. The current price is ${price}.")
    else:
        print("Failed to retrieve the flight price.")

if __name__ == "__main__":
    main()
