import scara
import logging 
import scara.can_pizza as pizza
from flask import Flask, request, jsonify
import json
import time

scara.logger.setLevel(logging.INFO)
nelen = scara.Robot()
time.sleep(1)

#example: nelen.move(point[0], point[1], 180.0,'right')
x_lims = [-200.0,200.0]
y_lims = [400.0,600.0]
z_lims = [30.0,170.0]

app = Flask(__name__)

@app.route('/move', methods=['POST'])
def move_robot():
    # Get JSON data from the request
    data = request.get_json()
    #convert data to dictionary
    data = json.loads(data)
    x_move = data['x']
    y_move = data['y']
    z_move = data['z']
    #convert data to float
    x_move = float(x_move)
    y_move = float(y_move)
    z_move = float(z_move)
    #check limits of x and y
    if x_move < -200 or x_move > 200:
        return jsonify({'status': 'error', 'message': 'x must be between 0 and 400'})
    if y_move < 400 or y_move > 600:
        return jsonify({'status': 'error', 'message': 'y must be between 400 and 600'})
    if z_move < 30 or z_move > 170:
        return jsonify({'status': 'error', 'message': 'z must be between 30 and 170'})

    nelen.move(x_move, y_move, z_move, 'right')
    print("Moving to x: ", x_move, " y: ", y_move, " z: ", z_move)
    # Return a success response
    return jsonify({'status': 'success', 'message': 'Robot moved successfully to x: ' + str(x_move) + ' y: ' + str(y_move) + ' z: ' + str(z_move)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)