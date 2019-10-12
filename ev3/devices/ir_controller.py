import evdev
from ev3dev2.sensor.lego import InfraredSensor
from ev3dev2.sensor import INPUT_1
from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, MoveTank, MoveSteering

from debug import debug

def steer(motor, direction):
    def on_press(state):
        if state:
            motor.run_forever(speed_sp=600*direction)
        else:
            motor.stop(stop_action='brake')
    return on_press


def runIrController():
    rc = InfraredSensor(INPUT_1)
    lA = LargeMotor(OUTPUT_A)
    lD = LargeMotor(OUTPUT_D)

    rc.on_chanel1_top_left = steer(lA, 1)
    rc.on_chanel1_top_right = steer(lD, 1)
    rc.on_chanel1_bottom_left = steer(lA, -1)
    rc.on_chanel1_bottom_left = steer(lD, -1)

    while True:
        rc.process()
