import my_pyfirmata

START_SYSEX = 0xF0
END_SYSEX = 0xF7
LEFT_MOTOR_POWER = 0x00
RIGHT_MOTOR_POWER = 0x01
ENCODER_RESET_POSITION = 0x03
ENCODER_REPORT_POSTITON = 0x04
LINE_SENSORS = 0x05
ZUMO = 0x61


class Robot:

    def __init__(self):

        """This method is automatically called when robot is created, there shouldn't be any need
         to run it after that"""
        self.board = my_pyfirmata.Arduino('COM5')
        # replace this address with the one from your Arduino IDE
        # For the pi: /dev/ttyACM0

    def set_left_motor(self, power):
        """This method sets a power to the left motor in range (-1, 1)"""
        if power > 1:
            power = 1
        elif power < -1:
            power = -1
        if power >= 0:
            dir = 1
        else:
            dir = 0
        power = int(round(abs(power*400)))

        self.board.sp.write(bytearray([START_SYSEX, ZUMO, LEFT_MOTOR_POWER, power % 128, (power >> 7), dir, END_SYSEX]))

    def set_right_motor(self, power):
        """This method sets a power to the right motor in range (-1, 1)"""
        if power > 1:
            power = 1
        elif power < -1:
            power = -1

        if power >=0:
            dir = 1
        else:
            dir = 0
        power = int(round(abs(power*400)))
        self.board.sp.write(bytearray([START_SYSEX, ZUMO, RIGHT_MOTOR_POWER, power % 128, power >> 7, dir, END_SYSEX]))

    def get_right_encoder(self):
        """This class gets the number of ticks from the right encoder since the last encoder reset as an integer"""
        self.board.sp.write(bytearray([START_SYSEX, ZUMO, ENCODER_REPORT_POSTITON, 1, END_SYSEX]))
        received = False
        while received is False:
            if self.board.bytes_available():
                self.board.iterate()
            enc_dat = self.board.get_new_encoder_positions()
            if enc_dat is not False:
                received = True
                return enc_dat[1]

    def get_left_encoder(self):
        """This method gets the number of ticks from the left encoder since the last encoder reset as an integer"""
        self.board.sp.write(bytearray([START_SYSEX, ZUMO, ENCODER_REPORT_POSTITON, 0, END_SYSEX]))

        received = False
        while received is False:
            if self.board.bytes_available():
                self.board.iterate()
            enc_dat = self.board.get_new_encoder_positions()
            if enc_dat is not False:
                received = True
                return enc_dat[0]

    def get_encoders(self):
        """this method gets the number of ticks from both encoders in a 1x2 array of integers"""
        self.board.sp.write(bytearray([START_SYSEX, ZUMO, ENCODER_REPORT_POSTITON, 0, END_SYSEX]))

        recived = False
        while recived is False:
            if self.board.bytes_available():
                self.board.iterate()
            enc_dat = self.board.get_new_encoder_positions()
            if enc_dat is not False:
                recived = True
                return enc_dat

    def reset_encoders(self):
        """This method resets the encoders"""
        self.board.sp.write(bytearray([START_SYSEX,ZUMO,ENCODER_RESET_POSITION, 1, END_SYSEX]))

    def get_lines(self):
        """This method gets the values from the line sensors as a 1x3 array"""
        self.board.sp.write(bytearray([START_SYSEX,ZUMO,LINE_SENSORS,END_SYSEX]))

        recived = False
        while recived is False:
            if self.board.bytes_available():
                self.board.iterate()
            lines = self.board.get_new_lines()
            if lines is not False:
                recived = True
                return lines

    def intake(self):
        """
        here we set the foam wheels spinning inwards
        """

    def outake(self):
        """
        here we set the foam wheels spinning outwards
        """