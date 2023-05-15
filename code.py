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
CHECK = 41
UPP = 100

#more flexible positional defenitions
PICKUP = {"rotation": 200, "hight": 0}
GREEN_POS = {"rotation": 140, "hight": 0}
RED_POS = {"rotation": 100, "hight": 0}
YELLOW_POS = {"rotation": 60, "hight": 0}
BLUE_POS = {"rotation": 0, "hight": 0}
pos_list = ["PICKUP", "GREEN", "RED", "YELLOW", "BLUE"]

#define collors
RED = Color.RED
YELLOW = Color.YELLOW
GREEN = Color.GREEN
BLUE = Color.BLUE
BLACK = Color.BLACK
BROWN = Color.BROWN
color_list = [RED, YELLOW, GREEN, BLUE]

times = 0
while True:
    buttons_pressed = EV3Brick.buttons.pressed()
    if len(buttons_pressed) == 0:
        arm.hold()
        rotate.hold()
        pass
    else:
        for i in range(len(buttons_pressed)):
            buttons_pressed[i] = str(buttons_pressed[i])
    print(EV3Brick.buttons.pressed())
    if "Button.LEFT" in buttons_pressed:
        rotate.run(30)
    if "Button.RIGHT" in buttons_pressed:
        rotate.run(-30)
    if "Button.UP" in buttons_pressed:
        arm.run(20)
    if "Button.DOWN" in buttons_pressed:
        arm.run(-20)
    if "Button.CENTER" in buttons_pressed:
        if times == 0:
            PICKUP["rotation"] = rotate.angle() 
            PICKUP["hight"] = arm.angle()
        elif times == 1:
            GREEN_POS["rotation"] = rotate.angle()
            GREEN_POS["hight"] = arm.angle()
        elif times == 2:
            RED_POS["rotation"] = rotate.angle()
            RED_POS["hight"] = arm.angle()
        elif times == 3:
            YELLOW_POS["rotation"] = rotate.angle()
            YELLOW_POS["hight"] = arm.angle()
        elif times == 4:
            BLUE_POS["rotation"] = rotate.angle()
            BLUE_POS["hight"] = arm.angle()
        times += 1
        ev3.speaker.beep()
        wait(500)
        ev3.screen.clear()
    ev3.screen.draw_text(40, 50, pos_list[times])

    if times >= 4:
        break

#indikation och reset complete
for i in range(3):
    ev3.speaker.beep()
    wait(100)
arm.run_target(60, CHECK)    

def robot_pick(position):
    #pick upp the brick

    # move to pickup position
    rotate.run_target(60, position["rotation"])
    # Lower the arm
    arm.run_target(60, position["hight"])
    # grab the block
    grab.run_until_stalled(200, then=Stop.HOLD, duty_limit=50)
    # Raise the arm
    arm.run_target(60, CHECK)

def robot_release(position):
    #the robot drops the brick on the correkt position
    # Rotate to the drop-off position
    rotate.run_target(60, position["rotation"])
    # Lower the arm
    arm.run_target(60, position["hight"])
    # Open the gripper to relise the brick
    grab.run_target(200, -90)
    # Raise the arm
    arm.run_target(60, CHECK)

def check_colors():
    ev3.screen.clear()
    ev3.screen.draw_text(40, 50, "Checking Colors")
    robot_pick(GREEN_POS)
    left_color = arm_sensor.color()
    for i in range(50):
        left_color = arm_sensor.color()
        if left_color in color_list:
            break
    robot_release(GREEN_POS)
    
    robot_pick(RED_POS)
    middle_left_color = arm_sensor.color()
    for i in range(50):
        middle_left_color = arm_sensor.color()
        if middle_left_color in color_list:
            break
    robot_release(RED_POS)

    robot_pick(BLUE_POS)
    middle_color = arm_sensor.color()
    for i in range(50):
        middle_color = arm_sensor.color()
        if middle_color in color_list:
            break
    robot_release(BLUE_POS)

    robot_pick(YELLOW_POS)
    right_color = arm_sensor.color()
    for i in range(50):
        right_color = arm_sensor.color()
        if right_color in color_list:
            break
    robot_release(YELLOW_POS)

    print("left: " + str(left_color) +"middle_left: " + str(middle_left_color) + " middle: " + str(middle_color) + " right: "+ str(right_color))

    rotate.run_target(60, PICKUP["rotation"])

#main loop
tries = 0
block = False
stanby = False
while True:
    ev3.screen.clear()
    ev3.screen.draw_text(40, 50, "Begin Sort")
    if stanby != True:
        robot_pick(PICKUP)
        block = arm_sensor.color()

    # Move a brick från pickupp till position
    if CHECK <= PICKUP["hight"] or GREEN_POS["hight"] or RED_POS["hight"] or YELLOW_POS["hight"] or BLUE_POS["hight"]:
        arm.run_target(60, UPP)

    if block == YELLOW:
        robot_release(YELLOW_POS)
        tries = 0
    elif block == RED:
        robot_release(RED_POS)
        tries = 0
    elif block == GREEN:
        robot_release(GREEN_POS)
        tries = 0
    elif block == BLUE:
        robot_release(BLUE_POS)
        tries = 0
    elif grab.angle() >= 5:
        tries += 1
    elif tries >= 3:
        wait(2000)
        grab.run_target(200, -90)
        check_colors()
        standby = True
        while standby: #efter att ha kontrolerat alla positioner så ställer den sig vid stanby och plockar tills dess att den hittar något 
            ev3.screen.clear()
            ev3.screen.draw_text(40, 50, "Standing By")
            wait(5000)
            grab.run_target(200, -90)
            robot_pick(PICKUP)
            block = arm_sensor.color()
            print(block)
            if block in color_list:
                standby = False
                tries = 0
                break
    elif block == BLACK or BROWN or None:
        for i in range(50):
            block = arm_sensor.color()
            # Open the gripper to relise the brick
            grab.run_target(200, -90)

            if block in color_list:
                break
        grab.run_target(200, -90)
        tries += 1
    print(block)
    print(tries)
