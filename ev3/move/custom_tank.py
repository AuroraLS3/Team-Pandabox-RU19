# Custom MoveTank extension for driving degrees and centimeters, calibrated
# for our robot

from ev3dev2.motor import MoveTank

defaultSpeed = 60


class CustomMoveTank(MoveTank):

    def turn(self, degrees, block=False):

        degrees = degrees * 5.75

        negative_turn = degrees < 0
        if negative_turn:
            degrees = -degrees

        speed = -defaultSpeed if negative_turn else defaultSpeed

        # rotations = (degrees - degrees % 360) / 360
        degrees = degrees  # - rotations * 360

        # Set all parameters
        # if rotations != 0:
        #     self.left_motor.on_for_rotations(speed, rotations, block=False)
        #     self.right_motor.on_for_rotations(-speed, rotations, block=True)
        if degrees != 0:
            self.left_motor.on_for_degrees(speed, degrees=degrees, block=False)
            self.right_motor.on_for_degrees(-speed,
                                            degrees=degrees, block=block)

    def centimetersToDegrees(self, centimeters):
        return centimeters * 70

    def getSpeed(self, degrees):
        negative_turn = degrees < 0
        if negative_turn:
            degrees = -degrees

        return -defaultSpeed if negative_turn else defaultSpeed

    def move_cm_lopsided(self, leftCm, rightCm, block=False):
        leftDegrees = self.centimetersToDegrees(leftCm)
        rightDegrees = self.centimetersToDegrees(rightCm)

        if leftDegrees != 0:
            speed = self.getSpeed(leftDegrees)
            self.left_motor.on_for_degrees(-speed,
                                           degrees=leftDegrees, block=False)
        if rightDegrees != 0:
            speed = self.getSpeed(rightDegrees)
            self.right_motor.on_for_degrees(-speed,
                                            degrees=rightDegrees, block=block)

    def move_cm(self, centimeters, block=False):
        degrees = self.centimetersToDegrees(centimeters)

        # rotations = (degrees - degrees % 360) / 360
        # degrees = degrees - rotations * 360
        speed = 60 if degrees > 0 else -60

        # Set all parameters
        # if rotations != 0:
        #     self.left_motor.on_for_rotations(speed, rotations, block=False)
        #     self.right_motor.on_for_rotations(speed, rotations, block=True)
        if degrees != 0:
            self.left_motor.on_for_degrees(-speed,
                                           degrees=degrees, block=False)
            self.right_motor.on_for_degrees(-speed,
                                            degrees=degrees, block=block)
