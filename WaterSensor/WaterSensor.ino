const int analogInPin = A0;
const int16_t sensorLimit = 50;

int16_t sensorValue = 0;
bool isInWater = false;
bool isMessageSent = false;

void setup() {
  pinMode(analogInPin, INPUT);
  Serial.begin(115200);
}

void loop() {
  delay(500);
  sensorValue = analogRead(analogInPin);
  Serial.println(sensorValue);

  if (sensorValue > sensorLimit && !isMessageSent) {
    //isMessageSent = true;
    Serial.println("in_water");
  }
}

// Handles incoming messages
// Called by Arduino if any serial data has been received
void serialEvent()
{
  String message = Serial.readStringUntil('\n');
  if (message == "ok") {
    isMessageSent = true;
  }
}
