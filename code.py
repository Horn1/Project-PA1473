#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Stop, Direction
from pybricks.tools import wait

# Create your objects here

# Initialize the EV3 Brick.
ev3 = EV3Brick()

# Initialize a motor at port B.
grab = Motor(Port.A)
upndown = Motor(Port.B)
turn = Motor(Port.C)

# Write your program here
color = ColorSensor(Port.S2)
touch = TouchSensor(Port.S1)




# Run the motor up to 500 degrees per second. To a target angle of 90 degrees.
# grab.run_target(500, 90)

grab.run_until_stalled(200, then=Stop.COAST, duty_limit=50)
grab.reset_angle(0)
grab.run_target(200, -90)

grab.run_target(200,90)
    

# Play another beep sound.
ev3.speaker.beep(frequency=1000, duration=500)



# This function makes the robot base rotate to the indicated
# position. There it lowers the elbow, closes the gripper, and
# raises the elbow to pick up the object.

# Rotate to the pick-up position.
turn.run_target(200, -90)
# Lower the arm.
upndown.run_target(60, -40)
# Close the gripper to grab the wheel stack.
grab.run_until_stalled(200, then=Stop.HOLD, duty_limit=50)
# Raise the arm to lift the wheel stack.
upndown.run_target(60, 0)


