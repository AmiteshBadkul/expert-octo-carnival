# Google Flights Fare Tracker

This repository contains a Python script for tracking flight fares from Google Flights using the HasData API. It is a command-line tool that allows you to monitor the price of a specific flight and receive alerts when the price drops.

## How It Works

The script uses the [HasData Google Flights API](https://hasdata.com/apis/google-flights-api) to fetch real-time flight fare data. The price is then saved to a local CSV file, `price_history.csv`, to keep a record of the price over time. On subsequent runs, the script will compare the current price to the last recorded price and alert the user if the price has dropped.

## Setup and Installation

### 1. Install Dependencies

Before running the script, you need to install the required Python packages. You can do this using `pip`:

```bash
pip install -r requirements.txt
```

### 2. Get an API Key

This script requires an API key from HasData. You can get a free API key by signing up on the [HasData website](https://hasdata.com/signup).

### 3. Set the Environment Variable

For security reasons, it is recommended to set your API key as an environment variable.

*   **On macOS and Linux:**
    ```bash
    export HASDATA_API_KEY="your_api_key_here"
    ```
*   **On Windows:**
    ```bash
    set HASDATA_API_KEY="your_api_key_here"
    ```
Replace `"your_api_key_here"` with the API key you received from HasData.

## Usage

You can run the script from the command line. You must provide the origin, destination, start date, and end date as arguments.

### Arguments

*   `origin`: The origin airport code (e.g., `SFO`).
*   `destination`: The destination airport code (e.g., `LAX`).
*   `start_date`: The departure date in `YYYY-MM-DD` format.
*   `end_date`: The return date in `YYYY-MM-DD` format.

### Example

To track the price of a round-trip flight from San Francisco (SFO) to Los Angeles (LAX) from December 25, 2024, to January 1, 2025, you would run the following command:

```bash
python fare_tracker.py SFO LAX 2024-12-25 2025-01-01
```

### Output

The script will print the current price of the flight and, if it has been run before, will alert you if the price has dropped.

```
Starting the fare tracker...
The current price for a flight from SFO to LAX is $128.

==============================
  PRICE DROP ALERT!
  The price for a flight from SFO to LAX
  has dropped from $150 to $128.
==============================
```
