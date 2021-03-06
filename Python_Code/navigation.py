from .robot import Robot
from .drive import Drive

IN_FRONT, LEFT = 0, 0
BEHIND, MIDDLE = 1, 1
RIGHT = 2

THRESHOLD = 60
TOLERANCE = 20

#  PID Controller Constants:            THESE WILL HAVE TO BE ADJUSTED
KP = 0.001
KI = 0
KD = 0.001

class Navigation:

    """
    Keep in mind for all of these functions that this code will be run over and over again. Since the robot may need
    to do other things while this is running avoid using loops, these have the potential to freeze the program.

    Look in the Robot class for the functions needed to access the line sensor data and in drivers for everything
    to make the robot move, if you need any additional functionality or have questions about what these functions need
    to do, feel free to contact me
    """

    def __init__(self, r: Robot, driver: Drive):
        self.r = r
        self.driver = driver
        self.finishedSquare = True
        self.foundBlack = False
        self.last_left = 0
        self.last_right = 0

        self.errorLast = 0
        self.integral = 0

    def followLine(self, speed, sensor, side):
        """
        This method should follow a dark line
        speed is the average speed to drive while following the line. sensor will either be the constant LEFT, MIDDLE
        or RIGHT telling which line sensor to use. side will either be the constant RIGHT or LEFT and will tell which
        side of the line the sensor will be on.
        """
        target = 1  # this will have to be changed to the light value that the robot picks up

        lines = self.r.get_lines()
        error = target - lines[sensor]
        self.integral = self.integral + error
        pterm = KP*error
        iterm = KI*self.integral
        derivative = error - self.errorLast
        dterm = KD*derivative
        offset = pterm + iterm + dterm
        if side == RIGHT:
            offset = -offset
        self.driver.tankDrive(speed - offset, speed + offset)
        self.errorLast = error






    def squareUp(self, direction):
        """
        This function squares up on a line either in front or behind the robot, direction will either be the constant
        IN_FRONT or BEHIND

        I'd like this to return True when it is finished, for an idea on how you could do this, see the
        startEncoderDrive, encoderDrive and iterate in drive
        """

        lp = 0
        rp = 0
        if self.finishedSquare:
            self.foundBlack = False
            self.finishedSquare = False

        lines = self.r.get_lines()
        if direction == IN_FRONT:
            if self.foundBlack:

                left_error = lines[0] - TOLERANCE
                der_term = self.last_left - left_error
                self.last_left = left_error
                pterm = 0.001
                lp = 0.001*left_error + 0.003*der_term

                right_error = lines[0] - TOLERANCE
                der_term = self.last_right - right_error
                self.last_right = right_error
                rp = 0.001 * right_error + 0.003 * der_term

                """if lines[0] < THRESHOLD - TOLERANCE:
                    lp = lp - 0.3
                elif lines[0] > THRESHOLD + TOLERANCE:
                    lp = lp + 0.3
                if lines[2] < THRESHOLD - TOLERANCE:
                    rp = rp - 0.3
                elif lines[2]> THRESHOLD + TOLERANCE:
                    rp = rp + 0.3"""
                self.driver.tankDrive(lp,rp)

            elif not self.foundBlack:
                self.driver.tankDrive(.3,.3)
                if (lines[0] < THRESHOLD) | (lines[2] < THRESHOLD):
                    self.foundBlack = True
            if (lines[0] < (THRESHOLD + TOLERANCE)) & (lines[0] > (THRESHOLD - TOLERANCE)) & (lines[2] < (THRESHOLD + TOLERANCE)) & (lines[2] > (THRESHOLD - TOLERANCE)):
                self.finishedSquare = True
                self.driver.stop()
                return True
            else:
                return False
        elif direction == BEHIND:
            if self.foundBlack:
                if lines[0] < THRESHOLD:
                    lp = lp - 0.3
                else:
                    lp = lp + 0.3
                if lines[2] < THRESHOLD:
                    rp = rp - 0.3
                else:
                    rp = rp + 0.3
                self.driver.tankDrive(-lp, -rp)

            elif not self.foundBlack:
                self.driver.tankDrive(-0.3, -0.3)
                if (lines[0] < THRESHOLD) | (lines[2] < THRESHOLD):
                    self.foundBlack = True
            if (lines[0] < (THRESHOLD + TOLERANCE)) & (lines[0] > (THRESHOLD - TOLERANCE)) & (lines[2] < (THRESHOLD + TOLERANCE)) & (lines[2] > (THRESHOLD - TOLERANCE)):
                self.finishedSquare = True
                self.driver.stop()
                return True
            else:
                return False

    def driveToLine(self, speed = 0.5):
        """
        this function drives straight forward at speed (passed as an argument) until it sees a line, I'd like it to use
        the same kind of algorithm as encoderDrive to keep the robot going as straight as possible, I can help with
         this if needed.

        As with squareUp, I'd like it to return True when it's finished
        """
        if not self.foundBlack:
            lines = self.r.get_lines()
            self.driver.tankDrive(0.4, 0.4)
        if (lines[1] < THRESHOLD) | (lines[0] < THRESHOLD) | (lines[2] < THRESHOLD):
            self.foundBlack = True
            self.driver.stop()
            return True
        else:
            return False

    def iterate(self):
        """This code will run every time the main program loops, see drive to see how this might be used"""
