/***************************************************
  Motor Test - Confirm the direction of the motor.
             - 确认电机方向
  观察实际运行，通过 .setMotorDirReverse()函数设置电机运行方向。

  YFROBOT ZL
  yfrobot@qq.com
  WWW.YFROBOT.COM
  08/19/2020
 ****************************************************/
int counter=0; // 计数器
byte buffer[8] = {0,0,0,0,0,0,0,0};
int comdata[4] = {0,0,0,0};
#include <MotorDriver_PCA9685.h>

// called this way, it uses the default address 0x40
MotorDriver_PCA9685 motorDirver = MotorDriver_PCA9685();

void setup() {
  Wire.begin();  // join the TWI as the master
  Serial.begin(9600);
  Serial.println("Motor Drive test!");
  motorDirver.begin();
  // motorDirver.setPWMFreq(1600);       // This is the maximum PWM frequency
  // motorDirver.setMotorDirReverse(0);  // 设置所有电机方向, 0-默认,1-反向.
  motorDirver.setMotorDirReverse(0, 1, 0, 1); // 设置M1,M2,M3,M4电机方向, 0-默认,1-反向.
  Serial.println("Start...");
  motorDirver.setMotor(0, 0, 0, 0); 
  //Serial.flush(); 
    
}

void loop()
{  
   while (Serial.available() > 0)//串口接收到数据
  { 

      Serial.readBytes(buffer, 4);
      
      for(int i = 0; i < 4; ++ i)
      {
        comdata[i] = buffer[i] * 16;
        Serial.println(comdata[i]);
      }
   
    //设置电机转速
    motorDirver.setMotor(comdata[0], comdata[1], comdata[2], comdata[3]);
    //向上位机发送信息 "setMotor:(comdata[0],comdata[1],comdata[2],comdata[3])
    //Serial.println("setMotor:");
    //for(int i = 0; i < 4; ++ i)
      //Serial.println(comdata[i]);
    //Serial.println("-----------------------------------------");
    
    
   }

  
}
