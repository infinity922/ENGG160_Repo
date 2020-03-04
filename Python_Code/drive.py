import pyfirmata
import time



class Drive:

    def __init__(self, board: pyfirmata.Board):
        self.board = board
        self.lMotor = board.get_pin('d:10:p')
        self.rMotor = board.get_pin('d:9:p')
        self.lDir = board.get_pin('d:14:o')
        self.rDir = board.get_pin('d:15:o')

    def tankDriveA(self,left,right,aTime):
        # not finished yet, maybe don't use
        steps = 60*aTime

        for x in range(steps):
            iTime = time()
            self.tankDrive(left*x/steps,right*x/steps)
            rem = 1/60 - (time() - iTime)
            if rem > 0:
                time.sleep(rem)
        self.tankDrive(left,right)

    def tankDrive(self,left,right):
        lm = abs(left)
        rm = abs(right)
        if left < 0:
            ld = 0
        else:
            ld = 1
        if right < 0:
            rd = 1
        else:
            rd = 0
        self.lDir.write(ld)
        self.rDir.write(rd)
        self.lMotor.write(lm)
        self.rMotor.write(rm)

    def stop(self):
        self.lMotor.write(0)
        self.rMotor.write(0)
