ENGG160_Repo
---------------------------
#### PLEASE KEEP THE README UP TO DATE
#### Note:  
In order to use the program, a few things must be configured for the device to work
1. Pin assignments for the Zumo robot can be found at https://www.pololu.com/docs/0J63/3.10
1. The port in robot.py needs to be set to the port the robot is plugged into your computer in. This can be found in the Arduino IDE
2. In the boards.py file in pyfirmata, replace the `'arduino'` section with   
```
'arduino': {
        'digital': tuple(x for x in range(30)),  
        'analog': tuple(x for x in range(12)),
        'pwm': (3, 5, 6, 9, 10, 11),
        'use_ports': True,
        'disabled': (0, 1)  # Rx, Tx, Crystal
    }
```

#### Files in repo
##### `master.py`
This file controls the main flow of the program.
##### `drive.py`
This file contains a class which contains functions to move the robot in a streamlined fashion.
##### `compassTest.py`
This file has preliminary testing for using the compass to turn the robot accurately
##### `__init__.py`
This file is supposed to do something just not sure what... imports maybe? configurations? if you know, do tell.
