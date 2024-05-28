from client_moves_class import MoveClient
import time
# Example usage
url = 'http://192.168.1.100:5000'
move_sender = MoveClient(url)
move_sender.send_move(-350.0, 200.0, 170.0)
move_sender.pizza(True)
time.sleep(1)
move_sender.pizza(False)