#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import serial
import time
import numpy as np

Port_ardn = 'COM3'
#Port_ardn = '/dev/ttyUSB0'
arduino = serial.Serial(Port_ardn, 9600, timeout = 1)

arduino.flushInput()
arduino.flushOutput()

wheel_ctrl = [0,0,0,0]
#send = [0,0,0,0]

left_front = 400
right_front = 400
left_rear = 400
right_rear = 400
end_sign = ';'

while True:
    wheel_ctrl = [left_front, right_front, left_rear, right_rear]
    #print(wheel_ctrl)
    for j in range(4):          
        #arduino.write(chr(wheel_ctrl[j]).encode("utf-8"))
        tmp_high = wheel_ctrl[j] / 100
        tmp_low = wheel_ctrl[j] % 100
        #print(tmp_high,tmp_low)
        
        send = chr(int(tmp_high))#发送高两位
        arduino.write(send.encode())
        time.sleep(0.01)

        send = chr(int(tmp_low))#发送低两位
        arduino.write(send.encode())
        time.sleep(0.01)
    
        '''
    send = end_sign#发送数组分割符
    arduino.write(send.encode())
    time.sleep(0.01)


    
    
    #将10进制车轮转速转化为16进制，以大数端存储
    wheel_ctrl[0] = left_front.to_bytes(2, 'big')#大数端
    #print(type(wheel_ctrl[0]))
    wheel_ctrl[1] = right_front.to_bytes(2, 'big')
    wheel_ctrl[2] = left_rear.to_bytes(2, 'big')
    wheel_ctrl[3] = right_rear.to_bytes(2, 'big')
    #print(wheel_ctrl)
    arduino.write(wheel_ctrl[0])
    
    #将方向指令传递给控制板子  
    #int转换为byte,并发送，最后发送终止符号，每个指令信号长9byte(2*4+1)
    for i in range(0,4):
        #tmp = wheel_ctrl[i]
        #send = tmp.to_bytes(2, byteorder='little', signed=True)
        #arduino.write(send)
        
        send = chr(int(4096))
        arduino.write(send.encode())
        #print('send = ',send)
    #arduino.write(end_sign)
    #print('-----------------------')
    #arduino.write(send)
    
    send = chr(int(1000))
    arduino.write(1000)
    '''
    str1 = arduino.readline().decode()
    rcv = arduino.readline().decode()
    print(rcv)
    
		
    

    
