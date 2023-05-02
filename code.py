#!/usr/bin/env pybricks-micropython
#import modules
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Stop, Direction, Color
from pybricks.tools import wait

#define motors and sensors
ev3 = EV3Brick()

grab = Motor(Port.A) #Gripp claw
arm = Motor(Port.B, Direction.COUNTERCLOCKWISE, [8, 40])#elbow motor
rotate = Motor(Port.C, Direction.COUNTERCLOCKWISE, [12, 36])#rotation motor
arm.control.limits(speed=60, acceleration=120)#Limits in extention of the arm
rotate.control.limits(speed=60, acceleration=120)#rotation limits
base_switch = TouchSensor(Port.S1) #base tutch sensor
arm_sensor = ColorSensor(Port.S2) #collor sensor

#reset the arm
arm.run_until_stalled(-30, then=Stop.HOLD, duty_limit=7)
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

#Define rotation possitions
PICKUP = 200
LEFT = 140
MIDLE_LEFT = 100
MIDLE = 60
RIGHT = 0

#Define elevation possitions
DOWN = 0
CHECK = 45

#define collors
RED = Color.RED
YELLOW = Color.YELLOW
GREEN = Color.GREEN
BLUE = Color.BLUE
BLACK = Color.BLACK
BROWN = Color.BROWN
color_list = [RED, YELLOW, GREEN, BLUE]

def robot_pick(position):
    #pick upp the brick
    # move to pickup position
    rotate.run_target(60, position)
    # Lower the arm
    arm.run_until_stalled(-60,then=Stop.HOLD, duty_limit=20)
    # grab the block
    grab.run_until_stalled(200, then=Stop.HOLD, duty_limit=50)
    # Raise the arm
    arm.run_target(60, CHECK)

def robot_release(position):
    #the robot drops the brick on the correkt position

    # Rotate to the drop-off position
    rotate.run_target(60, position)
    # Lower the arm
    arm.run_target(60, DOWN)
    # Open the gripper to relise the brick
    grab.run_target(200, -90)
    # Raise the arm
    arm.run_target(60, CHECK)

def check_colors():
    robot_pick(LEFT)
    left_color = arm_sensor.color()
    for i in range(50):
        left_color = arm_sensor.color()
        if left_color in color_list:
            break
    robot_release(LEFT)
    
    robot_pick(MIDLE_LEFT)
    middle_left_color = arm_sensor.color()
    for i in range(50):
        middle_left_color = arm_sensor.color()
        if middle_left_color in color_list:
            break
    robot_release(MIDLE_LEFT)

    robot_pick(MIDLE)
    middle_color = arm_sensor.color()
    for i in range(50):
        middle_color = arm_sensor.color()
        if middle_color in color_list:
            break
    robot_release(MIDLE)

    robot_pick(RIGHT)
    right_color = arm_sensor.color()
    for i in range(50):
        right_color = arm_sensor.color()
        if right_color in color_list:
            break
    robot_release(RIGHT)

    print("left: " + str(left_color) +"middle_left: " + str(middle_left_color) + " middle: " + str(middle_color) + " right: "+ str(right_color))

#indikation och reset complete
for i in range(3):
    ev3.speaker.beep()
    wait(100)
arm.run_target(60, CHECK)    

#main loop
tries = 0
block = False
while True:
    robot_pick(PICKUP)
    for i in range(50):
        block = arm_sensor.color()
        if block in color_list:
            break

    print(block)
    print(tries)
    # Move a brick från middle till position
    if block == YELLOW:
        robot_release(MIDLE)
        tries = 0
    elif block == RED:
        robot_release(LEFT)
        tries = 0
    elif block == GREEN:
        robot_release(RIGHT)
        tries = 0
    elif block == BLUE:
        robot_release(MIDLE_LEFT)
        tries = 0
    elif grab.angle() >= 5:
        tries += 1
    elif tries >= 3:
        wait(2000)
        grab.run_target(200, -90)
        check_colors()
        tries = 0
        wait(10000)
    elif block == BLACK or BROWN:
        for i in range(50):
            block = arm_sensor.color()
            arm.run_target(60, DOWN)
            # Open the gripper to relise the brick
            grab.run_target(200, -90)

            if block in color_list:
                break
        grab.run_target(200, -90)
        tries += 1
