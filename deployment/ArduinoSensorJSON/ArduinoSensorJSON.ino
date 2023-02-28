/*
   USB Serial communication from Arduino to Pi
   Uses a neopixel for visual feedback of communication status and if wind sensor is functioning
*/
#define PIXPIN 6
#define NUMPIXELS 1
#define WIND_PIN A2
#include <Adafruit_Sensor.h>
#include <Adafruit_HMC5883_U.h>
#include <Adafruit_NeoPixel.h>
#include <ArduinoJson.h>

/*
   Pinout! the slip ring colors are:
   Yell: SDA
   Purp: SCL
   Blac: GND
   Redd: VCC
   Gree: NeoPixelData
   Gray: Not Used
*/

StaticJsonDocument<200> doc;
Adafruit_NeoPixel pixels(NUMPIXELS, PIXPIN, NEO_GRB + NEO_KHZ800);
Adafruit_HMC5883_Unified mag = Adafruit_HMC5883_Unified(12345);

int inByte = '0'; //the keep alive / are you there
String status_string; //to give errors

void setup() {

  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);
  pixels.begin();
  pixels.setPixelColor(0, pixels.Color(150, 0, 0));
  pixels.show();   // Send the updated pixel colors to the hardware.
  delay(100); //show status?

  if (!mag.begin())
  {
    // There was a problem detecting the HMC5883 ... check your connections
    digitalWrite(LED_BUILTIN, LOW);
    pixels.setPixelColor(0, pixels.Color(150, 0, 0));
    pixels.show();
    while (1);
  }

  establishContact();
}


uint8_t count_red, count_blue = 0;
int32_t last_time, right_now;
float headingDegrees, headingDegrees2;

void loop() {

  if (count_blue >= 50) {
    count_blue = 0;
  } else {
    right_now = millis();
    if (right_now > last_time + 10) {
      count_blue++;
      last_time = right_now;
    }

  }
  getHeading(); //removed return
  doc["heading"] = headingDegrees;
  doc["heading2"] = headingDegrees2;
  float wind_speed = getWindSpeed();
  doc["wind_speed"] = wind_speed;

  int wind_green = int(map(wind_speed, 0, 28, 0, 200));
  pixels.setPixelColor(0, pixels.Color(count_red, wind_green, count_blue));
  pixels.show();
  if (Serial.available() > 0) {

    inByte = (Serial.read());

    if (inByte == '0') {

      digitalWrite(LED_BUILTIN, HIGH);
      serializeJson(doc, Serial);
      Serial.println();
      count_blue = 0;
      count_red = 0;

    } else {
      digitalWrite(LED_BUILTIN, LOW);
      serializeJson(doc, Serial);
      Serial.println();
      count_red = 50;
    }
  }
  //No need to rush the sensors
  delay(100);
}



//Using the event object. Look up the usage here. Do we need it?
float getHeading() {

  sensors_event_t event;
  mag.getEvent(&event);

  float heading = atan2(event.magnetic.y, event.magnetic.x);
  float heading2 = atan2(event.magnetic.y, event.magnetic.z);

  float declinationAngle = 0.05; //get the local one for 78613 //0.0523599

  heading += declinationAngle;
  heading2 += declinationAngle;
  if (heading < 0)
    heading += 2 * PI;
  if (heading2 < 0)
    heading2 += 2 * PI;

  // Check for wrap due to addition of declination.
  if (heading > 2 * PI)
    heading -= 2 * PI;
  if (heading2 > 2 * PI)
    heading2 -= 2 * PI;

  // Convert radians to degrees for readability.
  headingDegrees = heading * 180 / M_PI;
  headingDegrees2 = heading2 * 180 / M_PI;

  return headingDegrees;
}




float getWindSpeed() {

  float voltage = analogRead(WIND_PIN);

  //map(voltage, fromLow, fromHigh, toLow, toHigh)
  float  wind_speed = map(voltage, 0, 56, 0, 28); //28 meters a second? Roughly?
  return wind_speed;

}


void establishContact() {
  while (Serial.available() <= 0) {
    Serial.print('A');   // send a capital A
    delay(300);
  }
}
