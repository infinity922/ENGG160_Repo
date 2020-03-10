import math
import Wire.h
import Zumo32U4.h

#LSM303 compass
#Zumo32U4LCD lcd

calibration = 0
conversion = 0.000080

Wire.begin()
compass.init()
compass.enableDefault()

compass.read()
lcd.clear()
#value = compass.m.z * conversion + calibration for the default number
if compass.m.y > 0:
  value = 90 - math.atan(compass.m.x / compass.m.y)*(180/math.pi)
elif compass.m.y < 0:
  value = 270 - math.atan(compass.m.x / compass.m.y)*(180/math.pi)
elif compass.m.y and (compass.m.x < 0):
  value = 180
elif compass.m.y and (compass.m.x > 0):
   value = 0
else:
  value = 0

lcd.print(value)
lcd.print(" ")
delay(500)

# to convert compass.m to a direction: (untested)
# value = math.atan(compass.m.x / compass.m.y)*(180/math.pi)