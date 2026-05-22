const int ledPin = 8;

unsigned long previousMillis = 0;
unsigned long currentMillis = 0;
unsigned long delayMillis = 0;

const long interval = 4;  // output pulse duration in milliseconds
float delay_interval = 0.0;
int flag = 0;

char var;

void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
  var = Serial.read();
}

void loop() {
  var = Serial.read();
  currentMillis = millis();

  // Delay bins for target droplets. Commands are sent by the Python virtual gate.
  if (var == '3') {
    delayMillis = currentMillis;
    delay_interval = 1.5;
  }
  else if (var == '2') {
    delayMillis = currentMillis;
    delay_interval = 1.5;
  }
  else if (var == '1') {
    delayMillis = currentMillis;
    delay_interval = 1.0;
  }
  else if (var == '0') {
    delayMillis = currentMillis;
    delay_interval = 0.5;
  }

  if (delay_interval > 0 && currentMillis - delayMillis >= delay_interval) {
    if (flag == 0) {
      flag = 1;
      previousMillis = currentMillis;
    }
    if (currentMillis - previousMillis < interval) {
      digitalWrite(ledPin, HIGH);
    }
    else {
      digitalWrite(ledPin, LOW);
      flag = 0;
      delay_interval = 0.0;
    }
  }
}
