# example_usage.py
from DIYables_Pico_Ultrasonic_Sensor import UltrasonicSensor
import time

sensor = UltrasonicSensor(trig_pin=1, echo_pin=0)
sensor.set_detection_threshold(140)  # Set detection threshold to 140 cm
sensor.enable_filter(num_samples=20)  # Enable filtering and set number of samples to 20

while True:
    sensor.loop()  # Perform measurement cycle
    distance = sensor.get_distance()
    if not distance:
        print('No object detected within the set distance')
    else:
        # Print the distance formatted to two decimal places using format()
        print('Filtered distance: {:.2f} cm'.format(distance))
    time.sleep(1)  # Reduced sleep time to enhance measurement responsiveness

