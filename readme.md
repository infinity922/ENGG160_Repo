ENGG160_Repo
---------------------------
#### PLEASE KEEP THE README UP TO DATE
#### Note:  
In order to use the program, a few things must be configured for the device to work
1. Pin assignments for the Zumo robot can be found at https://www.pololu.com/docs/0J63/3.10
1. The port in robot.py needs to be set to the port the robot is plugged into your computer in. This can be found in the Arduino IDE

#### Files in repo
##### `master.py`
This file controls the main flow of the program.
##### `drive.py`
This file contains a class which contains functions to move the robot in a streamlined fashion.
##### `robot.py`
This file contains a class that takes care of all the hardware for the robot, it is the interface with `my_pyfirmata` and
handles the bytestream to the robot, and receives the interpreted incoming bytes from the robot through `my_pyfirmata`
##### `__init__.py`
This file is supposed to do something just not sure what... imports maybe? configurations? if you know, do tell.

#### The my_pyfirmata package
this package has the partially custom made program to send and recive values and instructions from the robot on the python 
side.
