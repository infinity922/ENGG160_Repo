import time

from .robot import Robot


# PID controller constants
KP = 3
KD = 2
KI = .1

CLOCKWISE = 0
COUNTERCLOCKWISE = 1


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
        self.targetAmount = None
        self.direction = None
        self.driving = False
        self.turning = False

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

    def startEncoderDrive(self, leftCounts, rightCounts, averagePower = 0.4):
        """This starts the encoderDrive running, it should only be run once, after, call driver.iterate() to do
        the actual calculations"""
        self.targetLeft = leftCounts
        self.targetRight = rightCounts
        self.targetReached = False
        self.lastError = 0
        self.totalError = 0
        self.r.reset_encoders()
        self.averagePower = averagePower
        self.driving = True

    def encoderDrive(self):
        """This function will take a left and right distance in encoder counts and dynamically adjust motor
        power so both targets are reached simultaneously and as smoothly as possible"""

        encs = self.r.get_encoders()
        error = encs[0]/self.targetLeft - encs[1]/self.targetRight
        self.totalError = self.totalError + error
        pterm = KP*error
        dterm = KD*(error - self.lastError)
        iterm = KI*self.totalError
        offset = pterm + dterm + iterm
        if self.averagePower >= 0:
            self.tankDrive(self.averagePower - offset, self.averagePower + offset)
        else:
            self.tankDrive(self.averagePower + offset, self.averagePower - offset)
        if (encs[0] >= self.targetLeft) | (encs[1] >= self.targetRight):
            print('target reached')
            self.targetReached = True
            self.driving = False
            self.stop()
            time.sleep(0.2)
        self.lastError = error

    def startEncoderTurn(self, amount, direction, averagePower = 0.3):
        self.targetAmount = amount
        self.targetReached = False
        self.lastError = 0
        self.totalError = 0
        self.r.reset_encoders()
        self.averagePower = averagePower
        self.direction = direction
        self.turning = True

    def encoderTurn(self):
        encs = self.r.get_encoders()
        error = encs[0] / self.targetAmount - encs[1] / self.targetAmount
        self.totalError = self.totalError + error
        pterm = 1 * error
        dterm = 0 * (error - self.lastError)
        iterm = 0 * self.totalError
        offset = pterm + dterm + iterm
        if self.direction == CLOCKWISE:
            self.tankDrive(self.averagePower - offset, -(self.averagePower + offset))
        elif self.direction == COUNTERCLOCKWISE:
            self.tankDrive(-(self.averagePower - offset), self.averagePower + offset)
        self.lastError = error
        if (encs[0] >= self.targetAmount) | (encs[1] >= self.targetAmount):
            print('target reached')
            self.targetReached = True
            self.turning = False
            self.stop()
            time.sleep(0.2)

    def iterate(self):
        """This method should be called in the main loop, it makes sure that all the iterating parts of this class are
        kept up to date"""
        if not self.targetReached:
            if self.driving:
                self.encoderDrive()
            if self.turning:
                self.encoderTurn()

