//#include <Arduino.h>

//Define Hardware PINS

#define BendingVavle 8
#define StraightValve 4
#define DefalteValve 7

#define motorPWM 11
#define motorEN 12

#define masterStop 6
//
//Global Init
int count = 0;

void setup()
{
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(masterStop, INPUT_PULLUP);
  pinMode(BendingVavle, OUTPUT);
  pinMode(StraightValve, OUTPUT);
  pinMode(DefalteValve, OUTPUT);
  pinMode(motorPWM,OUTPUT);
  pinMode(motorEN,OUTPUT);
  // Initially Solenoid turned off.
  digitalWrite(BendingVavle, HIGH);
  digitalWrite(StraightValve, HIGH);
  digitalWrite(DefalteValve, HIGH);
}
// Serial Data transfer.
void TX(float pressure, unsigned long times)
{
  Serial.print(times / 1000.0, 2);
  Serial.print(',');
  Serial.print(pressure);
  Serial.println(' ');
}

// Bending Valve Realy Switch Function
void BendingValveSW(int flag)
{
  digitalWrite(DefalteValve,HIGH);
  digitalWrite(BendingVavle, flag);
}

// Deflate Valve Realy Switch Function
void DeflateValveSW(int flag)
{
  digitalWrite(motorEN,LOW);
  digitalWrite(BendingVavle,HIGH);
  digitalWrite(DefalteValve, flag);
}

// l298n Motor speed control Function 
void MotorControls(int level)
{
  digitalWrite(motorEN,HIGH);
  switch (level)
  {
  case 1:
    analogWrite(motorPWM, 85); // Slow Speed.
    break;
  case 2:
    analogWrite(motorPWM, 170); // Medium Speed.
    break;
  case 3:
    analogWrite(motorPWM, 255); // High Speed.
    break;
  default:
    analogWrite(motorPWM, 170); // Medium Speed Default Case.
    break;
  }
}

void loop()
{
  // put your main code here, to run repeatedly:

  // Keep in mind the pull-up means the pushbutton's logic is inverted. It goes
  // HIGH when it's open, and LOW when it's pressed.
  if (digitalRead(masterStop) == 0)
  {
    DeflateValveSW(1);
    //Implement motor control.
  }
  unsigned long times = millis();
  float rawValue = analogRead(A0);
  float voltage = rawValue * (5.0/1023.0);
  float pressure = (voltage-0.04*5.0)/(5.0*0.0012858);
  TX(pressure, times);
  delay(50);
  
  if (Serial.available() > 0)
  {
    int inByte = Serial.read();
    switch (inByte)
    {
    case 'A':
      BendingValveSW(0); // If Serial reads 'A' execute this case.
      break;
    case 'B':
      BendingValveSW(1); // If Serial reads 'B' execute this case.
      break;
    case 'C':
      DeflateValveSW(0); // If Serial reads 'C' execute this case.
      break;                             
    case 'D':                           
      DeflateValveSW(1);                
      break;                            
    case 'E':                            
      MotorControls(1);                  
      break;
    case 'F':
      MotorControls(2);
      break;
    case 'G':
      MotorControls(3);
      break;
    }
  }
}
