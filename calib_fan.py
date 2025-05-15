#!/usr/bin/python
#
# Calibration tool for Raspberry-Pi Fan Control

# check the fan speed by:
# changing the PWM Fan pin used
# --> for a printed temp, set the fan speed
# use another shell to create load (see below) to see the impact
# use the final values in fan_control_settings.py, usually only 4 pairs are needed.
# note that the fan may need a minimal speed to properly operate.
# you also must have a minimum temp/0 speed pair that will definitely be reached coming from top down !

# load creation
# sudo apt install stress-ng
# stress-ng --cpu 4 --cpu-method fft

import sys
import time
import RPi.GPIO as GPIO

# Configuration
FAN_PIN = 18   # BCM pin used to drive transistor's base
WAIT_TIME = 5  # [s] Time to wait between each refresh <-- for tests is is fine to have that in 5s intervals
FAN_MIN = 30   # [%] Fan minimum speed.
PWM_FREQ = 25  # [Hz] Change this value if fan has strange behavior

# Example of configurable temperature and fan speed steps
tempSteps = [52, 55, 60, 65]   # [°C]
speedSteps = [0, 45, 70, 100]  # [%]

# Example of fan speed will change only when the difference of temperature is higher than the hysteresis
hyst = 1

def main() -> None:
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(FAN_PIN, GPIO.OUT, initial=GPIO.LOW)

	fan=GPIO.PWM(FAN_PIN,PWM_FREQ)
	fan.start(0)

	try:
		while True:
			# Read CPU temperature
			cpuTempFile = open("/sys/class/thermal/thermal_zone0/temp", "r")
			cpuTemp = round(float(cpuTempFile.read()) / 1000, 2)
			cpuTempFile.close()

			fanSpeed=float(input("CPU-Temp = " + cpuTemp + "° Fan Speed: "))
			fan.ChangeDutyCycle(fanSpeed)

			# Wait until next refresh
			time.sleep(WAIT_TIME)

	except(KeyboardInterrupt):
		print("\rFan ctrl interrupted by keyboard")
		GPIO.cleanup()
		sys.exit()

if __name__ == "__main__":
	main()
