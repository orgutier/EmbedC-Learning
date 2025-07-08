-- INA219 feedback current sensors setup:

         \  A1 |
        A0     |  GND  VCC  SDA  SCL
        -------+----------------------------------
        GND    |  S0   S1
        VCC    |  S2   S3
        SDA    |
        SCL    |  S4   S5

-- PWM pinout definition, safe zone defined in rtos_arm_quadrature_IX.c

    SERVO1 28   // Slice 1, Channel A // base(0) -> arm(5); 1
    SERVO2 27   // Slice 1, Channel B // base(0) -> arm(5); 5
    SERVO3 26   // Slice 2, Channel A // base(0) -> arm(5); 0
    SERVO4 22   // Slice 2, Channel B // base(0) -> arm(5); 2
    SERVO5 21   // Slice 3, Channel A // base(0) -> arm(5); 4
    SERVO6 20   // Slice 3, Channel B // base(0) -> arm(5); 3

-- Voltage shifter for pwm outputs

    74HCT245 -> DIP package

-- Flash, test and debug

    Raspberry pi IP {Generic}.100
    SSH tunnel to port 3333
    Debug probe configuration defined in root folder readme.md

-- Power requirements

    5v to 6v 5A -> Servomotors (6)
    5v to 6v 3A -> DC motors 
    Fixed 5v (1A) -> pi pico 2W (main controller) & pi zero W (debug server)
    
