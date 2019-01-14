import pygame
import time
from adafruit_servokit import ServoKit

# prints out the status of each button, whether or not it is pressed
def watch_joystick(js):
	pygame.event.pump()
	for button_num in range(js.get_numbuttons()):
		print("Button {} is pressed ? {}".format(button_num, js.get_button(button_num)))
	for axis_num in range(js.get_numaxes()):
		print("axis {} is pressed ? {}".format(axis_num, js.get_axis(axis_num)))

def main():
	pygame.init()
	pygame.joystick.init()
	joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
	print("Connected joysticks: {}".format(joysticks))
	if len(joysticks) == 0: raise RuntimeError("No joystick connected")
	j = joysticks[0]
	print("Using joystick '{}'".format(j.get_name()))
	j.init()

	servo_controller = ServoKit(channels=16)
	control = lambda axis_value, servo_min, servo_max: (servo_max - servo_min) *(1+axis_value) / 2 + servo_min
	while True:
		pygame.event.pump()
		# axis num, servo num, servo min, servo max
		for cfg in [(5, 1, 150, 0), (3, 3, 0, 180), (4, 2, 133, 42), (1, 4, 110, 179)]:
			servo_controller.servo[cfg[1]].angle = control(j.get_axis(cfg[0]), cfg[2], cfg[3])

if __name__ == '__main__':
	main()
