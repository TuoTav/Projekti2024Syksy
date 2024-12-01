import requests
import csv

def fetch_sensor_data_http(url, output_file):
    """
    Fetches data from the Flask API and saves it to a CSV file.

    Args:
        url (str): The URL to fetch data from.
        output_file (str): Output CSV file name.
    """
    try:
        # Send GET request to the Flask API
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful

        # Parse the JSON response
        data = response.json()

        if not data:
            print("No data found.")
            return

        # Write data to a CSV file
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()  # Write the headers
            writer.writerows(data)  # Write the rows

        print(f"Data saved to {output_file}")
    
    except requests.exceptions.RequestException as e:
        print(f"HTTP request error: {e}")
    except Exception as e:
        print(f"Error: {e}")

# Example Usage
if __name__ == "__main__":
    # Flask server URL
    SERVER_URL = "http://172.20.241.50:8080/get_sensor_data"  # Your server's IP and endpoint
    OUTPUT_FILE = "sensor_values.csv"

    # Fetch and save data to CSV
    fetch_sensor_data_http(SERVER_URL, OUTPUT_FILE)
