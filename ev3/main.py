#!/usr/bin/env python3

'''
Main file for the ev3.
Goal: Prepare robot for execution & start algorithm

Other algorithms can be run on the brick by running the file directly.
'''

from logging import debug, prepare_console
import time

from devices.controller import buttons, sticks, Button, Stick, is_controller_connected


def main():
    prepare_console()

    class State:
        run = True

    def stop():
        State.run = False

    buttons.add(Button.START, stop)

    while (State.run):
        time.sleep(1)

    debug("Shutting down in 10 seconds")
    # allow reading of console output
    time.sleep(10)


if __name__ == '__main__':
    main()

'''
    for fn in evdev.list_devices():
        debug(fn)

    devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
    for device in devices:
        debug(device.name.encode('ascii', 'ignore').decode('ascii'))
'''