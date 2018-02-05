typedef struct struct_measurement
{
  const char* name;
  int timestamp;
  int sequence;
  float value;
  const char* unit;
  int time;
  const char* error;
} Measurement;
