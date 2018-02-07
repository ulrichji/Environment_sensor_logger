
def specialCharConversion(special_char):
	return special_char

def parseMeasurement(measurement_string):
	key_values = {}
	state = "key"
	key = ''
	value = ''
	
	for char in measurement_string:
		if(state == "key"):
			if(char == ":"):
				state = "value"
			else:
				key += char
				
		elif(state == "value"):
			if(char == "\""):
				state = "string"
			#We have finished the key
			elif(char == ";"):
				key_values[key] = value
				key = ''
				value = ''
				state = "key"
			else:
				value += char
				
		elif(state == "string"):
			if(char == "\\"):
				state = "escape"
			elif(char == "\""):
				state = "value"
			else:
				value += char
				
		elif(state == "escape"):
			value += specialCharConversion(char)
	
	if(key != '' or value != ''):
		key_values[key] = value

	return key_values

class Measurement:
	
	def __init__(self, measurement_string = ""):
		key_values = parseMeasurement(measurement_string)
		
		self.timestamp = None
		self.sequence = None
		self.value = None
		self.unit = None
		self.sensor_name = None
		self.next_measurement_time = 1000
		
		if("timestamp" in key_values):
			self.timestamp = key_values["timestamp"]
		if("sequence" in key_values):
			self.sequence = int(key_values["sequence"])
		if("value" in key_values):
			self.value = float(key_values["value"])
		if("unit" in key_values):
			self.unit = key_values["unit"]
		if("name" in key_values):
			self.sensor_name = key_values["name"]
		if("time" in key_values):
			self.next_measurement_time = int(key_values["time"])


def run_tests():
	measurement_string = "timestamp:\"31.01.2018:12:48\";sequence:1002341;value:440;unit:ppm;name:\"CO2\";time=2000"
	measurement_string2 = "timestamp:\"31.01.2018:12:48\";sequence:1002341;value:440;unit:ppm;name:\"CO2\";time=2000;"
	key_pairs = parseMeasurement(measurement_string)
	key_pairs2 = parseMeasurement(measurement_string2)
	print(key_pairs)
	print(key_pairs2)
	
	measure1 = Measurement(measurement_string)
	measure2 = Measurement(measurement_string2)
	
	print(measure1)
	print(measure2)


if __name__ == "__main__":
	run_tests()
