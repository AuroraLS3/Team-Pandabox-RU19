#!/usr/bin/env python3
from time import sleep
from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, MoveTank, MoveSteering
from ev3dev2.motor import SpeedDPS, SpeedRPM, SpeedRPS, SpeedDPM
# degrees per second, rotations per minute, rotations per second, degrees per minute
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor
from ev3dev2.led import Leds
from ev3dev2.display import Display
from ev3dev2.button import Button
from ev3dev2.sound import Sound
from move.custom_tank import CustomMoveTank
from debug import debug, prepare_console
from time import sleep

def runCalibrator():

    speed = 25
    counter_max = 5
    # todo: adjust scale
    proximityScale = 0.7

    button = Button()
    colorS = ColorSensor(INPUT_3)
    sound = Sound()

    moveTank = CustomMoveTank(OUTPUT_A, OUTPUT_D)
    infrared = InfraredSensor()

    def moveWithDistance(moveLengthCm, distance):
        movedLength = 0
        step = 10
        turn = 0.5

        while movedLength < moveLength:
            proximity = proximityScale * infrared.proximity

            debug("proximity cm " + str(proximity))

            if proximity < distance:
                moveTank.move_cm(step + turn, step - turn)
            else
                moveTank.move_cm(step - turn, step + turn)
            
            moveLength += step

    # 70cm forward
    # turn 90 degrees
    # keep 10cm distance from edge
    # drive forward 240cm
    # stop to wait for usb

    moveTank.move_cm(70)
    moveTank.turn(90)
    moveWithDistance(240, 10)
    time.sleep(3)
    moveWithDistance(40, 10)

        