import time
import cv2 
import numpy as np 
import keyboard
from client_moves_class import MoveClient
from hanoi_solver import HanoiSolver

#scara arm object
url = 'http://192.168.1.100:5000/move'
move_sender = MoveClient(url)

#Hanoi solver object
hanoi_solver = HanoiSolver(n_disks=8)

# Start the video stream
top_cam = cv2.VideoCapture(0)
azimut_cam = cv2.VideoCapture(1)

# Flags
flag_border_id = False
flag_solved = False
flag_move = False
flag_start = False
flag_goal_reached = False

def get_base_projection(base_frame):
    # Get the base borders
    base_border_frame=base_frame
    obj_points = [] #3d points in real world space
    return base_border_frame, obj_points

def get_disk_ids(disk_frame):
    # Get the disk borders
    disk_border_frame=disk_frame
    ids_sorted = [] #ids of the disks
    return disk_border_frame, ids_sorted

def main():
    global flag_border_id, flag_solved, flag_move, flag_start

    while True:       
        ret, top_frame = top_cam.read()
        ret2, azimut_frame = azimut_cam.read()
        #resize the frames to 640x480
        top_frame = cv2.resize(top_frame, (640, 480))
        azimut_frame = cv2.resize(azimut_frame, (640, 480))

        base_border_frame, obj_points = get_base_projection(azimut_frame)
        disk_border_frame, ids_sorted = get_disk_ids(azimut_frame)

        #check every frame
        

        # Check if the borders and ids are detected
        if flag_border_id:
            # Check if the hanoi tower is solved
            hanoi_solved_list = hanoi_solver.solve()
            if flag_solved:
                # Send the move to the scara arm
                for move in hanoi_solved_list:
                    if flag_move:
                        # Send the move to the scara arm
                        move = []
                        move_sender.send_move(move)
                        if flag_goal_reached:
                            # The scara arm reached the goal
                            break
            

        # Display the resulting frame
        cv2.imshow('Top Camera', top_frame)
        cv2.imshow('Azimut Camera', azimut_frame)
        
        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    main()