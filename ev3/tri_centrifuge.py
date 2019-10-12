#!/usr/bin/env python3
from time import sleep
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, MoveTank, MoveSteering
from ev3dev2.motor import SpeedDPS, SpeedRPM, SpeedRPS, SpeedDPM
# degrees per second, rotations per minute, rotations per second, degrees per minute


class Centrifuge(MoveTank):
    def move_fw(self):
        self.on_for_rotation()
        a = 1

    def move_bw(self):
        tank.move_cm(-10)