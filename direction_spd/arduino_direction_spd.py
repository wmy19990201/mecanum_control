#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import serial
import time
import numpy as np

#电机转速0-4095，一个字节0-255，可将电机转速映射到字节中，字节中一个单位对应电机16个单位
Port_ardn = 'COM3'



class send_data:
    def __init__(self, Port_ardn):
        self.arduino = serial.Serial(Port_ardn, 9600, timeout = 1)
        self.data = 0
        
    def read_data(self, data):
        self.data = data
    
    def init_setup(self):
        self.arduino.flushInput()
        self.arduino.flushOutput()
        
    def send_msg(self):
        self.arduino.write(chr(self.data).encode("utf-8"))
        time.sleep(0.01)
        print("data sent:", bin(self.data))
        
    def rcv_msg(self):
        rcv = self.arduino.readline().decode()
        print(rcv)
        
    def intereption(self):
        self.arduino.write(chr(0).encode("utf-8"))
        print("stop")
        self.arduino.flushInput()
        self.arduino.flushOutput()
        self.arduino.close()
        
def encode_spd_direction(direction, spd):
    #为了提高分辨率对电机限速
    if spd >= 2048:
        spd = 2047
    data = direction * 0b10000 + spd/128#高四位为方向，第四位是速度
    return int(data)        

    
        

if __name__ == '__main__':
    
    
    ser = send_data(Port_ardn)
    ser.init_setup()
    direction = 0
    
    try:
        while True:
            direction = (direction + 1) % 11
            print("direction:", direction)
            ser.init_setup()
            msg = encode_spd_direction(direction, 500)
            ser.read_data(msg)
            #print("msg=",bin(msg))
            ser.send_msg()
            ser.rcv_msg()
            time.sleep(3)
        
    except KeyboardInterrupt:
        ser.intereption()
        
    
