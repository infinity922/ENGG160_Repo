import pyfirmata
import drive
import time

# Look at the really pretty readme, and keep it up to date when you change it
bot = pyfirmata.Arduino('COM4');

driver = drive.Drive(bot)
# driver.tankDrive(0.5,-0.5)
# time.sleep(5)
# driver.stop()
# compass = bot.digital_ports[2]
# compass.enable_reporting()
