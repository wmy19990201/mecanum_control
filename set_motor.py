#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import serial
import time
import numpy as np

#电机转速0-4095，一个字节0-255，可将电机转速映射到字节中，字节中一个单位对应电机16个单位#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import serial
import time
import numpy as np

#电机转速0-4095，一个字节0-255，可将电机转速映射到字节中，字节中一个单位对应电机16个单位
Port_ardn = 'COM3'
#Port_ardn = '/dev/ttyUSB0'
#---arduino = serial.Serial(Port_ardn, 9600, timeout = 1)

#---arduino.flushInput()
#---arduino.flushOutput()

wheel_ctrl = [0,0,0,0]
#send = [0,0,0,0]

left_front = 00
right_front = 00
left_rear = 00
right_rear = 500
end_sign = ';'

def encode_spd(spd):
    tmp = spd.to_bytes(2, byteorder='big', signed=True)#大数端存储
    print(tmp)
    result = tmp & bytes(0b000111111111)#语法错误
    #print("spd:", result)
    #return result

#将int类型的wheel_ctrl数组（一共4个元素）编为12byte（起始字节+4*3）数据:0b000x xxxx xxxx
def encode_array(wheel_ctrl):
    #正副4095占13个二进制位，因此在2Byte中，最高3位置为0，后13位记录速度
    def encode_spd(spd):
        tmp = spd.to_bytes(2, byteorder='big', signed=True)#大数端存储
        print(tmp)
        result = tmp & 0b000111111111
        print("spd:", result)
        return result
    
    def encode_wheelID(ID):#将轮子ID编入一个Byte中:0b111111xx
        tmp = ID.to_bytes(1, byteorder = 'big', signed = False)
        result = tmp | 0b11111100
        print("ID:",result)
        return result
    
    upload_data = []
    for i in range(0, 4):
        upload_data.append(encode_wheelID(i))
        upload_data.append(encode_spd(wheel_ctrl[i]))
        
    return upload_data
        
        
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

#def direction_test():
#    wheel_ctrl = direction_ctrl(direction, 500)
#    direction = (direction + 1) % 11
    
        

if __name__ == '__main__':
    spd_encoded = encode_spd(0b101)
    print(spd_encoded)
        
    
'''
while True:
    #right_rear = (right_rear + 16) % 4096
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
'''    
		
    

    

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
    
		
    

    
