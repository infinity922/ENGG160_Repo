# Look at the readme, and keep it up to date when you change the code
from Python_Code.drive import Drive
from Python_Code.robot import Robot
import time

timeout = 60

r = Robot()  # initialize the robot
driver = Drive(r)  # initialize the driver
# driver.tankDrive(0.5, 0.5)
running = True
state = 0
pos = 0


startTime = time.time()
r.reset_encoders()
while running:
    if r.board.bytes_available():
        while r.board.bytes_available():
            r.board.iterate()
    if time.time() - startTime > timeout:
        print("timed out")
        running = False
    driver.iterate()
    if state == 0:
        driver.tankDrive(-0.4, 0.4)
        pos = r.get_right_encoder()
        print(pos)
        if pos >= 8000:
            state += 1
    elif state == 1:
        driver.stop()
        r.reset_encoders()
        pos = r.get_encoders()
        print('After Reset: ')
        print(pos)
        state += 1
    elif state == 2:
        if time.time() >= (startTime + 20):
            state += 1
    elif state == 3:
        driver.startEncoderDrive(8000, 8000, 0.4)
        state += 1
    elif state == 4:
        if driver.targetReached:
            state += 1
    elif state == 5:
        running = False

print('done')
driver.stop()