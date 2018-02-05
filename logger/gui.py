#! python3

import tkinter as tk
import measurement
import collections
import threading
import time

class SensorLoggerApplication(tk.Frame):
	
	def __init__(self, master=None):
		super().__init__(master)
		self.pack()
		self.value_list = collections.OrderedDict()
	
	def addMeasurement(self,measurement):
		name = measurement.name
		
		if(name in self.value_list):
			value_tuple = self.value_list[name]
			value_tuple[1].set(measurement.value)
			value_tuple[2].set(measurement.unit)
		
		else:
			name_label_text = tk.StringVar()
			value_label_text = tk.StringVar()
			unit_label_text = tk.StringVar()
			
			name_label_text.set(measurement.name)
			value_label_text.set(measurement.value)
			unit_label_text.set(measurement.unit)
			
			name_label = tk.Label(self, textvariable=name_label_text)
			value_label = tk.Label(self, textvariable=value_label_text)
			unit_label = tk.Label(self, textvariable=unit_label_text)
			
			name_label.grid(row=len(self.value_list), column=0)
			value_label.grid(row=len(self.value_list), column=1)
			unit_label.grid(row=len(self.value_list), column=2)
			
			self.value_list[name] = [name_label_text, value_label_text, unit_label_text]

def exampleMeasurements(application):
	time.sleep(1.0)
	ex1 = measurement.Measurement("")
	ex1.name = "CO2"
	ex1.value = "2000"
	ex1.unit = "ppm"
	application.addMeasurement(ex1)
	
	time.sleep(1.0)
	ex2 = measurement.Measurement("")
	ex2.name = "CO2"
	ex2.value = "2200"
	ex2.unit = "ppm"
	application.addMeasurement(ex2)
	
	time.sleep(1.0)
	ex3 = measurement.Measurement("")
	ex3.name = "Temperature"
	ex3.value = "22.2"
	ex3.unit = "C"
	application.addMeasurement(ex3)

def main():
	root = tk.Tk()
	logger_application = SensorLoggerApplication(master=root)
	
	example_thread = threading.Thread(target=exampleMeasurements, args=(logger_application,))
	example_thread.start()
	
	logger_application.mainloop()
	
	example_thread.join()
	
if __name__ == "__main__":
	main()
