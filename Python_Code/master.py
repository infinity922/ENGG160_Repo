# Look at the readme, and keep it up to date when you change the code
from Python_Code.drive import Drive
from Python_Code.robot import Robot
import time
r = Robot()  # initialize the robot

driver = Drive(r)  # initialize the driver
# driver.tankDrive(0.5, 0.5)

running = True
state = 0

while running:
    r.board.iterate()
    driver.tankDrive(0.4, 0.4)