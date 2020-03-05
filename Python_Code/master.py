import pyfirmata
import drive
import time

# Look at the readme, and keep it up to date when you change the code
bot = pyfirmata.Arduino('COM4')  # replace this address with the one from your Arduino IDE

driver = drive.Drive(bot)  # initialize the drive
driver.encoderRead()
# Here would be a state machine once a few more pieces are in place
# driver.tankDrive(0.5,-0.5)
# time.sleep(5)
# driver.stop()
# compass = bot.digital_ports[2]
# compass.enable_reporting()
