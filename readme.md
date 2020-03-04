ENGG160_Repo
---------------------------
Note:  
In order to use the program, a few things must be configured for the device to work
1. The port in master.py needs to be set to the port the robot is plugged into your computer in. This can be found in the Arduino IDE
2. the boards.py file in pyfirmata, replace the `'arduino'` section with   
```
'arduino': {
        'digital': tuple(x for x in range(30)),  
        'analog': tuple(x for x in range(12)),
        'pwm': (3, 5, 6, 9, 10, 11),
        'use_ports': True,
        'disabled': (0, 1)  # Rx, Tx, Crystal
    }
```
