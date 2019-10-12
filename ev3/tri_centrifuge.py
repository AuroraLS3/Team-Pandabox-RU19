#!/usr/bin/env python3
from time import sleep
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, MoveTank, MoveSteering
from ev3dev2.motor import SpeedDPS, SpeedRPM, SpeedRPS, SpeedDPM
# degrees per second, rotations per minute, rotations per second, degrees per minute


class Centrifuge(MoveTank):
    times_fw = 0
    times_bw = 0
    speed = 90
    long_jump = 7
    short_jump = 4

    def move_fw(self):
        if(times_fw == 0):
            self.on_for_rotations(speed, speed, long_jump)
            times_fw += 1
        else:
            self.on_for_rotations(speed, speed, short_jump)

    def move_bw(self):
        if(times_bw == 1):
            self.on_for_rotations(-speed, -speed, long_jump)
        else:
            self.on_for_rotations(-speed, -speed, short_jump)
            times_bw += 1

