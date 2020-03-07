# Look at the readme, and keep it up to date when you change the code
from Python_Code.drive import Drive
from Python_Code.robot import Robot
import time
r = Robot()  # initialize the robot

driver = Drive(r)  # initialize the driver
# driver.tankDrive(0.5, 0.5)

r.board.iterate()
driver.tankDrive(0.7,0.7)
driver.encoderRead()
driver.stop()
r.board.reset_encoders()
r.board.iterate()
# Here would be a state machine once a few more pieces are in place
# driver.tankDrive(0.5,-0.5)
# time.sleep(5)
# driver.stop()
# compass = bot.digital_ports[2]
# compass.enable_reporting()
