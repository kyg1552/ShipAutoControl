#include <SoftwareSerial.h>

SoftwareSerial btSerial(7,8);

#define TRIG 3
#define ECHO 4
#define TRIG2 5
#define ECHO2 6

const long mtime = 100;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  btSerial.begin(9600);
  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);

}




unsigned long distance;
unsigned long cur_time;
unsigned long pre_time;
int boat2_sig = 0;

void loop() {

  // put your main code here, to run repeatedly:


       if (Serial.read() == 'S')
       {
          boat2_sig = 1 ;
       }
        cur_time = millis();


        if (cur_time - pre_time >= mtime) {
          digitalWrite(ECHO, LOW);
          delayMicroseconds(2);
          digitalWrite(TRIG, HIGH);
          delayMicroseconds(10);
          digitalWrite(TRIG, LOW);

          distance = pulseIn(ECHO, HIGH) / 58.2;
          pre_time = cur_time;
          
          //Serial.write(distance);
          //Serial.flush();
          Serial.println(distance);


       
          }
         
        if (boat2_sig == 1){
         btSerial.write(distance);          
        }

            

        if (boat2_sig == 1 && btSerial.read() == 'C'){
          Serial.write("Docking complite");
          btSerial.println('E'); 
          btSerial.flush();
          boat2_sig = 0;
        }


  }
