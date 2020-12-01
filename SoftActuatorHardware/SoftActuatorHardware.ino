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

int fsrPin = 1;     // the FSR and 10K pulldown are connected to a0
int fsrReading;     // the analog reading from the FSR resistor divider
int fsrVoltage;     // the analog reading converted to voltage
float fsrResistance;  // The voltage converted to resistance
float fsrConductance; 
float fsrForce;       // Finally, the resistance converted to 
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
void TX(float pressure,float fsrForce, unsigned long times)
{
  Serial.print(times / 1000.0, 2);
  Serial.print(',');
  Serial.print(pressure);
  Serial.print(',');
  Serial.print(fsrForce);
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
  fsrReading = analogRead(A1);  
  // analog voltage reading ranges from about 0 to 1023 which maps to 0V to 5V (= 5000mV)
  fsrVoltage = map(fsrReading, 0, 1023, 0, 5000);
  // put your main code here, to run repeatedly:
  fsrResistance = 5000 - fsrVoltage;     // fsrVoltage is in millivolts so 5V = 5000mV
  fsrResistance *= 10000;                // 10K resistor
  fsrResistance /= fsrVoltage;
  fsrConductance = 1000000;           // we measure in micromhos so 
  fsrConductance /= fsrResistance;
    
 
    // Use the two FSR guide graphs to approximate the force
    if (fsrConductance <= 1000) {
      fsrForce = fsrConductance / 80;
      //Serial.print("Force in Newtons: ");    
    } else {
      fsrForce = fsrConductance - 1000;
      fsrForce /= 30;
      //Serial.print("Force in Newtons: ");         
    }
  TX(pressure,fsrForce,times);
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
