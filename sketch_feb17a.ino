

#include <Wire.h>
#include <Zumo32U4.h>

LSM303 compass;
Zumo32U4Motors moto;
Zumo32U4LCD lcd;
int zero = 0;
bool halt = true;
void setup(){
 delay(1000);
 lcd.clear();
 Wire.begin();
 if (!compass.init())
  {
    // Failed to detect the compass.
    ledRed(1);
    while(1)
    {
      Serial.println(F("Failed to detect the compass."));
      delay(100);
    }
  }

  compass.enableDefault();
  compass.read();
  zero = compass.a.x;
}
void loop(){
 while(abs(compass.a.x-zero)<90 && halt){
  moto.setLeftSpeed(-70);
  moto.setRightSpeed(70);
  lcd.print("IL");
 }
 halt = false;
moto.setLeftSpeed(0);
moto.setRightSpeed(0);
}
