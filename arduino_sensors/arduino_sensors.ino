/*
# Reads temperature sensor and pH meter
# Editor : David Roberts
# Ver : 1.0
# Products: analog pH meter, DS18B20 temp sensor
*/

#include <OneWire.h>
#include <DallasTemperature.h>

// initialization of temp sensor
#define ONE_WIRE_BUS 2
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

// defining constants 
#define printInterval 1000 * 10
#define phSensorPin A0 //pH meter Analog output to Arduino Analog Input 0
#define calibrationOffset 0.26 //deviation compensate
#define samplingInterval 20
#define ArrayLength 40 //times of collection
int pHArray[ArrayLength];
int arrayIndex = 0;

void setup(void) {
  Serial.begin(9600);
  Serial.println("Booch Sensors // Serial Monitor Version"); 
  sensors.begin();
}

void loop(void) {
  
  static unsigned long samplingTime = millis();
  static unsigned long printTime = millis();
  static float pHValue, voltage;
  static float tempC, tempF;
  if (millis() - samplingTime > samplingInterval) {
    
    arrayIndex++;
    pHArray[arrayIndex] = analogRead(phSensorPin);
    if (arrayIndex == ArrayLength) arrayIndex = 0;
    voltage = avergearray(pHArray, ArrayLength) * 5.0 / 1024;
    pHValue = 3.5 * voltage + calibrationOffset;
    samplingTime = millis();
  }
  if (millis() - printTime > printInterval) // if over print interval, gather temp and print
  {
    
    sensors.requestTemperatures();
    tempC = sensors.getTempCByIndex(0);
    tempF = (9.0/5) * (tempC + 32);
    
    Serial.print("{'voltage':");
    Serial.print(voltage, 2);
    Serial.print(", 'pH':");
    Serial.print(pHValue, 2);
    Serial.print(", 'temp_c':");
    Serial.print(tempC, 2);
    Serial.print(", 'temp_f':");
    Serial.print(tempF, 2);
    Serial.print("}\n");
    printTime = millis();
  }
}

// helper functions
double avergearray(int * arr, int number) {
  int i;
  int max, min;
  double avg;
  long amount = 0;
  if (number <= 0) {
    Serial.println("Error number for the array to avraging!/n");
    return 0;
  }
  if (number < 5) { //less than 5, calculated directly statistics
    for (i = 0; i < number; i++) {
      amount += arr[i];
    }
    avg = amount / number;
    return avg;
  } else {
    if (arr[0] < arr[1]) {
      min = arr[0];
      max = arr[1];
    } else {
      min = arr[1];
      max = arr[0];
    }
    for (i = 2; i < number; i++) {
      if (arr[i] < min) {
        amount += min; //arr<min
        min = arr[i];
      } else {
        if (arr[i] > max) {
          amount += max; //arr>max
          max = arr[i];
        } else {
          amount += arr[i]; //min<=arr<=max
        }
      } //if
    } //for
    avg = (double) amount / (number - 2);
  } //if
  return avg;
}

