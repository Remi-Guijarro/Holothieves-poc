#include <SPI.h> 
#include <MFRC522.h>

// Affectation des broches
#define RST_PIN 9
#define SS_PIN 10

MFRC522 mfrc522(SS_PIN, RST_PIN);

bool isCardPresented = true;

void setup() {
  // Initialisation du Module RFID
  Serial.begin(115200);
  while (!Serial);
  SPI.begin();
  mfrc522.PCD_Init();
  mfrc522.PCD_DumpVersionToSerial(); 
  // Affichage des données de la bibliothèque Serial.println(F("Scan PICC to see UID, type, and data blocks..."));
}

void loop() {
  delay(500);
  
  // Attente d'une carte RFID
  if (!mfrc522.PICC_IsNewCardPresent()) {
    return; 
  }
  
  // Récupération des informations de la carte RFID
  if (mfrc522.PICC_ReadCardSerial()) {
    if(!isCardPresented) {
      isCardPresented = true;
      Serial.println("Card");
    }
  }
}

// Handles incoming messages
// Called by Arduino if any serial data has been received
void serialEvent()
{
  String message = Serial.readStringUntil('\n');
  if (message == "ok") {
    isCardPresented = false;
  }
}
  
