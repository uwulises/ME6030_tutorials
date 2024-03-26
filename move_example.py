from serialcontrol import SerialControl
import time


scara = SerialControl(port='COM3', baudrate=115200)
scara.open_serial()
scara.send_command([100,100])
time.sleep(2)
scara.send_command([0,0])
time.sleep(2)
scara.close_serial()