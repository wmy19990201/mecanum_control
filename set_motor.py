#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import serial
import time
import numpy as np

#电机转速0-4095，一个字节0-255，可将电机转速映射到字节中，字节中一个单位对应电机16个单位
Port_ardn = 'COM3'
#Port_ardn = '/dev/ttyUSB0'
arduino = serial.Serial(Port_ardn, 9600, timeout = 1)

arduino.flushInput()
arduino.flushOutput()

wheel_ctrl = [0,0,0,0]
#send = [0,0,0,0]

left_front = 00
right_front = 00
left_rear = 00
right_rear = 500
end_sign = ';'

while True:
    right_rear = (right_rear + 16) % 4096
    wheel_ctrl = [left_front, right_front, left_rear, right_rear]
    #print(wheel_ctrl)
    for j in range(4):        
        send = chr(int(wheel_ctrl[j] / 16))#发送高两位
        #print(wheel_ctrl[j] / 16)
        arduino.write(send.encode())
        time.sleep(0.00)

    print("wheel_spd:", wheel_ctrl)

        
    
    #这句不能删，删了会导致周期错乱，很迷
    #str1 = arduino.readline().decode()
    rcv = arduino.readline().decode()
    #print(rcv)
    
		
    

    
