#!/usr/bin/env python3

'''
Main file for the ev3.
Goal: Prepare robot for execution & start algorithm

Other algorithms can be run on the brick by running the file directly.
'''

from debug import debug, prepare_console
import time
import threading
from threading import Event
import ctypes

import evdev

from devices.controller import buttons, sticks, Button, Stick
from move.custom_tank import CustomMoveTank
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, MediumMotor
# from tri_centrifuge import Centrifuge
# from calibrator import runCalibrator

from move.white_line import runWhiteLine
from devices.ir_controller import runIrController


def main():
    prepare_console()

    class Program:
        CONTROLLER = "controller"
        WHITE_LINE = "white_line"
        CALIBRATOR = "calibrator"
        CENTRIFUGE = "centrifuge"
        IRCONTROLLER = "ircontroller"

    class State:
        program = Program.CONTROLLER
        run = True
        picNo = 1
        speedL = 0
        speedR = 0
        armOpen = False

    tank = CustomMoveTank(OUTPUT_D, OUTPUT_A)
    arm = MediumMotor(OUTPUT_B)
    claw = MediumMotor(OUTPUT_C)
    # centrifuge = Centrifuge(OUTPUT_D, OUTPUT_A)

    def stop():
        State.run = False

    def turn(degrees):
        return lambda: tank.turn(degrees)

    # def move_fw():
    #     State.program = Program.CENTRIFUGE
    #     centrifuge.move_fw()
    #     State.program = Program.CONTROLLER

    # def move_bw():
    #     State.program = Program.CENTRIFUGE
    #     centrifuge.move_bw()
    #     State.program = Program.CONTROLLER

    def left(value):
        if abs(value) < 5:
            value = 0
        State.speedL = value

    def right(value):
        if abs(value) < 5:
            value = 0
        State.speedR = value

    def abort():
        debug("abort raising exception in main thread")
        main_thread.raise_exception()

    def openArm():
        if State.armOpen:
            return
        State.armOpen = True
        while not arm.is_overloaded:
            arm.on(-30, block=True)
        arm.off()

    def closeArm():
        if not State.armOpen:
            return
        State.armOpen = False
        while not arm.is_overloaded:
            arm.on(30, block=True)
        arm.off()

    def downClaw():
        claw.on_for_degrees(10, 30, block=True)
        claw.off()

    def upClaw():
        claw.on_for_degrees(-10, 30, block=True)
        claw.off()

    debug("Connected devices:")
    devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
    for device in devices:
        debug(device.name.encode('ascii', 'ignore').decode('ascii'))

    sticks.add(Stick.LEFT_Y, left)
    sticks.add(Stick.RIGHT_Y, right)
    buttons.add(Button.L2, closeArm)
    buttons.add(Button.R2, openArm)
    buttons.add(Button.R1, downClaw)
    buttons.add(Button.L1, upClaw)

    ready = Event()

    class MainThread(threading.Thread):
        def __init__(self, event=None):
            self.event = event
            threading.Thread.__init__(self)

        def run(self):
            while (State.run):
                try:
                    self.runAlgorithm()
                except:
                    debug("exception received. Current program aborted.")
                    continue
            self.event.set()

        def runAlgorithm(self):
            if (State.program == Program.CONTROLLER):
                lspeed = State.speedL
                rspeed = State.speedR
                if lspeed != 0 or rspeed != 0:
                    tank.on(lspeed, rspeed)
                else:
                    tank.off()
            elif State.program == Program.WHITE_LINE:
                runWhiteLine()
            elif State.program == Program.CALIBRATOR:
                # runCalibrator()
                State.program = Program.CONTROLLER
            elif State.program == Program.IRCONTROLLER:
                runIrController()

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

    main_thread = MainThread(ready)
    main_thread.setDaemon(True)
    main_thread.start()

    def setWhiteline():
        State.program = Program.WHITE_LINE

    def setController():
        State.program = Program.CONTROLLER

    def setCalibrator():
        State.program = Program.CALIBRATOR

    def setIRController():
        State.program = Program.IRCONTROLLER

    buttons.add(Button.CIRCLE, setWhiteline)
    buttons.add(Button.X, setController)
    buttons.add(Button.TRIANGLE, setIRController)

    # Quit current program
    buttons.add(Button.SELECT, abort)

    ready.wait()


if __name__ == '__main__':
    main()
