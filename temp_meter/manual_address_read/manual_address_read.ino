#include <OneWire.h>
#include <DallasTemperature.h>

#define ONE_WIRE_BUS 2

OneWire oneWire(ONE_WIRE_BUS);

DallasTemperature sensors(&oneWire);

float tempC = 0;
float tempF = 0;

void setup() {
  sensors.begin();
  pinMode(3, OUTPUT);
  analogWrite(3, 0);
  Serial.begin(9600);
  
}

void loop() {
  sensors.requestTemperatures();
  tempC = sensors.getTempCByIndex(0);
  tempF = sensors.toFahrenheit(tempC);
  delay(1000);
  
  Serial.print("C: ");
  Serial.print(tempC);
  Serial.print("   F: ");
  Serial.println(tempF);
}
