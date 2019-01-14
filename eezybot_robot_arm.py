import pygame
import time

# Calculate what position to set the servo to given the value of the axis on the
# xbox controller.
# @param servo_min The position that the servo servo (a value between 0 and 180)
#     should be at when the joystick axis is at position -1 (all the way down).
# @param servo_max The position that the servo should be at when the joystick
#     axis is at position 1 (all the way up).
# Note: It's fine for servo_min to be bigger value than servo_max.
def calculate_servo_command(axis_value, servo_min, servo_max, axis_min=-1, axis_max=1):
	# x = axis value (our input), y = servo value (our output)
	# y = mx + b
	# m = slope = rise / run
	m = (servo_max - servo_min) / (axis_max - axis_min)

	# y = mx + b
	# b = y - mx
	# plug in a point for x,y and solve for b
	b = servo_min - m*axis_min

	# plug current axis_value into our linear equation as the value x (our
	# input) to get the value of y (our servo output)
	return m*axis_value + b

# The servo_controller object allows us to set the positions of the servos
from adafruit_servokit import ServoKit
servo_controller = ServoKit(channels=16)

# Use pygame to connect to the xbox controller. This will allow us to check for
# button presses and joystick movement.
pygame.init()
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
print ("connected joysticks: {}".format(joysticks))
if len(joysticks) == 0:
	print("No joystick connected")
	exit(1)

# we'll use the first joystick in the list as the controller for the robot.
# TODO: if multiple joysticks are connected, it would be better to choose one by name
j = joysticks[0]
print("Using joystick '{}'".format(j.get_name()))

j.init()

# prints out the status of each button, whether or not it is pressed
def print_buttons(js):
	pygame.event.pump()
	for button_num in range(js.get_numbuttons()):
		print("Button {} is pressed ? {}".format(button_num, js.get_button(button_num)))


# prints out the value of each controller axis
def print_axes(js):
	pygame.event.pump()
	for axis_num in range(js.get_numaxes()):
		print("axis {} is pressed ? {}".format(axis_num, js.get_axis(axis_num)))


# ensure x is between 0 and 180. values outside of this range are invalid to
# send to the joystick and will cause errors
def servo_clamp(x):
	if x > 180:
		return 180
	if x < 0:
		return 0
	return x

# Uncomment this to continually print out button and axis state. Helpful for
# figuring out which number corresonds to which button/axis on the controller
#while True:
#	print_buttons(j)
#	print_axes(j)
#	print("-------------------------------------------------------------------------------------")
#	time.sleep(1)

# Give names to each of the servos we're going to use
gripper_servo = servo_controller.servo[1]
base_servo = servo_controller.servo[3]
shoulder_servo = servo_controller.servo[2]
elbow_servo = servo_controller.servo[4]

# Main loop. Controls each of the robot arm servos according to the axes on the
# joystick controller. For each joystick axis we're interested in, the value is
# read and used to set the desired position of the corresponding servo.
while True:
	# This has to be called before j.get_axis() or j.get_button(), otherwise new
	# axis movements / button presses won't be detected.
	pygame.event.pump()
	
	# Gripper control!
	#RT is Axis 5, minimum value is (-1.0) (minimum means button not pressed )
	# (when Axis is pressed all the way it is 1.0)
	rt = j.get_axis(5)
	gripper_servo.angle = calculate_servo_command(rt, 150, 0)
	
	# Base Control!
	r3leftright = j.get_axis(3)
	base_servo.angle = calculate_servo_command(r3leftright, 0, 180)
	
	# Shoulder control!
	r3updown = j.get_axis(4)
	# note: when this joystick axis is up, the reading is -1 which is wierd...
	shoulder_servo.angle = calculate_servo_command(r3updown, 133, 42)

	# Elbow control!
	l3updown = j.get_axis(1)
	elbow_servo.angle = calculate_servo_command(l3updown, 110, 179)
