import my_pyfirmata

START_SYSEX = 0xF0
END_SYSEX = 0xF7
LEFT_MOTOR_POWER = 0x00
RIGHT_MOTOR_POWER = 0x01
ENCODER_RESET_POSITION = 0x03
ENCODER_REPORT_POSTITON = 0x04
ZUMO = 0x61
class Robot:

    def __init__(self):
        self.board = my_pyfirmata.Arduino('COM4')  # replace this address with the one from your Arduino IDE

    def set_left_motor(self, power):
        power = int(round(power*400))
        self.board.sp.write(bytearray([START_SYSEX, ZUMO, LEFT_MOTOR_POWER, power % 128, power >> 7, END_SYSEX]))

    def set_right_motor(self, power):
        power = int(round(power * 400))
        self.board.sp.write(bytearray([START_SYSEX, ZUMO, RIGHT_MOTOR_POWER, power % 128, power >> 7, END_SYSEX]))


