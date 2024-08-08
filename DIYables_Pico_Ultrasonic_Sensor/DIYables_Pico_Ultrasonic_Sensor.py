"""
This MicroPython library is designed for Raspberry Pi Pico to make it easy to use with ultrasonic sensor. It is easy to use for not only beginners but also experienced users... 

It is created by DIYables to work with DIYables products, but also work with products from other brands. Please consider purchasing products from [DIYables Store on Amazon](https://amazon.com/diyables) from to support our work.

Product Link:
- Ultrasonic Sensor: https://diyables.io/products/ultrasonic-sensor
- Sensor Kit: https://diyables.io/products/sensor-kit


Copyright (c) 2024, DIYables.io. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

- Redistributions of source code must retain the above copyright
  notice, this list of conditions and the following disclaimer.

- Redistributions in binary form must reproduce the above copyright
  notice, this list of conditions and the following disclaimer in the
  documentation and/or other materials provided with the distribution.

- Neither the name of the DIYables.io nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY DIYABLES.IO "AS IS" AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL DIYABLES.IO BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""

# DIYables_Pico_Ultrasonic_Sensor.py

from machine import Pin
import time
import utime

class UltrasonicSensor:
    def __init__(self, trig_pin, echo_pin):
        self.trig = Pin(trig_pin, Pin.OUT)
        self.echo = Pin(echo_pin, Pin.IN)
        self.detection_threshold = float('inf')  # Initially set to infinity
        self.filter_enabled = False  # Filter is disabled by default
        self.num_samples = 1  # Default number of samples to 1 when filter is disabled
        self.distances = []  # Store measurements

    def loop(self):
        """Perform a measurement cycle and update the list of distances."""
        # Ensure the trigger pin is low for a clean pulse
        self.trig.low()
        time.sleep_us(5)
        
        # Send a 10 microsecond pulse to start the measurement
        self.trig.high()
        time.sleep_us(10)
        self.trig.low()
        
        start_time = utime.ticks_us()
        timeout = 30000  # Timeout in microseconds (e.g., 30 milliseconds)

        # Wait for the echo to start
        while self.echo.value() == 0:
            if utime.ticks_diff(utime.ticks_us(), start_time) > timeout:
                return None  # Return None or some error indication on timeout

        # Record the start time of the echo
        signal_off = utime.ticks_us()

        # Wait for the echo to end
        while self.echo.value() == 1:
            if utime.ticks_diff(utime.ticks_us(), signal_off) > timeout:
                return None  # Return None or some error indication on timeout

        # Record the end time of the echo
        signal_on = utime.ticks_us()
            
        # Calculate the duration of the echo pulse
        time_passed = utime.ticks_diff(signal_on, signal_off)
        
        # Calculate the distance in centimeters
        distance = (time_passed * 0.017)
        self.distances.append(distance)
        if len(self.distances) > self.num_samples:
            self.distances.pop(0)  # Maintain a fixed length of distances

    def get_distance(self):
        """Return the calculated distance based on current measurements."""
        if not self.distances:
            return None  # Return None if no measurements have been made yet

        # Check if filtering is enabled and there are enough samples to filter
        if self.filter_enabled and len(self.distances) >= self.num_samples:
            sorted_distances = sorted(self.distances)
            # Consider only the middle samples if filtering is enabled
            mid_index_start = len(sorted_distances) // 4
            mid_index_end = len(sorted_distances) * 3 // 4
            mid_distances = sorted_distances[mid_index_start:mid_index_end]
            if not mid_distances:  # Check if the slice results in an empty list
                return None  # Return None or an appropriate default value to prevent division by zero
            calculated_distance = sum(mid_distances) / len(mid_distances)
        else:
            # Use the latest measurement if no filtering or not enough samples for filtering
            calculated_distance = self.distances[-1] if self.distances else None

        if calculated_distance is None:
            return None  # Safeguard against no available data to process

        # Compare against the detection threshold
        if calculated_distance > self.detection_threshold:
            return False  # Indicate no object detected within the threshold
        return calculated_distance

    def set_detection_threshold(self, distance):
        """Set the maximum distance beyond which no object is considered detected."""
        self.detection_threshold = distance

    def enable_filter(self, num_samples=20):
        """Enable filtering of measurements and set number of samples for filtering."""
        if num_samples > 0:
            self.num_samples = num_samples
            self.filter_enabled = True
        else:
            raise ValueError("Number of samples must be greater than 0")

    def disable_filter(self):
        """Disable filtering of measurements and reset number of samples to 1."""
        self.filter_enabled = False
        self.num_samples = 1  # Reset to default sample count

