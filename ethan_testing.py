from Python_Code.drive import Drive
from Python_Code.robot import Robot
from Python_Code.navigation import Navigation
import time

IN_FRONT, LEFT, CLOCKWISE = 0, 0, 0
BEHIND, MIDDLE, COUNTERCLOCKWISE = 1, 1, 1
RIGHT = 2

r = Robot()  # initialize the robot
driver = Drive(r)  # initialize the driver
nav = Navigation(r, driver)  # initialize the nav

startTime = time.time()

timeout = 45

running = True
state = 0

while running:

    if r.board.bytes_available():
        while r.board.bytes_available():
            r.board.iterate()
    if time.time() - startTime > timeout:
        print("timed out")
        running = False
    driver.iterate()
    nav.iterate()

    if state == 0:
        driver.startEncoderDrive(4000, 4000)
        state = 1
    elif state == 1:
        if driver.targetReached:
            state = 2
    elif state == 2:
        running = False

driver.stop()
print('done')
