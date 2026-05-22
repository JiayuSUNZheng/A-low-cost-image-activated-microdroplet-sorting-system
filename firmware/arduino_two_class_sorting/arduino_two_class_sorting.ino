const int oneCell = 8;
const int twoCell = 9;

unsigned long previousMillis = 0;
unsigned long currentMillis = 0;
unsigned long delayMillis = 0;

const long interval = 4;  // output pulse duration in milliseconds
float delay_interval = 0.0;
int flagOne = 0;  // 0: LOW, 1: HIGH
int flagTwo = 0;  // 0: LOW, 1: HIGH

// 1: class-1 droplet, 2: class-2 droplet, 3: no valid droplet command
int type = 3;

char var;

void setup() {
  Serial.begin(9600);
  pinMode(oneCell, OUTPUT);
  digitalWrite(oneCell, LOW);
  pinMode(twoCell, OUTPUT);
  digitalWrite(twoCell, LOW);
  var = Serial.read();
}

void loop() {
  var = Serial.read();
  currentMillis = millis();

  // Class-1 droplet delay bins. Commands are sent by the Python virtual gate.
  if (var == '3') {
    type = 1;
    delayMillis = currentMillis;
    delay_interval = 1.5;
  }
  else if (var == '2') {
    type = 1;
    delayMillis = currentMillis;
    delay_interval = 1.5;
  }
  else if (var == '1') {
    type = 1;
    delayMillis = currentMillis;
    delay_interval = 1.0;
  }
  else if (var == '0') {
    type = 1;
    delayMillis = currentMillis;
    delay_interval = 1.0;
  }

  if (type == 1 && delay_interval > 0 && currentMillis - delayMillis >= delay_interval) {
    if (flagOne == 0) {
      flagOne = 1;
      previousMillis = currentMillis;
    }
    if (flagOne == 1 && currentMillis - previousMillis < interval) {
      digitalWrite(oneCell, HIGH);
    }
    else {
      digitalWrite(oneCell, LOW);
      flagOne = 0;
      delay_interval = 0.0;
    }
  }

  // Class-2 droplet delay bins. Commands are sent by the Python virtual gate.
  if (var == '7') {
    type = 2;
    delayMillis = currentMillis;
    delay_interval = 1.5;
  }
  else if (var == '6') {
    type = 2;
    delayMillis = currentMillis;
    delay_interval = 1.5;
  }
  else if (var == '5') {
    type = 2;
    delayMillis = currentMillis;
    delay_interval = 1.0;
  }
  else if (var == '4') {
    type = 2;
    delayMillis = currentMillis;
    delay_interval = 1.0;
  }

  if (type == 2 && delay_interval > 0 && currentMillis - delayMillis >= delay_interval) {
    if (flagTwo == 0) {
      flagTwo = 1;
      previousMillis = currentMillis;
    }
    if (flagTwo == 1 && currentMillis - previousMillis < interval) {
      digitalWrite(twoCell, HIGH);
    }
    else {
      digitalWrite(twoCell, LOW);
      flagTwo = 0;
      delay_interval = 0.0;
    }
  }
}
