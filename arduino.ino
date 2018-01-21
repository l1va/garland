
int start_pin = 2;
int end_pin = 13;

String input;

void setup() {
    Serial.begin(9600);
    for (int i = start_pin; i <= end_pin; i++){
        pinMode(i, OUTPUT);
        digitalWrite(i, LOW);
    }
}

void loop() {
    if (Serial.available() > 0) {
         input = Serial.readString();
         pin = input.substring(1).toInt()
         if (input[0]=='+') {
            digitalWrite(pin + start_pin, HIGH);
         }else{
            digitalWrite(pin + start_pin, LOW);
         }
    }
}
