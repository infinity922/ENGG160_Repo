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
UNLOAD = 2  # Unused
STOP = 3
NEXT_ACTION = 4  # Unused
TEST = 5  # For testing only
CONTINUE = 6

RIGHT_TURN = 650
TO_END = 3000
LIGHT_THRESHOLD = 100  # Light sensors unused
PASSES_PER_LOAD = 127  # Not unloading, we don't have enough golf balls
PASSES_PER_QUADRANT = 4  # Not using quadrants because of light sensors
NUM_PASSES = 16

passes = 0
loaded = False

timeout = 300

r = Robot()  # initialize the robot
driver = Drive(r)  # initialize the driver
nav = Navigation(r, driver)  # initialize the nav
running = True
state = START
pos = 0
pass_direction = RIGHT

""" calibrating = True
calib_state = 0

while calibrating:
    r.calibrate_lines()
    driver.iterate()
    if calib_state == 0:
        driver.startEncoderDrive(1000, 1000, 0.3)
        calib_state = 2
    elif calib_state == 2:
        if driver.targetReached:
            calib_state = 3
    elif calib_state == 3:
        input('Press Enter to start')
        calibrating = False"""


startTime = time.time()
r.reset_encoders()

start_state = 0


def start():
    global start_state
    if start_state == 0:
        driver.startEncoderDrive(300, 300)
        start_state = 2
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
        driver.startEncoderTurn(RIGHT_TURN, turn_dir)
        pass_state = 7
        return MAKE_PASS
    elif pass_state == 7:
        print('here now')
        if driver.targetReached:
            pass_state = 8
        return MAKE_PASS
    elif pass_state == 8:
        driver.startEncoderDrive(TO_END, TO_END)
        pass_state = 9
        return MAKE_PASS
    elif pass_state == 9:
        if driver.targetReached:
            return CONTINUE
        else:
            passes = passes + 1
            return MAKE_PASS


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% UNUSED %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
unload_state = 0


def unload():
    ls = UNLOAD

    return ls
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


def stop():
    pass


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% UNUSED %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
action_state = 0


def nextAction():
    global action_state
    global passes
    global loaded
    ls = NEXT_ACTION
    quadrant = math.floor(passes/PASSES_PER_QUADRANT) % 4
    unload_needed = passes % PASSES_PER_LOAD == 0
    new_quadrant = passes % PASSES_PER_QUADRANT == 0
    if quadrant == 0 | quadrant == 1:
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
                driver.startEncoderDrive(300, 300)
                action_state = 11
            elif action_state == 11:
                if driver.targetReached:
                    action_state = 12
            elif action_state == 12:
                driver.startEncoderTurn(RIGHT_TURN, COUNTERCLOCKWISE)
                action_state = 13
            elif action_state == 13:
                if driver.targetReached:
                    action_state = 14
            elif action_state == 14:
                r.reset_encoders()
                nav.followLine(0.5, LEFT, LEFT)
                action_state = 15
            elif action_state == 15:
                if r.get_encoders()[0] >= 5000:
                    action_state = 16
                else:
                    nav.followLine(0.5, LEFT, LEFT)
            elif action_state == 16:
                driver.startEncoderTurn(RIGHT_TURN, CLOCKWISE)
                action_state = 17
            elif action_state == 17:
                if driver.targetReached:
                    action_state = 18
            elif action_state == 18:
                if nav.squareUp(BEHIND):
                    action_state = 19
            elif action_state == 19:
                driver.stop()
                action_state = 0
                ls = MAKE_PASS
        elif quadrant == 1:
            if action_state == 0:
                driver.startEncoderTurn(RIGHT_TURN, COUNTERCLOCKWISE)
                action_state = 1
            elif action_state == 1:
                if driver.targetReached:
                    action_state = 2
            elif action_state == 2:
                if r.get_encoders()[0] > LIGHT_THRESHOLD:
                    nav.followLine(0.5, RIGHT, RIGHT)
                else:
                    action_state = 3
            elif action_state == 3:
                driver.startEncoderDrive(300, 300)
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
                if nav.squareUp(BEHIND):
                    ls = MAKE_PASS
                    driver.stop()
                    action_state = 0
        elif quadrant == 2:
            if action_state == 0:
                if nav.squareUp(IN_FRONT):
                    action_state = 1
            elif action_state == 1:
                driver.startEncoderTurn(RIGHT_TURN, CLOCKWISE)
                action_state = 2
            elif action_state == 2:
                if driver.targetReached:
                    action_state = 3
            elif action_state == 3:
                nav.followLine(0.5, LEFT, LEFT)
                action_state = 4
            elif action_state == 4:
                if r.get_lines()[2] > LIGHT_THRESHOLD:
                    nav.followLine(0.5, LEFT, LEFT)
                else:
                    action_state = 6
            elif action_state == 6:
                driver.startEncoderDrive(300, 300, -0.5)
                action_state = 7
            elif action_state == 7:
                if driver.targetReached:
                    action_state = 8
            elif action_state == 8:
                driver.startEncoderTurn(RIGHT_TURN, COUNTERCLOCKWISE)
                action_state = 9
            elif action_state == 9:
                if driver.targetReached:
                    action_state = 13
            elif action_state == 12:
                driver.startEncoderDrive(300, 300, -0.5)
                action_state = 13
            elif action_state == 13:
                if driver.targetReached:
                    action_state = 10
            elif action_state == 10:
                if nav.squareUp(IN_FRONT):
                    action_state = 11
            elif action_state == 11:
                driver.stop()
                action_state = 0
                ls = MAKE_PASS

        elif quadrant == 3:
            if action_state == 0:
                driver.startEncoderTurn(RIGHT_TURN, COUNTERCLOCKWISE)
                action_state = 1
            elif action_state == 1:
                if driver.targetReached:
                    action_state = 2
            elif action_state == 2:
                if r.get_lines()[0] > LIGHT_THRESHOLD:
                    nav.followLine(0.5, RIGHT, RIGHT)
                else:
                    action_state = 3
                    driver.stop()
            elif action_state == 3:
                driver.startEncoderDrive(100, 100)
                action_state = 4
            elif action_state == 4:
                if driver.targetReached:
                    action_state = 5
            elif action_state == 5:
                r.reset_encoders()
                nav.followLine(0.5, RIGHT, RIGHT)
                action_state = 6
            elif action_state == 6:
                if r.get_encoders()[0] >= 5000:
                    action_state = 7
                    driver.stop()
                else:
                    nav.followLine(0.5, RIGHT, RIGHT)
            elif action_state == 7:
                driver.startEncoderTurn(RIGHT_TURN, COUNTERCLOCKWISE)
                action_state = 8
            elif action_state == 8:
                if nav.squareUp(BEHIND):
                    action_state = 9
            elif action_state == 9:
                driver.stop()
                action_state = 0
                ls = MAKE_PASS
    else:
        if loc_pass_direction == LEFT:
            turn_dir = COUNTERCLOCKWISE
            sensor = RIGHT
        else:
            turn_dir = COUNTERCLOCKWISE
            sensor = LEFT
        if action_state == 0:
            if nav.squareUp(IN_FRONT):
                action_state = 1
        elif action_state == 1:
            driver.startEncoderTurn(RIGHT_TURN, turn_dir)
            action_state = 2
        elif action_state == 2:
            if driver.targetReached:
                action_state = 3
        elif action_state == 3:
            r.reset_encoders()
            action_state = 4
        elif action_state == 4:
            if r.get_encoders()[0] < 300:
                nav.followLine(0.5, sensor, sensor)
            else:
                driver.stop()
                action_state = 5
        elif action_state == 5:
            driver.startEncoderTurn(RIGHT_TURN, turn_dir)
            action_state = 6
        elif action_state == 6:
            if nav.squareUp(BEHIND):
                action_state = 0
                driver.stop()
                ls = MAKE_PASS

    return [ls, loc_pass_direction]


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


while running:
    # r.calibrate_lines()
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
    elif state == CONTINUE:
        if passes <= NUM_PASSES:
            if passes % 2 == 0:
                pass_direction = RIGHT
            else:
                pass_direction = LEFT
            state = MAKE_PASS
        else:
            state = STOP
    elif state == UNLOAD:
        state = unload()
        if state != UNLOAD:
            unload_state = 0
    elif state == STOP:
        stop()
        running = False
    elif state == NEXT_ACTION:
        [state, pass_direction] = nextAction()
        if state != NEXT_ACTION:
            action_state = 0
    elif state == TEST:
        lin = r.get_lines()
        print(math.floor(lin[0]), math.floor(lin[2]), 'ahhha')
        """if nav.squareUp(IN_FRONT):
            print('Square')"""

print('done')
driver.stop()
