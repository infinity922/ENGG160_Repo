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
        self.board = my_pyfirmata.Arduino('COM4')  # replace this address with the one from your Arduino IDE
        # For the pi: /dev/ttyACM0

    def set_left_motor(self, power):
        power = int(round(power*400))
        self.board.sp.write(bytearray([START_SYSEX, ZUMO, LEFT_MOTOR_POWER, power % 128, power >> 7, END_SYSEX]))

    def set_right_motor(self, power):
        power = int(round(power * 400))
        self.board.sp.write(bytearray([START_SYSEX, ZUMO, RIGHT_MOTOR_POWER, power % 128, power >> 7, END_SYSEX]))

    def get_right_encoder(self):
        self.board.sp.write(bytearray([START_SYSEX, ZUMO, ENCODER_REPORT_POSTITON, 1, END_SYSEX]))
        recived = False
        while recived is False:
            if self.board.bytes_available():
                self.board.iterate()
            enc_dat = self.board.get_new_encoder_positions()
            if enc_dat is not False:
                recived = True
                return enc_dat[1]

    def get_left_encoder(self):
        self.board.sp.write(bytearray([START_SYSEX, ZUMO, ENCODER_REPORT_POSTITON, 0, END_SYSEX]))

        recived = False
        while recived is False:
            if self.board.bytes_available():
                self.board.iterate()
            enc_dat = self.board.get_new_encoder_positions()
            if enc_dat is not False:
                recived = True
                return enc_dat[0]

    def get_encoders(self):
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
        self.board.sp.write(bytearray([START_SYSEX,ZUMO,ENCODER_RESET_POSITION, 1, END_SYSEX]))

        recived = False
        while recived is False:
            if self.board.bytes_available():
                self.board.iterate()
            enc_dat = self.board.get_new_encoder_positions()
            if enc_dat is not False:
                recived = True

    def get_lines(self):
        self.board.sp.write(bytearray([START_SYSEX,ZUMO,LINE_SENSORS,END_SYSEX]))

        recived = False
        while recived is False:
            if self.board.bytes_available():
                self.board.iterate()
            lines = self.board.get_new_lines()
            if lines is not False:
                recived = True
                return lines
