from Python_Code.drive import Drive
from Python_Code.robot import Robot
from Python_Code.navigation import Navigation
import time

r = Robot()  # initialize the robot
driver = Drive(r)  # initialize the driver
nav = Navigation(r, driver)  # initialize the nav

startTime = time.time()

timeout = 300

running = True

while running:

    if r.board.bytes_available():
        while r.board.bytes_available():
            r.board.iterate()
    if time.time() - startTime > timeout:
        print("timed out")
        running = False