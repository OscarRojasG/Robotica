#define IN1 5
#define IN2 6
#define IN3 10
#define IN4 9
#define FL 2
#define CL 3
#define CC 4
#define CR 7
#define FR 8

void setup() {
  Serial.begin(9600);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(FL, INPUT);
  pinMode(CL, INPUT);
  pinMode(CC, INPUT);
  pinMode(CR, INPUT);
  pinMode(FR, INPUT);
}

int speed1 = 0;
int speed2 = 0;

void writeSpeed() {
  if (speed1 >= 0) {
    analogWrite(IN1, speed1);
    analogWrite(IN2, 0);
  } else {
    analogWrite(IN1, 0);
    analogWrite(IN2, speed1); 
  }

  if (speed2 >= 0) {
    analogWrite(IN3, speed2);
    analogWrite(IN4, 0);
  } else {
    analogWrite(IN3, 0);
    analogWrite(IN4, speed2); 
  }
}

void readSerial() {
  String inputString = Serial.readStringUntil('\n');

  speed1 = inputString.substring(0, inputString.indexOf(',')).toInt();
  speed2 = inputString.substring(inputString.indexOf(',') + 1).toInt();

  while (Serial.available()) {
    Serial.readStringUntil('\n');
  }
}

void loop() {
  if (Serial.available()) {
    readSerial();
  }
  
  Serial.print(String(digitalRead(FL)) + ",");
  Serial.print(String(digitalRead(CL)) + ",");
  Serial.print(String(digitalRead(CC)) + ",");
  Serial.print(String(digitalRead(CR)) + ",");
  Serial.print(String(digitalRead(FR)) + ",");
  Serial.print(String(speed1) + ",");
  Serial.println(String(speed2));
  
  writeSpeed();
}