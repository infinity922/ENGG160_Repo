from .robot import Robot
from .drive import Drive

IN_FRONT, LEFT = 0
BEHIND, MIDDLE = 1
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

    def squareUp(self, direction):
        """
        This function squares up on a line either in front or behind the robot, direction will either be the constant
        IN_FRONT or BEHIND

        I'd like this to return True when it is finished, for an idea on how you could do this, see the
        startEncoderDrive, encoderDrive and iterate in drive
        """

    def iterate(self):
        """This code will run every time the main program loops, see drive to see how this might be used"""