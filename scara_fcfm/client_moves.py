from client_moves_class import MoveClient
import time
# Example usage
url = 'http://192.168.1.100:5000/move'
move_sender = MoveClient(url)
move_sender.send_move(-350.0, 100.0, 150.0, False)