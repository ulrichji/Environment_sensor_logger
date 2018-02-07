
from measurement import *

class MeasurementStream:
	
	def __init__(self):
		self.mesurement_callback = None

	def setMeasurementCallback(self, callback):
		self.measurement_callback = callback

	def measurementCallback(self, measurement):
		if(not (self.measurement_callback is None)):
			self.measurement_callback(measurement)
	
	def startStream(self):
		pass

	def stopStream(self):
		pass
