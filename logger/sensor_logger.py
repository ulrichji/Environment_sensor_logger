#! python3

import sys

import example_measurement_stream
import gui
import tkinter as tk
import threading

def applicationThread(application):
	application.mainloop()

def loggerThread(application, logger):
	#Register what function to call when the gui is closing
	application.addStopCallback(logger.stopStream)
	#Set which function the logger should send measurements to
	logger.setMeasurementCallback(application.addMeasurement)
	#Now start the actual logger stream
	logger.startStream()

def main():
	#Set default logger as the example logger
	logger_type = "example"
	
	if(len(sys.argv) > 1):
		logger_type = sys.argv[1].lower()
	
	logger = None
	
	#It is already lowercase
	if(logger_type == "example"):
		logger = example_measurement_stream.ExampleMeasurementStream()
	elif(logger_type.startswith("com")):
		#TODO open a serial logger
		pass
	else:
		raise Exception("The logger "+str(logger_type)+" is not recognized by the system")
	
	root = tk.Tk()
	application = gui.SensorLoggerApplication(root)
	
	logger_thread = threading.Thread(target=loggerThread, args=(application,logger,))
	logger_thread.start()
	
	#This must be on the main thread
	applicationThread(application)
	
	return logger_type

if __name__ == "__main__":
	main()
