#! python3

import tkinter as tk
import measurement
import collections
import threading
import time
import example_measurement_stream

class SensorLoggerApplication(tk.Frame):
	
	def __init__(self, master=None):
		super().__init__(master)
		self.pack()
		self.value_list = {}
		self.stop_callbacks = []
		
		self.master = master
		if(not (master is None)):
			master.protocol("WM_DELETE_WINDOW", self.stop)
	
	def stop(self):
		for stop_callback in self.stop_callbacks:
			stop_callback()
		
		if(not (self.master is None)):
			self.master.destroy()
	
	def addStopCallback(self, stop_callback):
		self.stop_callbacks.append(stop_callback)
	
	def processEvents(self):
		shortest_time = float("inf")
		event_name = ""
		current_time = time.time()
		
		for key in self.value_list:
			label_tuple = self.value_list[key]
			label_time = label_tuple[7]
			
			if(label_time < shortest_time):
				shortest_time = label_time
				event_name = key
	
	def addMeasurement(self, measurement):
		name = measurement.sensor_name
		
		if(not (name is None)):
			if(name in self.value_list):
				value_tuple = self.value_list[name]
				value_tuple[1].set(measurement.value)
				value_tuple[2].set(measurement.unit)
			
			else:
				name_label_text = tk.StringVar()
				value_label_text = tk.StringVar()
				unit_label_text = tk.StringVar()
				
				name_label_text.set(measurement.sensor_name)
				value_label_text.set(measurement.value)
				unit_label_text.set(measurement.unit)
				
				name_label = tk.Label(self, textvariable=name_label_text, font=("Calibri",40))
				value_label = tk.Label(self, textvariable=value_label_text, font=("Calibri",40))
				unit_label = tk.Label(self, textvariable=unit_label_text, font=("Calibri",40))
				
				row = len(self.value_list)
				
				name_label.grid(row=row, column=0)
				value_label.grid(row=row, column=1)
				unit_label.grid(row=row, column=2)
				
				current_time = time.time()
				event_time = current_time + (measurement.next_measurement_time / 1000.0)
				self.value_list[name] = [name_label_text, value_label_text, unit_label_text, name_label, value_label, unit_label, row, event_time]
				self.processEvents()
	
	def reEnumerateElements(self):
		values = sorted(self.value_list.values(), key=lambda tup : tup[6])
		
		for expected_index in range(len(values)):
			actual_index = values[expected_index][6]
			if(actual_index != expected_index):
				values[expected_index][6] = expected_index
		
		for label_tuple in values:
			name_label = label_tuple[3]
			value_label = label_tuple[4]
			unit_label = label_tuple[5]
			row = label_tuple[6]
			
			name_label.grid_forget()
			value_label.grid_forget()
			unit_label.grid_forget()
			
			name_label.grid(row=row, column=0)
			value_label.grid(row=row, column=1)
			unit_label.grid(row=row, column=2)
	
	def removeMeasurement(self, measure):
		name = ""
		if(type(measure) is measurement.Measurement):
			name = measure.sensor_name
		else:
			name = measure
		
		if(name in self.value_list):
			self.value_list[name][3].grid_forget()
			self.value_list[name][4].grid_forget()
			self.value_list[name][5].grid_forget()
			
			del self.value_list[name]
			self.reEnumerateElements()
			
		else:
			raise Exception("The sensor "+str(name)+" cannot be removed because it's not added.")
		
		self.processEvents()

def exampleMeasurements(application):
	time.sleep(1.0)
	ex1 = measurement.Measurement("")
	ex1.sensor_name = "CO2"
	ex1.value = "2000"
	ex1.unit = "ppm"
	application.addMeasurement(ex1)
	
	time.sleep(1.0)
	ex2 = measurement.Measurement("")
	ex2.sensor_name = "CO2"
	ex2.value = "2200"
	ex2.unit = "ppm"
	application.addMeasurement(ex2)
	
	time.sleep(1.0)
	ex3 = measurement.Measurement("")
	ex3.sensor_name = "Temperature"
	ex3.value = "22.2"
	ex3.unit = "C"
	application.addMeasurement(ex3)
	
	ex4 = measurement.Measurement("")
	ex4.sensor_name = "Humidity"
	ex4.value = "30"
	ex4.unit = "%"
	application.addMeasurement(ex4)
	
	time.sleep(1.0)
	application.removeMeasurement(ex1)
	time.sleep(1.0)
	application.removeMeasurement("Temperature")
	
	time.sleep(1.0)
	ex5 = measurement.Measurement("")
	ex5.sensor_name = "Humidity"
	ex5.value = "34"
	ex5.unit = "%"
	application.addMeasurement(ex5)

	time.sleep(1.0)
	ex6 = measurement.Measurement("")
	ex6.sensor_name = "CO2"
	ex6.value = "2300"
	ex6.unit = "ppm"
	application.addMeasurement(ex6)

def exampleMeasurements2(application):
	stream = example_measurement_stream.ExampleMeasurementStream()
	
	application.addStopCallback(stream.stopStream)
	stream.setMeasurementCallback(application.addMeasurement)
	stream.startStream()

def main():
	root = tk.Tk()
	logger_application = SensorLoggerApplication(master=root)
	
	example_thread = threading.Thread(target=exampleMeasurements2, args=(logger_application,))
	example_thread.start()
	
	logger_application.mainloop()
	
	example_thread.join()
	
if __name__ == "__main__":
	main()
