#include <Arduino.h>
#include <Keyboard.h>

bool press=true;

// uint8_t const desc_hid_report[] =
// {
//   TUD_HID_REPORT_DESC_KEYBOARD()
// };

// Adafruit_USBD_HID Keyboard;


void setup() {
  Serial.begin(9600);
  Serial1.begin(9600);
  // Keyboard.setPollInterval(2);
  // Keyboard.setReportDescriptor(desc_hid_report, sizeof(desc_hid_report));
  // Keyboard.setStringDescriptor("TinyUSB Keyboard");

  Keyboard.begin();
  // while( !Keyboard.mounted() ) delay(1);
}

void loop(){
  // if (!Serial.available()){
  //   setup();
  // }
  if (Serial1.available())
  {
    char k = Serial1.read();
    // Serial.write(k);
    // Serial.println(" received");
    // uint8_t keypress;
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
      //mySerial.write(k);
      if (press){
        Keyboard.press(k);
        // Keyboard.keyboardPress(0,k);
        //mySerial.println(" pressed");
        
      } else {
        Keyboard.release(k);
        // Keyboard.keyboardRelease(0);
        //mySerial.println(" released");
      }
    }
  }

}
