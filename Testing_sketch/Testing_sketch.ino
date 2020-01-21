#include <Wire.h>
#include <Zumo32U4.h>

Zumo32U4LCD lcd;
Zumo32U4Motors motors;
Zumo32U4ButtonA buttonA;
Zumo32U4LineSensors ls;


void setup() {
  // put your setup code here, to run once:
  lcd.clear();
  ls.initFiveSensors();
  lcd.print(F("Press A"));
  buttonA.waitForButton();
  lcd.clear();

}

void loop() {
  // put your main code here, to run repeatedly:
  motors.setSpeeds(400,400);
  

}
