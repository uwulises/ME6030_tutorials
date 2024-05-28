import requests
import json

class MoveClient:
    def __init__(self, url):
        self.url = url

    def send_move(self, x, y, z=170):
        # Data to be sent in the POST request
        data = {
            'x': x,
            'y': y,
            'z': z,
        }
        # Convert data to JSON format
        json_data = json.dumps(data)
        # Send POST request to the server
        response = requests.post(self.url+'/move', json=json_data)
        # Check the response from the server
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.json()}
        
    def pizza(self, pizza_val=False):
        if pizza_val:
            response = requests.get(self.url+'/solenoidON',timeout=1)
        else:
            response = requests.get(self.url+'/solenoidOFF',timeout=1)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.json()}