## Ultrasonic Sensor Library for Raspberry Pi Pico - DIYables_Pico_Ultrasonic_Sensor
This MicroPython library is designed for Raspberry Pi Pico to make it easy to use with ultrasonic sensor. It is easy to use for not only beginners but also experienced users... 

It is created by DIYables to work with DIYables Ultrasonic Sensor, but also work with products from other brands. Please consider purchasing products from [DIYables Store on Amazon](https://www.amazon.com/dp/B0BDFLPZ2R) to support our work.



Features
----------------------------
* Works with any Raspberry Pi Pico board.
* Supports the noise filter  (filtering noise from enviroment, ultrasonic interference...)
* Supports detection threshold. If distance > threshold, the library will not consider any object detected.


Available Functions
----------------------------
* __init__(trig_pin, echo_pin)
* set_detection_threshold(distance)
* enable_filter(num_samples=20)
* disable_filter()
* loop()
* get_distance()


Available Examples
----------------------------
* main.py



Tutorials
----------------------------
* [Raspberry Pi Pico - Ultrasonic Sensor](https://newbiely.com/tutorials/raspberry-pico/raspberry-pi-pico-ultrasonic-sensor)



References
----------------------------
* [Raspberry Pi Pico - Ultrasonic Sensor Library](https://newbiely.com/tutorials/raspberry-pico/raspberry-pi-pico-ultrasonic-sensor-library)
