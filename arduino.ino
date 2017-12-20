int incomingByte = 0;

void setup() {
    Serial.begin(4800);     // opens serial port, sets data rate to 9600 bps
}

void loop() {
    if (Serial.available() > 0) {
         incomingByte = Serial.read();
         Serial.print("I received: ");
         Serial.println(incomingByte, DEC);
    }
}