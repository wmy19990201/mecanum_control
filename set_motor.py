#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import serial
import time
import numpy as np

#电机转速0-4095，一个字节0-255，可将电机转速映射到字节中，字节中一个单位对应电机16个单位
Port_ardn = 'COM3'

wheel_ctrl = [0,0,0,0]

left_front = 00
right_front = 00
left_rear = 00
right_rear = 500
end_sign = ';'


def encode_array_0812(wheel_ctrl):
    def encode_spd_0812(spd):
        #由于chr()无法处理负数，若spd<0，则给其加10000
        #完成映射 0-4095：0-63  -1-（-4095）：64-127
        if (spd < 0):
            result = int(abs(spd) / 64 + 0b1000000)
        else:
            result = int(spd/64)
        return result
    
    #加入电机号、起始位（127）、终止位(126)
    encode_array = [127, 0, encode_spd_0812(wheel_ctrl[0]), 1, encode_spd_0812(wheel_ctrl[1]), 2, encode_spd_0812(wheel_ctrl[2]), 3, encode_spd_0812(wheel_ctrl[3]), 126]
    return encode_array         
    
        
        
#根据direction:0-9 和spd 设置四个电机转速wheel_ctrl[4]
def direction_ctrl(direction, spd):
    #设置一个字典，达到C++ switch的效果
    def stop():
        wheel_ctrl = [0,0,0,0]
        return wheel_ctrl
        
    def forward():
        wheel_ctrl = [spd,spd,spd,spd]
        return wheel_ctrl
    
    def backward():
        wheel_ctrl = [-spd,-spd,-spd,-spd]
        return wheel_ctrl
        
    def left():
        wheel_ctrl = [-spd, spd, spd, -spd]
        return wheel_ctrl
    
    def right():
        wheel_ctrl = [spd, -spd, -spd, spd]
        return wheel_ctrl
    
    def left_forward():
        wheel_ctrl = [0, spd, spd, 0]
        return wheel_ctrl
        
    def right_forward():
        wheel_ctrl = [spd, 0, 0, spd]
        return wheel_ctrl
        
    def left_backward():
        wheel_ctrl = [-spd, 0, 0, -spd]
        return wheel_ctrl
        
    def right_backward():
        wheel_ctrl = [0, -spd, -spd, 0]
        return wheel_ctrl
        
    def right_round():
        wheel_ctrl = [spd, -spd, spd, -spd]
        return wheel_ctrl
        
    def left_round():
        wheel_ctrl = [-spd, spd, -spd, spd]
        return wheel_ctrl
        
    switch = {
        0: stop,
        1: forward,
        2: backward,
        3: left,
        4: right,
        5: left_forward,
        6: right_forward,
        7: left_backward,
        8: right_backward,
        9: right_round,
        10: left_round,
        }
        
    result = switch.get(direction)()
    return result

class send_data:
    def __init__(self, Port_ardn):
        self.arduino = serial.Serial(Port_ardn, 9600, timeout = 1)
        self.data = np.zeros(10)
        
    def read_data(self, data):
        self.data = data
    
    def init_setup(self):
        self.arduino.flushInput()
        self.arduino.flushOutput()
        
    def send_msg(self):
        for j in range(10):          
            self.arduino.write(chr(self.data[j]).encode("utf-8"))
            time.sleep(0.01)
        print("data sent")
        
    def rcv_msg(self):
        rcv = self.arduino.readline().decode()
        print(rcv)
        
    def intereption(self):
        self.arduino.write(chr(125).encode("utf-8"))
        print("stop")
        self.arduino.flushInput()
        self.arduino.flushOutput()
        self.arduino.close()
        
        

#def direction_test():
#    wheel_ctrl = direction_ctrl(direction, 500)
#    direction = (direction + 1) % 11
    
        

if __name__ == '__main__':
    msg = encode_array_0812([0,-500,0,0])

    
    ser = send_data(Port_ardn)
    ser.init_setup()
    
    try:
        ser.init_setup()
        ser.read_data(msg)
        print("msg=",msg)
        ser.send_msg()
        ser.rcv_msg()
        
    except KeyboardInterrupt:
        ser.intereption()
        
    
