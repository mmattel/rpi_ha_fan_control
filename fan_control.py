#!/usr/bin/python3
#
# Raspberry-Pi Fan Control

# derived from:
# https://github.com/JeremySCook/RaspberryPi-Fan-Control
# https://www.instructables.com/PWM-Regulated-Fan-Based-on-CPU-Temperature-for-Ras/

import sys
import time
import syslog
import RPi.GPIO as GPIO
from fan_control_settings import * # import all variables defined in the settings file for direct usage

def main() -> None:
	# Setup GPIO pin
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(FAN_PIN, GPIO.OUT, initial=GPIO.LOW)
	fan = GPIO.PWM(FAN_PIN, PWM_FREQ)
	fan.start(0)

	i = 0
	cpuTemp = 0
	fanSpeed = 0
	cpuTempOld = 0
	fanSpeedOld = 0

	# We must set a speed value for each temperature step
	if len(speedSteps) != len(tempSteps):
		print("Quantity of temp and speed entries differ, exiting.")
		exit(0)

	syslog.syslog(syslog.LOG_INFO, 'Started temperature control by PWM fan')
	try:
		while True:
			# Read CPU temperature
			cpuTempFile = open("/sys/class/thermal/thermal_zone0/temp", "r")
			cpuTemp = float(cpuTempFile.read()) / 1000
			cpuTempFile.close()

			# Calculate desired fan speed
			if abs(cpuTemp - cpuTempOld) > hyst:
				# Below first value, fan will run at min speed.
				if cpuTemp < tempSteps[0]:
					fanSpeed = speedSteps[0]

				# Above last value, fan will run at max speed
				elif cpuTemp >= tempSteps[len(tempSteps) - 1]:
					fanSpeed = speedSteps[len(tempSteps) - 1]

				# If temperature is between 2 steps,
				# fan speed is calculated by linear interpolation
				else:
					for i in range(0, len(tempSteps) - 1):
						if (cpuTemp >= tempSteps[i]) and (cpuTemp < tempSteps[i + 1]):
							fanSpeed = round((speedSteps[i + 1] - speedSteps[i])
											/ (tempSteps[i + 1] - tempSteps[i])
											* (cpuTemp - tempSteps[i])
											+ speedSteps[i], 1)

				if fanSpeed != fanSpeedOld:
					if (fanSpeed != fanSpeedOld and (fanSpeed >= FAN_MIN or fanSpeed == 0)):
						fan.ChangeDutyCycle(fanSpeed)
						fanSpeedOld = fanSpeed
						syslog.syslog(syslog.LOG_INFO, 'CPU Temp: ' + str(cpuTemp) + '° Fan: ' + str(fanSpeed) + '%')
				cpuTempOld = cpuTemp

			# Wait until next refresh
			time.sleep(WAIT_TIME)

	# If a keyboard interrupt occurs (ctrl + c),
	# the GPIO is set to 0 and the program exits.
	except KeyboardInterrupt:
		print("\rFan control interrupted by keyboard")
		GPIO.cleanup()
		sys.exit()

if __name__ == "__main__":
	main()
