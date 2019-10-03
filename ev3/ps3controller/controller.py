#!/usr/bin/env python3

'''
PS3 controller connector & handler.

Example usage

    from ps3controller.controller import buttons, sticks, Buttons, Sticks

    def exampleFunction():
        # change state variable
        # don't do "expensive" stuff

    # exampleFunction will be called when X is pressed on the PS3 controller
    buttons.add(Button.X, exampleFunction)

    def exampleStick(value):
        # value represents how much the stick is pushed forward
        # change state variable for the stick
        # don't do "expensive" stuff

    sticks.add(Sticks.LEFT_X, exampleStick)
'''

# This is a linux-specific module.
# It is required by the Button class, but failure to import it may be
# safely ignored if one just needs to run API tests on Windows.
import evdev

import threading
import math

## Some helpers ##


def scale(val, src, dst):
    """
    Scale the given value from the scale of src to the scale of dst.
    val: float or int
    src: tuple
    dst: tuple
    example: print(scale(99, (0.0, 99.0), (-1.0, +1.0)))
    """
    return (float(val - src[0]) / (src[1] - src[0])) * (dst[1] - dst[0]) + dst[0]


def scale_stick(value):
    return scale(value, (0, 255), (-100, 100))


class ButtonListeners:
    def __init__(self):
        self.listeners = {
            0: []  # Listeners are higher order functions. ##
        }

    def add(self, button, function):
        button_listeners = self.listeners[button]
        if not button_listeners:
            button_listeners = []

        button_listeners.append(function)
        self.listeners[button] = button_listeners

    def call(self, button):
        button_listeners = self.listeners[button]
        if not button_listeners:
            return
        for listener in self.listeners[button]:
            listener()

class StickListeners:
    def __init__(self):
        self.listeners = {
            0: []  # Listeners are higher order functions.
        }

    def add(self, stick, function):
        stick_listeners = self.listeners[stick]
        if not stick_listeners:
            stick_listeners = []

        stick_listeners.append(function)
        self.listeners[stick] = stick_listeners

    def call(self, stick, value):
        stick_listeners = self.listeners[stick]
        if not stick_listeners:
            return
        for listener in self.listeners[stick]:
            listener(value)


class ControllerPollThread(threading.Thread):
    def __init__(self, button_listeners, stick_listeners):
        ## Initializing ##

        print("Finding ps3 controller...")
        devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
        for device in devices:
            if device.name == 'PLAYSTATION(R)3 Controller':
                ps3dev = device.fn

        self.gamepad = evdev.InputDevice(ps3dev)
        self.button_listeners = button_listeners
        self.stick_listeners = stick_listeners
        threading.Thread.__init__(self)

    def run(self):
        BUTTON_PRESS = 1
        STICK_MOVE = 3

        for event in self.gamepad.read_loop():  # this loops infinitely
            if event.type == BUTTON_PRESS and event.value == 1:
                self.button_listeners.call(event.code)
            elif event.type == STICK_MOVE:
                self.stick_listeners.call(event.code, scale_stick(event.value))
                # if event.type == 2 or event.type == 1 or event.type == 0:
                #     if event.value != 0:
                #         print("%s %s %s" % (event.type, event.code, event.value))


buttons = ButtonListeners()
sticks = StickListeners()


controller_thread = ControllerPollThread(buttons, sticks)
controller_thread.setDaemon(True)
controller_thread.start()


class Buttons:
    X = 304
    CIRCLE = 305
    TRIANGLE = 307
    SQUARE = 308
    L1 = 310
    R1 = 311
    SELECT = 314
    START = 315


class Sticks:
    LEFT_X = 0
    LEFT_Y = 1
    L2 = 2
    RIGHT_X = 3
    RIGHT_Y = 4
    R2 = 5