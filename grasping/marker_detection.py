#Codigo autoria de https://github.com/NNaert

import time
import cv2 # Import the OpenCV library
import numpy as np # Import Numpy library
from marker_define import *
import keyboard
from client_moves_class import MoveClient

url = 'http://192.168.1.100:5000/move'
move_sender = MoveClient(url)


start_time = time.time()
 
desired_aruco_dictionary1 = "DICT_ARUCO_ORIGINAL"
desired_aruco_dictionary2 = "DICT_ARUCO_ORIGINAL"

# mtx = [[853.06293928   0.         315.41805146]
#  [  0.         975.51888127 242.3807209 ]
#  [  0.           0.           1.        ]]
# dist :

# [[ 4.49137514e-01 -2.80151731e+01 -3.57937402e-02 -4.19449667e-03
#    2.45787043e+02]]
mtx= np.array([[853.06293928, 0., 315.41805146], [0., 975.51888127, 242.3807209], [0., 0., 1.]])
dist= np.array([4.49137514e-01, -2.80151731e+01, -3.57937402e-02, -4.19449667e-03, 2.45787043e+02])

# The different ArUco dictionaries built into the OpenCV library. 
ARUCO_DICT = {
  "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
  "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
  "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
  "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
  "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
  "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
  "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
  "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
  "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
  "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
  "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
  "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
  "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
  "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
  "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
  "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
  "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL
}

def get_markers(vid_frame, aruco_dictionary, aruco_parameters):
    _detector = cv2.aruco.ArucoDetector(aruco_dictionary, aruco_parameters)
    bboxs, ids, rejected = _detector.detectMarkers(vid_frame)
    if ids is not None:
        ids_sorted=[]
        for id_number in ids:
            ids_sorted.append(id_number[0])
    else:
        ids_sorted=ids
    return bboxs,ids_sorted

#initial framesize of the cropped window
square_points=[[10,cv2.CAP_PROP_FRAME_HEIGHT-10], [cv2.CAP_PROP_FRAME_WIDTH-10,cv2.CAP_PROP_FRAME_HEIGHT-10], [cv2.CAP_PROP_FRAME_WIDTH-10, 10], [10,10]] #initial square

init_loc_1=[0,0]
init_loc_2=[300,0]
init_loc_3=[300,300]
init_loc_4=[0,300]

x_lims = [-400.0,300.0]
y_lims = [200.0,600.0]
z_lims = [30.0,170.0]


#initiaize locations
current_square_points=[init_loc_1,init_loc_2,init_loc_4,init_loc_3]
current_center_Corner=[[0,0]]


#use location hold
marker_location_hold=True

def main():
   
    # Load the ArUco dictionary
    
    this_aruco_dictionary1 = cv2.aruco.getPredefinedDictionary(ARUCO_DICT[desired_aruco_dictionary1])   #for 4x4 markers
    this_aruco_parameters1 = cv2.aruco.DetectorParameters()  #for 4x4 markers
    this_aruco_dictionary2 = cv2.aruco.getPredefinedDictionary(ARUCO_DICT[desired_aruco_dictionary2])  #for 6x6 markers
    this_aruco_parameters2 = cv2.aruco.DetectorParameters()  #for 6x6 markers
    
    # Start the video stream
    cap = cv2.VideoCapture(1)
    
    
    square_points=current_square_points


    while(True):
        

        current_time=time.time()
        delay=0 #seconds , set to zero if not an demo

        
        ret, frame = cap.read()  
        #img = cv.imread('left12.jpg')
        h, w = frame.shape[:2]
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
        undistorted = cv2.undistort(frame, mtx, dist, None, newcameramtx)

        frame = undistorted
        
        
        # Detect 4x4 ArUco markers in the video frame
        markers,ids=get_markers(frame, this_aruco_dictionary1, this_aruco_parameters1)

        #create copy of te initial 'clean frame'
        frame_clean=frame.copy()

        #get info over the different markers and display info
        left_corners,corner_ids=getMarkerCoordinates(markers,ids,0)


        #update the markers positions when a markers is found. When no marker is found, use previous location
        if marker_location_hold==True:
            if corner_ids is not None:
                count=0
                for id in corner_ids:
                    
                    if id>4:
                        break  #sometimes wring values are read
                    current_square_points[id-1]=left_corners[count]
                    count=count+1
            left_corners=current_square_points            
            corner_ids=[1,2,3,4]      

        
        if (start_time+delay*1)<current_time and (start_time+delay*2)>current_time:   
            cv2.aruco.drawDetectedMarkers(frame, markers) #built in open cv function
        if (start_time+delay*2)<current_time:    
            draw_corners(frame,left_corners)
        if (start_time+delay*3)<current_time:
            draw_numbers(frame,left_corners,corner_ids)
        if (start_time+delay*4)<current_time:    
            show_spec(frame,left_corners)
       
        frame_with_square,squareFound=draw_field(frame,left_corners,corner_ids)
        
            
        #####look for foam    
        #extract square and show in extra window
        if (start_time+delay*6)<current_time:
            if squareFound:
                square_points=left_corners
            img_wrapped=four_point_transform(frame_clean, np.array(square_points))
            # look for foam, Detect 6x6 ArUco markers in the video frame
            h, w, c = img_wrapped.shape
            marker_foam,ids_foam=get_markers(img_wrapped, this_aruco_dictionary2, this_aruco_parameters2)
            left_corner_foam,corner_id_foam=getMarkerCoordinates(marker_foam,ids_foam,0)
            centerCorner=getMarkerCenter_foam(marker_foam)
           
            #update the markers positions when a markers is found. When no marker is found, use previous location
            if marker_location_hold==True:
                if corner_id_foam is not None:
                    #only one piece of foam
                    
                    current_center_Corner[0]=centerCorner[0]
                centerCorner[0]=current_center_Corner[0]              
                

            draw_corners(img_wrapped, centerCorner)
            #draw cross over frame
            img_wrapped=cv2.line(img_wrapped,(centerCorner[0][0],0), (centerCorner[0][0],h), (0,0,255), 2)
            img_wrapped=cv2.line(img_wrapped,(0,(centerCorner[0][1])), (w,(centerCorner[0][1])), (0,0,255), 2)

            draw_numbers(img_wrapped,left_corner_foam,corner_id_foam)
            cv2.imshow('img_wrapped',img_wrapped)       
        
        # Display the resulting frame
        cv2.imshow('frame_with_square',frame_with_square)
        #cv2.imshow('img_cropped',img_cropped)    
        # If "q" is pressed on the keyboard, 
        # exit this loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
        if keyboard.is_pressed('c'):
            move_sender.send_move(-200, 400, z=150)
            time.sleep(2)
        # #pick up piece of foam    q
        if keyboard.is_pressed('p'):
            
            x_coordinate=int((centerCorner[0][1]/h)*600)
            y_coordinate=int((centerCorner[0][0]/w)*300)
            
            x_scara = -y_coordinate -125
            y_scara = x_coordinate + 120
            print(x_scara, y_scara)
            #if the position is within the range of the robot, send the move
            if x_scara > x_lims[0] and x_scara < x_lims[1] and y_scara > y_lims[0] and y_scara < y_lims[1]:
                move_sender.send_move(x_scara, y_scara, z=100)
                print("Sent move: ", x_scara,y_scara, 100)
                time.sleep(3)
                

            
            
    # Close down the video stream
    cap.release()
    cv2.destroyAllWindows()
    return centerCorner 
   

if __name__ == '__main__':
    
    foam_center=main()  #pull foam location from markers