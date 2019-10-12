#!/usr/bin/env python3

'''
Main file for the ev3.
Goal: Prepare robot for execution & start algorithm

Other algorithms can be run on the brick by running the file directly.
'''

from debug import debug, prepare_console
import time
import threading
import ctypes

import evdev

from devices.controller import buttons, sticks, Button, Stick, is_controller_connected
from move.custom_tank import CustomMoveTank
from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_D
from tri_centrifuge import Centrifuge

def main():
    prepare_console()

    class Program:
        CONTROLLER = "controller"
        WHITE_LINE = "white_line"

    class State:
        program = Program.CONTROLLER
        run = True
        picNo = 1
        speedL = 0
        speedR = 0

    tank = CustomMoveTank(OUTPUT_D, OUTPUT_A)
    centrifuge = Centrifuge(OUTPUT_D, OUTPUT_A)

    def stop():
        State.run = False

    def turn(degrees):
        return lambda: tank.turn(degrees)

    # def move_fw():
    #     tank.move_cm(10)

    # def move_bw():
    #     tank.move_cm(-10)

    def left(value):
        State.speedL = value

    def right(value):
        State.speedR = value

    debug("Connected devices:")
    devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
    for device in devices:
        debug(device.name.encode('ascii', 'ignore').decode('ascii'))

    sticks.add(Stick.LEFT_Y, left)
    sticks.add(Stick.RIGHT_Y, right)

    class MainThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)

        def run(self):
            while (State.run):
                try:
                    self.runAlgorithm()
                except:
                    continue

            debug("Shutting down in 10 seconds")
            # allow reading of console output
            time.sleep(10)

        def runAlgorithm(self):
            if (State.program == Program.CONTROLLER):
                if State.speedL != 0 or State.speedR != 0:
                    tank.on(State.speedR, State.speedL)
                else:
                    tank.off()
            elif State.program == Program.WHITE_LINE:
                runWhiteLine()

        def get_id(self):
            # returns id of the respective thread
            if hasattr(self, '_thread_id'):
                return super._thread_id
            for id, thread in threading._active.items():
                if thread is self:
                    return id

        def raise_exception(self):
            thread_id = self.get_id()
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
                                                             ctypes.py_object(SystemExit))
            if res > 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
                print('Exception raise failure')

    main_thread = MainThread()
    main_thread.setDaemon(True)
    main_thread.start()

    buttons.add(Button.START, stop)
    buttons.add(Button.RIGHT, turn(90))
    buttons.add(Button.LEFT, turn(-90))
    buttons.add(Button.UP, centrifuge.move_fw)
    buttons.add(Button.DOWN, centrifuge.move_bw)

    def runWhiteLine():
        State.program = not Program.WHITE_LINE
        main_thread.raise_exception()

    buttons.add(Button.SELECT, runWhiteLine)


if __name__ == '__main__':
    main()
