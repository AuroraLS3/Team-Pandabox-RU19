#!/usr/bin/env python3

'''
PS3 controller connector & handler.

Example usage

    from devices.controller import buttons, sticks, Buttons, Sticks, is_controller_connected

    if not is_controller_connected():
        return

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
import time

from debug import debug

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

class Button:
    ANY = 0
    X = 304
    CIRCLE = 305
    TRIANGLE = 307
    SQUARE = 308
    L1 = 310
    R1 = 311
    L2 = 312
    R2 = 313
    R2_STICK = 317
    R3_STICK = 318
    SELECT = 314
    START = 315
    UP = 544
    DOWN = 545
    LEFT = 546
    RIGHT = 547
    WAKE_CONTROLLER = 316


class Stick:
    ANY = 0
    LEFT_X = 0
    LEFT_Y = 1
    L2 = 2
    RIGHT_X = 3
    RIGHT_Y = 4
    R2 = 5



class ButtonListeners:
    def __init__(self):
        self.listeners = {
            Button.ANY: []  # Listeners are higher order functions. ##
        }

    def add(self, button, function):
        self.listeners.setdefault(button, []).append(function)

    def call(self, button):
        if button != Button.ANY:
            debug("Pressed button: %s" % button)
            self.call(Button.ANY)

        if not button in self.listeners:
            return
        for listener in self.listeners[button]:
            listener()


class StickListeners:
    def __init__(self):
        self.listeners = {
            Stick.ANY: []  # Listeners are higher order functions.
        }

    def add(self, stick, function):
        self.listeners.setdefault(stick, []).append(function)

    def call(self, stick, value):
        if stick != Stick.ANY:
            self.call(Stick.ANY, value)
        
        if not stick in self.listeners:
            return
        for listener in self.listeners[stick]:
            listener(value)


class ControllerPollThread(threading.Thread):
    def _find_controller(self):
        debug("Finding ps3 controller...")
        devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
        for device in devices:
            if device.name == 'Sony PLAYSTATION(R)3 Controller':
                ps3dev = device.fn
                self.gamepad = evdev.InputDevice(ps3dev)
        if not self.gamepad:
            time.sleep(1)

    def __init__(self, button_listeners, stick_listeners):
        ## Initializing ##
        self.find_attempts = 0

        self.gamepad = None
        self.button_listeners = button_listeners
        self.stick_listeners = stick_listeners
        threading.Thread.__init__(self)

    def run(self):
        while not self.gamepad and self.find_attempts < 5:
            self._find_controller()

        if not self.gamepad:
            return  # assuming that the thread execution ends here.

        debug("Found controller.")

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


def is_controller_connected():
    return bool(controller_thread.gamepad)
