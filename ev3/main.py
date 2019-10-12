#!/usr/bin/env python3

'''
Main file for the ev3.
Goal: Prepare robot for execution & start algorithm

Other algorithms can be run on the brick by running the file directly.
'''

from debug import debug, prepare_console
import time
import evdev

from devices.controller import buttons, sticks, Button, Stick, is_controller_connected
from move.custom_tank import CustomMoveTank
from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_D

def main():
    prepare_console()

    class State:
        run = True

    tank = CustomMoveTank(OUTPUT_D, OUTPUT_A)

    def stop():
        State.run = False

    def turn(degrees):
        return lambda: tank.turn(degrees)

    def move(): 
        tank.move_cm(10)

    debug("Connected devices:")
    devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
    for device in devices:
        debug(device.name.encode('ascii', 'ignore').decode('ascii'))

    buttons.add(Button.START, stop)
    buttons.add(Button.RIGHT, turn(90))
    buttons.add(Button.LEFT, turn(-90))
    buttons.add(Button.UP, move)

    while (State.run):
        time.sleep(1)

    debug("Shutting down in 10 seconds")
    # allow reading of console output
    time.sleep(10)


if __name__ == '__main__':
    main()
