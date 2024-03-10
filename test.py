import requests
import csv

# Define your Amadeus API credentials
API_KEY = "Your_api_key"
API_SECRET = "Your_secret_api_code"
# Define the base URL for the Amadeus API
BASE_URL = "https://test.api.amadeus.com/v1/analytics/itinerary-price-metrics"

# Generate a new access token (use your actual credentials)
token_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
token_data = {
    "grant_type": "client_credentials",
    "client_id": API_KEY,
    "client_secret": API_SECRET
}
response = requests.post(token_url, data=token_data)
acsse_token = response.json()['access_token']
headers = {
    "Authorization": f"Bearer {acsse_token}"
}
# Define the source airport code (DEL for Delhi)
source_airport = "DEL"

# Define the top 5 destination airports in India
destination_airports = ["BOM", "BLR", "MAA", "HYD", "CCU"]

# Open a CSV file to store the results
with open('flight_prices_2022.csv', mode='w', newline='') as csv_file:
    fieldnames = ['Date', 'Destination', 'Min Price']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    # Iterate over each day in 2022
    for month in range(1, 13):
        for day in range(1, 32):
            date = f"2022-{month:02d}-{day:02d}"

            # Iterate over each destination airport
            for destination in destination_airports:
                # Construct the URL for the API request
                
                url = f"{BASE_URL}?originIataCode={source_airport}&destinationIataCode={destination}&departureDate={date}"

                # Make the API request
                response = requests.get(url, headers=headers)

                # Check if the request was successful
                if response.status_code == 200:
                    # Parse the response JSON
                    data = response.json()
                    # Extract the minimum price
                    minimum_price = None
                    try:
                        for metric in data["data"][0]["priceMetrics"]:
                            if metric["quartileRanking"] == "MINIMUM":
                                minimum_price = float(metric["amount"])  # Convert amount to float
                                break
                    except:
                        print(f"No data for {date}, {destination}")
                        continue

                    # Write the data to the CSV file
                    writer.writerow({'Date': date, 'Destination': destination, 'Min Price': minimum_price})
                else:
                    print(response.status_code)
                    print(f"Failed to fetch data for {date}, {destination}")

print("Data retrieval and storage complete.")
