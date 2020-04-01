# Look at the readme, and keep it up to date when you change the code
import math

from Python_Code.drive import Drive
from Python_Code.robot import Robot
from Python_Code.navigation import Navigation
import time

IN_FRONT, LEFT, CLOCKWISE = 0, 0, 0
BEHIND, MIDDLE, COUNTERCLOCKWISE = 1, 1, 1
RIGHT = 2

# state codes
START = 0
MAKE_PASS = 1
UNLOAD = 2
STOP = 3
NEXT_ACTION = 4

RIGHT_TURN = 450
TO_END = 5000
LIGHT_THRESHOLD = 125
PASSES_PER_LOAD = 3
PASSES_PER_QUADRANT = 4

passes = 0
loaded = False

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
        driver.startEncoderDrive(300, 300)
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
    global passes
    r.intake()
    if direction == RIGHT:
        turn_dir = CLOCKWISE
    else:
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
        driver.startEncoderDrive(300, 300)
        pass_state = 5
        return MAKE_PASS
    elif pass_state == 5:
        if driver.targetReached:
            pass_state = 6
        return MAKE_PASS
    elif pass_state == 6:
        driver.startEncoderTurn(RIGHT_TURN, direction)
        pass_state = 7
        return MAKE_PASS
    elif pass_state == 7:
        if driver.targetReached:
            pass_state = 8
        return MAKE_PASS
    elif pass_state == 8:
        if nav.driveToLine():
            passes += 1
            return NEXT_ACTION
        else: 
            return MAKE_PASS


unload_state = 0


def unload():
    ls = UNLOAD

    return ls


def stop():
    pass


action_state = 0


def nextAction():
    global action_state
    global passes
    global loaded
    ls = NEXT_ACTION
    quadrant = math.floor(passes/PASSES_PER_QUADRANT) % 4
    unload_needed = passes % PASSES_PER_LOAD == 0
    new_quadrant = passes % PASSES_PER_QUADRANT == 0
    if quadrant == 0 | quadrant == 2:
        loc_pass_direction = RIGHT
    else:
        loc_pass_direction = LEFT

    if unload_needed:
        ls = UNLOAD
    elif new_quadrant:
        if quadrant == 0:
            if action_state == 0:
                driver.startEncoderDrive(300, 300, -0.5)
                action_state = 8
            elif action_state == 8:
                if driver.targetReached:
                    action_state = 9
            elif action_state == 9:
                driver.startEncoderTurn(RIGHT_TURN, CLOCKWISE)
                action_state = 1
            elif action_state == 1:
                if driver.targetReached:
                    action_state = 2
            elif action_state == 2:
                if nav.squareUp(IN_FRONT):
                    action_state = 3
            elif action_state == 3:
                driver.startEncoderDrive(300, 300, -0.5)
                action_state = 4
            elif action_state == 4:
                if driver.targetReached:
                    action_state = 5
            elif action_state == 5:
                driver.startEncoderTurn(RIGHT_TURN, COUNTERCLOCKWISE)
                action_state = 6
            elif action_state == 6:
                if driver.targetReached:
                    action_state = 7
            elif action_state == 7:
                if nav.squareUp(IN_FRONT):
                    action_state = 10
            elif action_state == 10:
                driver.startEncoderTurn(RIGHT_TURN, COUNTERCLOCKWISE)
        elif quadrant == 1:
            if action_state == 0:
                driver.startEncoderTurn(RIGHT_TURN, COUNTERCLOCKWISE)
                action_state = 1
            elif action_state == 1:
                if driver.targetReached:
                    action_state = 2
            elif action_state == 2:
                if r.get_encoders()[0] > LIGHT_THRESHOLD:
                    nav.followLine(0.5, RIGHT)

    return [ls, loc_pass_direction]


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
        state = makePass(pass_direction)
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
        [state, pass_direction] = nextAction()


print('done')
driver.stop()
