#! python3

import measurement_stream
import measurement

import serial

class SerialMeasurementStream(measurement_stream.MeasurementStream):
	
	def __init__(self, serial_port):
		self.running = True
		self.serial_port = serial_port
	
	def startStream(self):
		self.running = True
		
		ser = serial.Serial(self.serial_port, timeout=1.0)
		
		while(self.running):
			line = ser.readline().decode("utf-8") 
			measure = measurement.Measurement(line)
			self.measurementCallback(measure)
	
	def stopStream(self):
		self.running = False
