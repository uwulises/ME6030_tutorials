import requests
import json

# URL of the Flask server
url = 'http://192.168.1.100:5000/move'

# Data to be sent in the POST request
data = {
    'x': 100,  # Example x coordinate
    'y': 500   # Example y coordinate
}

# Convert data to JSON format
json_data = json.dumps(data)

# Send POST request to the server
response = requests.post(url, json=json_data)

# Check the response from the server
if response.status_code == 200:
    print("Success:", response.json())
else:
    print("Error:", response.json())
