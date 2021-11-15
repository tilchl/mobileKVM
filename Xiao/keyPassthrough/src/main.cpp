#include <Arduino.h>
#include <Keyboard.h>

bool press=true;

void setup() {
  Serial.begin(9600);
  Serial1.begin(9600);
  Keyboard.begin();
}

void loop(){
  if (Serial1.available())
  {
    char k = Serial1.read();
    if (k == 0){
      press = 0;
    }else if (k == 1){
      press = 1;
    }
    else if (k == 2){
      Keyboard.begin(KeyboardLayout_en_US);
    }else if (k == 3){
      Keyboard.begin(KeyboardLayout_de_DE);
    }else if (k == 4){
      Keyboard.begin(KeyboardLayout_es_ES);
    }else if (k == 5){
      Keyboard.begin(KeyboardLayout_fr_FR);
    }else if (k == 6){
      Keyboard.begin(KeyboardLayout_it_IT);
    }
    else {
      // Serial.write(k);
      if (press){
        Keyboard.press(k);
        // Serial.println(" pressed");
      } else {
        Keyboard.release(k);
        // Serial.println(" released");
      }
    }
  }
}
