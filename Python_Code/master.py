import pyfirmata
import drive
import time


bot = pyfirmata.Arduino('COM4');

driver = drive.Drive(bot)
# driver.tankDrive(0.5,-0.5)
# time.sleep(5)
# driver.stop()
# compass = bot.digital_ports[2]
# compass.enable_reporting()
