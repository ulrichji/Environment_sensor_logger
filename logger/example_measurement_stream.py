
from measurement_stream import *
import random
import time

class ExampleMeasurementStream(MeasurementStream):
	
	def __init__(self):
		self.running = True
	
	def stopStream(self):
		print("Stopping now")
		self.running = False
	
	def startStream(self):
		self.running = True
		name_list = ["CO2", "Temperature", "Humidity", "Sound", "Light"]
		unit_list = ["ppm", "C", "%", "dB", "Lux"]
		
		index = 0
		while(self.running):
			measurement = Measurement("")
			random_index = int(random.random() * len(name_list))
			measurement.sensor_name = name_list[random_index]
			measurement.unit = unit_list[random_index]
			measurement.value = random.random() * 1024
			measurement.sequence = index
			measurement.next_measurement_time = 1000
			
			self.measurementCallback(measurement)
			
			time.sleep(random.random())
			
			index += 1
		
		print("Has stopped")
