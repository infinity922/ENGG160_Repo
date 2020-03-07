import pyfirmata
ENCODER_ATTACH = 0x00
ENCODER_REPORT_POSITION = 0x01
ENCODER_RESET_POSITION = 0x03
ENCODER_DATA = 0x61
class Robot:

    def __init__(self):
        self.board = pyfirmata.Arduino('COM4')  # replace this address with the one from your Arduino IDE
        self.lMotor = self.board.get_pin('d:10:p')
        self.rMotor = self.board.get_pin('d:9:p')
        self.lDir = self.board.get_pin('d:14:o')
        self.rDir = self.board.get_pin('d:15:o')
        # Need to add encoder pins
        self.lEnc = self.board.get_pin('d:7:e')
        self.rEnc = self.board.get_pin('d:8:e')
        self.board.send_sysex(ENCODER_DATA, bytearray([ENCODER_ATTACH, 1, 7, 23]))

    def get_encoder_report(self):
        self.board.send_sysex(ENCODER_DATA, bytearray([ENCODER_REPORT_POSITION, 1]))
        print('here')

