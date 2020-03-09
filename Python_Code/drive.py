import time

from .robot import Robot

ENCODER_DATA = 0x61

KP = 3
KD = 2
KI = .1


class Drive:
    # This class handles all the driving operations for the robot

    def __init__(self, robot: Robot):
        # Here we initialize the board and pin setup for the drive motors
        self.r = robot

        # initialize current power variables
        self.cleft = 0
        self.cright = 0

        # stop robot
        self.stop()

        # initialize encoderDrive vars
        self.targetLeft = None
        self.targetRight = None
        self.targetReached = True
        self.lastError = None
        self.totalError = None
        self.averagePower = None

    def tankDriveA(self, left, right, aTime):
        """ (UNFINISHED) This function will smoothly accelerate the robot from the current power to a new power in a
        given amount of time """
        steps = 60*aTime

        for x in range(steps):
            iTime = time()
            self.tankDrive(left*x/steps, right*x/steps)
            rem = 1/60 - (time() - iTime)
            if rem > 0:
                time.sleep(rem)
        self.tankDrive(left, right)

    def tankDrive(self, left, right):
        """ This function takes a left and right drive motor power between -1 (full reverse) and 1 (full forward) and
        sends them to the motors """

        self.r.set_left_motor(left)
        self.r.set_right_motor(right)

        # store current power values
        self.cleft = left
        self.cright = right

    def stop(self):
        # This function stops the robot's drive motors
        self.r.set_left_motor(0)
        self.r.set_right_motor(0)
        self.cleft = 0
        self.cright = 0

    def startEncoderDrive(self, leftCounts, rightCounts, averagePower = 0.5):
        self.targetLeft = leftCounts
        self.targetRight = rightCounts
        self.targetReached = False
        self.lastError = 0
        self.totalError = 0
        self.r.reset_encoders()
        self.averagePower = averagePower

    def encoderDrive(self):
        """ (UNFINISHED) This function will take a left and right distance in encoder counts and dynamically adjust motor
        power so both targets are reached simultaneously"""

        encs = self.r.get_encoders()
        error = encs[0]/self.targetLeft - encs[1]/self.targetRight
        self.totalError = self.totalError + error
        pterm = KP*error
        dterm = KD*(error - self.lastError)
        iterm = KI*self.totalError
        offset = pterm + dterm + iterm
        print(offset)
        print(error)
        self.tankDrive(self.averagePower - offset, self.averagePower + offset)
        print(encs)
        if (encs[0] >= self.targetLeft) | (encs[1] >= self.targetRight):
            print('target reached')
            self.targetReached = True
            self.stop()

    def iterate(self):

        if not self.targetReached:
            self.encoderDrive()







