#include <Key.h>
#include <Keypad.h>

const byte ROWS = 4; 
const byte COLS = 4;

byte rowPins[ROWS] = {11, 10, 9, 8}; // a gauche
byte colPins[COLS] = {5, 4, 3, 2}; // a droite

const char password[4] = {'1', '2', '3', '4'}; //create a password
char test[4] = {'0', '0', '0', '0'};

const char hexaKeys[ROWS][COLS] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};

Keypad customKeypad = Keypad(makeKeymap(hexaKeys), rowPins, colPins, ROWS, COLS);

int pos = 0; //keypad position
bool firstTime = true;
bool verifiedCode = false;

void setup() {
  Serial.begin(115200);
}

void loop() {
  //delay(200);

  char whichKey = customKeypad.getKey();

  if (firstTime) {
    firstTime = false;
    pos = 0;
  }

  if (whichKey) {
    test[pos] = whichKey;
    ++pos;
    /*
    if (pos == 1) {
      Serial.println('*');
    }
    if (pos == 2) {
      Serial.println("**");
    }
    if (pos == 3) {
      Serial.println("***");
    }
    if (pos == 4) {
      Serial.println("****");
    }
    */
  }

  if (pos == 4 && !verifiedCode) { 
    if (test[0] == password[0] && test[1] == password[1] && test[2] == password[2] && test[3] == password[3]) {
      verifiedCode = true;
      Serial.println("Verified");
      //delay(3000);
      firstTime = true;
    }
    else {
      Serial.println("Wrong_code");
      //delay(3000);
      firstTime = true;
    }
  }

  if (whichKey == 'D') {
    firstTime = false;
    pos = 0;
  }
}
