# Raspberry-Pi Fan Control

Fan control for Raspberry Pi based on the embedded CPU temp sensor and a fan which speed is controlled via PWM.

This Python code can be run as service.

Use the calibration tool to get pairs of temperature and fan speeds in % which match your needs.
Usually not more than 4 pairs are required.

Then use these values in the fan_control_settings code to activate them.

Note that the Pi caps CPU processing if the temperature exceeds 80°.

Any change in the fan speed is logged together with the CPU temp in the syslog.
