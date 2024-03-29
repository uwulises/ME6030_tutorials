from client_moves_class import MoveClient

# Example usage
url = 'http://127.0.0.1:5000/move'
move_sender = MoveClient(url)
response = move_sender.send_move(100, 300)
print(response)

