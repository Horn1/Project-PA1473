#!/usr/bin/env pybricks-micropython

#import modules
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Stop, Direction
from pybricks.tools import wait

#define motors and sensors
ev3 = EV3Brick()

grab = Motor(Port.A) #Gripp claw
arm = Motor(Port.B, Direction.COUNTERCLOCKWISE, [8, 40])#elbow motor
rotate = Motor(Port.C, Direction.COUNTERCLOCKWISE, [12, 36])#rotation motor
arm.control.limits(speed=60, acceleration=120)#Limits in extention of the arm
rotate.control.limits(speed=60, acceleration=120)#rotation limits
base_switch = TouchSensor(Port.S1) #base tutch sensor
arm_sensor = ColorSensor(Port.S3) #collor sensor

#reset the arm
arm.run_time(-30, 1000)
arm.run(15)
while arm_sensor.reflection() < 32:
    wait(10)
arm.reset_angle(0)
arm.hold()

#reset the base of the arm
rotate.run(-60)
while not base_switch.pressed():
    wait(10)
rotate.reset_angle(0)
rotate.hold()

#reset the claw
grab.run_until_stalled(200, then=Stop.COAST, duty_limit=50)
grab.reset_angle(0)
grab.run_target(200, -90)


def robot_pick(position):
    #pick upp the brick

    # move to pickup position
    rotate.run_target(60, position)
    # Lower the arm
    arm.run_target(60, -40)
    # grab the block
    grab.run_until_stalled(200, then=Stop.HOLD, duty_limit=50)
    # Raise the arm
    arm.run_target(60, 0)


def robot_release(position):
    #the robot drops the brick on the correkt position

    # Rotate to the drop-off position
    rotate.run_target(60, position)
    # Lower the arm
    arm.run_target(60, -40)
    # Open the gripper to relise the brick
    grab.run_target(200, -90)
    # Raise the arm
    arm.run_target(60, 0)


#indikation och reset complete
for i in range(3):
    ev3.speaker.beep()
    wait(100)

#Define rotation possitions
LEFT = 160
MIDDLE = 100
RIGHT = 40

#main loop
while True:
    # Move a brick from the left to the middle
    robot_pick(LEFT)
    robot_release(MIDDLE)

    # Move a brick from the right to the left
    robot_pick(RIGHT)
    robot_release(LEFT)

    # Move a brick from the middle to the right
    robot_pick(MIDDLE)
    robot_release(RIGHT)
