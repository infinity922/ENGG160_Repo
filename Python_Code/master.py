# Look at the readme, and keep it up to date when you change the code
from drive import Drive
from robot import Robot
import time
r = Robot()  # initialize the robot

driver = Drive(r)  # initialize the driver
# driver.tankDrive(0.5, 0.5)
running = True
state = 0

while running:
    if r.board.bytes_available():
        while r.board.bytes_available():
            r.board.iterate()
    pos = 0
    if state is 0:
        driver.tankDrive(0.4, 0.4)
        pos = driver.encoderRead()
        print(pos)
        if pos >= 5000:
            state += 1
    elif state is 1:
        driver.stop()
        r.reset_encoders()
        pos = r.get_left_encoder()
        print('After Reset: ')
        print(pos)
        state += 1
    elif state is 2:
        running = False

print('done')