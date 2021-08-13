#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import serial
import time
import numpy as np
#一个字节管方向，一个字节管速度
#电机转速0-4095，将速度字节最高位置为0，一个字节0-127，可将电机转速映射到字节中，字节中一个单位对应电机32个单位
#将方向字节高四位置为1，后四位记录方向（0-10）
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
    if spd <= 4095 and spd >=0:
        spd_encoded = spd/32 + 0b00000000
    elif spd > 4095:
        spd_encoded = 4095/32 + 0b00000000
    else:
        spd_encoded = 0
    
    if direction >=0 and direction <=10:
        direction_encoded = direction + 0b11110000
    else:
        direction_encoded = 0b11110000
        
    return [int(direction_encoded), int(spd_encoded)]
        
def set_direction_spd(direction, spd, Port_ardn):
    ser = send_data(Port_ardn)
    ser.init_setup()
    
    try:
        while True:
            #direction = (direction + 1) % 11
            print("spd:", spd)
            print("direction:", direction)
            ser.init_setup()
            msg = encode_spd_direction(direction, spd)
            ser.read_data(msg[0])
            ser.send_msg()
            ser.read_data(msg[1])
            ser.send_msg()
            ser.rcv_msg()
            time.sleep(3)
        
    except KeyboardInterrupt:
        ser.intereption()
        

if __name__ == '__main__':
    set_direction_spd(1, 500, Port_ardn)
    
    
    
