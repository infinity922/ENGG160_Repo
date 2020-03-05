import pyfirmata
import time


class Drive:
    # This class handles all the driving operations for the robot

    def __init__(self, board: pyfirmata.Board):
        # Here we initialize the board and pin setup for the drive motors
        self.board = board
        self.lMotor = board.get_pin('d:10:p')
        self.rMotor = board.get_pin('d:9:p')
        self.lDir = board.get_pin('d:14:o')
        self.rDir = board.get_pin('d:15:o')
        # Need to add encoder pins
        self.lEnc = board.get_pin('a:5:i')
        self.rEnc = board.get_pin('d:7:i')

        # initialize current power variables
        self.cleft = 0
        self.cright = 0

        # stop robot
        self.stop()

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

        # Take the absolute value of the power to find what to send to the motor power pins
        lm = abs(left)
        rm = abs(right)

        # set appropriate values to the motor direction pins
        if left < 0:
            ld = 0
        else:
            ld = 1
        if right < 0:
            rd = 1
        else:
            rd = 0

        # write the values to the physical pins
        self.lDir.write(ld)
        self.rDir.write(rd)
        self.lMotor.write(lm)
        self.rMotor.write(rm)

        # store current power values
        self.cleft = left
        self.cright = right

    def stop(self):
        # This function stops the robot's drive motors
        self.lMotor.write(0)
        self.rMotor.write(0)
        self.cleft = 0
        self.cright = 0

    def encoderDrive(self, leftCounts, rightCounts, averagePower = 0.5):
        """ (UNFINISHED) This function will take a left and right distance in encoder counts and dynamically adjust motor
        power so both targets are reached simultaneously"""

        lcounter = 0
        rcounter = 0

    def encoderRead(self):
        counts = 0
        last = 0
        while True:
            cur = self.lEnc.read()
            if cur != last:
                counts += 1
                last = cur
            # print(counts)
            print(cur)

