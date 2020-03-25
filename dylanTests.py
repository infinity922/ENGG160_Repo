from Python_Code import drive
from Python_Code import robot
from .robot import Robot
from .drive import Drive

IN_FRONT, LEFT = 0, 0
BEHIND, MIDDLE = 1, 1
RIGHT = 2

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

    def followLine(self, speed, sensor):
        """
        This method should follow a dark line
        speed is the average speed to drive while following the line. sensor will either be the constant LEFT, MIDDLE
        or RIGHT telling which line sensor to use.
        """
        self.r.get_lines()
        while lines == [0, 1, 0]:
            self.driver.tankDrive(speed, speed)
        if lines == [1, 0, 0]:
            self.r.get_lines()
            while lines != [0, 1, 0]:
                self.driver.tankDrive(-0.1, 0.1)
        if lines == [0, 0, 1]:
            self.r.get_lines()
            while lines !=[0, 1, 0]:
                self.driver.tankDrive(0.1, -0.1)



    def squareUp(self, direction):
        """
        This function squares up on a line either in front or behind the robot, direction will either be the constant
        IN_FRONT or BEHIND

        I'd like this to return True when it is finished, for an idea on how you could do this, see the
        startEncoderDrive, encoderDrive and iterate in drive
        """
        self.driveToLine(0.5)
        self.r.get_lines()
        if lines == [1, 0, 0]:
            while lines[2] == 0:
                self.driver.tankDrive(0.1, 0.1)
            while lines != [1, 1, 1]:
                self.driver.tankDrive(-0.1, 0.1)
        if lines == [0, 0, 1]:
            while lines[2] == 0:
                self.driver.tankDrive(0.1, 0.1)
            while lines != [1, 1, 1]:
                self.driver.tankDrive(0.1, -0.1)
        if lines = [1, 1, 1]:
            return True

    def driveToLine(self, speed):
        """
        this function drives straight forward at speed (passed as an argument) until it sees a line, I'd like it to use
        the same kind of algorithm as encoderDrive to keep the robot going as straight as possible, I can help with
         this if needed.

        As with squareUp, I'd like it to return True when it's finished
        speed = 0.5?
        """
        self.r.get_lines()
        while lines == [0, 0, 0]:
            self.driver.tankDrive(speed, speed)
        if lines[2] = 1:
            return True

    def iterate(self):
        """This code will run every time the main program loops, see drive to see how this might be used"""
        self.r.get_lines()
        if lines == [0, 0, 0]:
            self.driveToLine(0.5)
