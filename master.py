# Look at the readme, and keep it up to date when you change the code
from Python_Code.drive import Drive
from Python_Code.robot import Robot
from Python_Code.navigation import Navigation
import time

IN_FRONT, LEFT, CLOCKWISE = 0
BEHIND, MIDDLE, COUNTERCLOCKWISE = 1
RIGHT = 2

# state codes
START = 0
MAKE_PASS = 1
UNLOAD = 2
STOP = 3
NEXT_ACTION = 4

RIGHT_TURN = 150
TO_END = 800

timeout = 60

r = Robot()  # initialize the robot
driver = Drive(r)  # initialize the driver
nav = Navigation(r, driver)  # initialize the nav
# driver.tankDrive(0.5, 0.5)
running = True
state = START
pos = 0
pass_direction = RIGHT


startTime = time.time()
r.reset_encoders()

start_state = 0


def start():
    global start_state
    if start_state == 0:
        driver.startEncoderDrive(30, 30)
        start_state = 1
        return False
    elif start_state == 2:
        if driver.targetReached:
            start_state = 3
        return False
    elif start_state == 3:
        driver.startEncoderTurn(RIGHT_TURN, COUNTERCLOCKWISE)
        start_state = 4
        return False
    elif start_state == 4:
        if driver.targetReached:
            start_state = 5
        return False
    elif start_state == 5:
        if nav.squareUp(BEHIND):
            return True
        else:
            return False


pass_state = 0


def makePass(direction):
    global pass_state
    r.intake()
    if direction == RIGHT:
        turn_dir = CLOCKWISE
    elif direction == LEFT:
        turn_dir = COUNTERCLOCKWISE
    if pass_state == 0:
        driver.startEncoderDrive(TO_END, TO_END, 0.7)
        pass_state = 1
        return MAKE_PASS
    elif pass_state == 1:
        if driver.targetReached:
            pass_state = 2
        return MAKE_PASS
    elif pass_state == 2:
        driver.startEncoderTurn(RIGHT_TURN, turn_dir)
        pass_state = 3
        return MAKE_PASS
    elif pass_state == 3:
        if driver.targetReached:
            pass_state = 4
        return MAKE_PASS
    elif pass_state == 4:
        driver.startEncoderDrive(50, 50)
        pass_state = 5
        return MAKE_PASS
    elif pass_state == 5:
        if driver.targetReached:
            pass_state = 6
        return MAKE_PASS
    elif pass_state == 6:
        driver.startEncoderTurn(RIGHT_TURN, turn_dir)
        pass_state = 7
        return MAKE_PASS
    elif pass_state == 7:
        if driver.targetReached:
            pass_state = 8
        return MAKE_PASS
    elif pass_state == 8:
        if nav.driveToLine():
            return NEXT_ACTION
        else: 
            return MAKE_PASS



unload_state = 0


def unload():
    pass


def stop():
    pass


def nextAction():
    pass


while running:
    if r.board.bytes_available():
        while r.board.bytes_available():
            r.board.iterate()
    if time.time() - startTime > timeout:
        print("timed out")
        running = False
    driver.iterate()
    nav.iterate()
    if state == START:
        if start():
            state = MAKE_PASS
            pass_direction = RIGHT
    elif state == MAKE_PASS:
        state = makePass(RIGHT)
        if state != MAKE_PASS:
            pass_state = 0
    elif state == UNLOAD:
        state = unload()
        if state != UNLOAD:
            unload_state = 0
    elif state == STOP:
        stop()
        running = False
    elif state == NEXT_ACTION:
        state = nextAction()


print('done')
driver.stop()