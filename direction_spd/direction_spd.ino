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
int comdata = 0;
int direction = 0;
int spd = 0;
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
    
}

void loop() {
  Serial.flush();
   while (Serial.available() > 0)//串口接收到数据
  {
    comdata = Serial.read();//获取串口接收到的数据
    //comdata高四位表示方向0-10，低四位表示速度0-2047/128
    direction = comdata / 16;
    spd = 128 * (comdata - direction * 16);
    //Serial.println(comdata);
    //Serial.println(spd);
    //Serial.println(direction);
    if (direction == 0) //如果上位机发送的为字符，则改为'0'
    {
       motorDirver.setMotor(0, 0, 0, 0);  // 电机M1/M2/M3/M4停止
       //delay(1000);        
      Serial.println("Stop"); //向上位机发送信息
    }
    if (direction == 1)  //向前
    {
       motorDirver.setMotor(spd, spd, spd, spd); 
      Serial.println("Move forward"); //向上位机发送信息
    }
     if (direction == 5)  //向后
    {
       motorDirver.setMotor(-spd, -spd, -spd, -spd); 
      Serial.println("Move backward"); //向上位机发送信息
    }
     if (direction == 3)  //向左
    {
       motorDirver.setMotor(-spd, spd, spd, -spd); 
      Serial.println("Move left"); //向上位机发送信息
    }
     if (direction == 7)   //向右
    {
       motorDirver.setMotor(spd, -spd, -spd, spd); 
      Serial.println("Move right"); //向上位机发送信息
    }
     if (direction == 2)   //左前
    {
       motorDirver.setMotor(0, spd, spd, 0); 
      Serial.println("Move left-forward"); //向上位机发送信息
    }
     if (direction == 8)   //右前
    {
       motorDirver.setMotor(spd, 0, 0, spd);
      Serial.println("Move right-forward"); //向上位机发送信息
    }
     if (direction == 4)   //左后
    {
       motorDirver.setMotor(-spd, 0, 0, -spd);  
      Serial.println("Move left-backward"); //向上位机发送信息
    }
     if (direction == 6)  //右后
    {
       motorDirver.setMotor(0, -spd, -spd, 0);
      Serial.println("Move right-backward"); //向上位机发送信息
    }
     if (direction == 9)  //右转
    {
       motorDirver.setMotor(spd, -spd, spd, -spd);
      Serial.println("Move right-round"); //向上位机发送信息
    }
    if (direction == 10)  //左转
    {
       motorDirver.setMotor(-spd, spd, -spd, spd);
      Serial.println("Move left-round"); //向上位机发送信息
    }

  }

  
}
