#include <Time.h>
#include "measurement.h"
#include <DHT22.h>

int lightSensorIn = A0;
int soundSensorIn = A2;
int co2SensorIn = A4;
int tempHumidSensorIn = 7;

DHT22 temp_humid_sensor(tempHumidSensorIn);
const char* last_DHT22_error = "";

void setup()
{
  Serial.begin(9600); // open serial port, set the baud rate to 9600 bps
  // Set the default voltage of the reference voltage
  analogReference(DEFAULT);
}

Measurement measureCO2(void)
{
  Measurement measurement;
  measurement.name = "CO2";
  measurement.unit = "ppm";
  measurement.time = 2000;
  measurement.error = "";

  int sensor_value = analogRead(co2SensorIn);
  float voltage = sensor_value * (5000 / 1024.0);
  if (voltage == 0)
  {
    measurement.error = "Measurement error";
  }
  else if (voltage < 400)
  {
    measurement.error = "Preaheating";
  }
  else
  {
    int voltage_difference = voltage - 400;
    float concentration = voltage_difference * 50.0 / 16.0;
    measurement.value = concentration;
  }

  return measurement;
}

void readDHT22Data(void)
{
  last_DHT22_error = "";
  DHT22_ERROR_t error_code;
  error_code = temp_humid_sensor.readData();
  
  switch(error_code)
  {
    case DHT_ERROR_CHECKSUM:
      last_DHT22_error = "DHT22: check sum error";
      break;
    case DHT_BUS_HUNG:
      last_DHT22_error = "DHT22: Bus hung error";
      break;
    case DHT_ERROR_NOT_PRESENT:
      last_DHT22_error = "DHT22: Not present";
      break;
    case DHT_ERROR_ACK_TOO_LONG:
      last_DHT22_error = "ACK time out";
      break;
    case DHT_ERROR_SYNC_TIMEOUT:
      last_DHT22_error = "Sync timeout";
      break;
    case DHT_ERROR_DATA_TIMEOUT:
      last_DHT22_error = "Data timeout";
      break;
    case DHT_ERROR_TOOQUICK:
      last_DHT22_error = "Polled to quick";
      break;
  }
}

Measurement measureTemperature(bool do_read_data=true)
{
  Measurement measurement;

  measurement.name = "Temp";
  measurement.unit = "C";
  measurement.time = 2000;
  measurement.error = "";

  if(do_read_data)
  {
    readDHT22Data();
  }

  measurement.value = temp_humid_sensor.getTemperatureC();
  measurement.error = last_DHT22_error;

  return measurement;
}

Measurement measureHumidity(bool do_read_data=true)
{
  Measurement measurement;

  measurement.name = "Humidity";
  measurement.unit = "%";
  measurement.time = 2000;
  measurement.error = "";

  if(do_read_data)
  {
    readDHT22Data();
  }
  measurement.value = temp_humid_sensor.getHumidity();
  measurement.error = last_DHT22_error;

  return measurement;
}

void sendMeasurementOnSerial(Measurement measurement)
{

  Serial.print("name:\""); Serial.print(measurement.name); Serial.print("\";");
  Serial.print("timestamp:"); Serial.print(measurement.timestamp); Serial.print(";");
  Serial.print("sequence:"); Serial.print(measurement.sequence); Serial.print(";");
  Serial.print("value:"); Serial.print(measurement.value); Serial.print(";");
  Serial.print("unit:\""); Serial.print(measurement.unit); Serial.print("\";");
  Serial.print("time:"); Serial.print(measurement.time); Serial.print(";");
  Serial.print("Error:\"");Serial.print(measurement.error);Serial.print("\";");
  Serial.println("");
}

void loop()
{
  while (1)
  {
    Measurement co2Measurement = measureCO2();
    Measurement temperatureMeasurement = measureTemperature();
    //The false argument prevents a new read and uses the value obtained from the same sensor in the temperature measurement
    //If not set to false, it will give a "polled to quickly error"
    Measurement humidityMeasurement = measureHumidity(false);
    
    sendMeasurementOnSerial(co2Measurement);
    sendMeasurementOnSerial(temperatureMeasurement);
    sendMeasurementOnSerial(humidityMeasurement);

    delay(2000);
  }
}
