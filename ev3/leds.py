#!/usr/bin/env python3

'''
Wrapper for ev3dev2 Leds.

Example usage:

    from leds import leds, Color, Group

    leds.set_color(Group.LEFT, Color.GREEN)
    time.sleep(5)
    leds.all_off()
'''

from ev3dev2.led import Leds

leds = Leds()
leds.all_off()


class Color:
    RED = "RED"
    GREEN = "GREEN"
    YELLOW = "YELLOW"
    ORANGE = "ORANGE"
    AMBER = "AMBER"
    BLACK = "BLACK"


class Group:
    RIGHT = "RIGHT"
    LEFT = "LEFT"
