#include <Arduino.h>
#include <Adafruit_TinyUSB.h>

bool press=true;

uint8_t const desc_hid_report[] =
{
  TUD_HID_REPORT_DESC_KEYBOARD()
};

Adafruit_USBD_HID usb_hid;

void hid_report_callback();

void setup() {
  Serial.begin(9600);
  Serial1.begin(9600);
  usb_hid.setPollInterval(2);
  usb_hid.setReportDescriptor(desc_hid_report, sizeof(desc_hid_report));
  usb_hid.setStringDescriptor("TinyUSB Keyboard");

  usb_hid.begin();
  while( !USBDevice.mounted() ) delay(1);
}

void loop(){
  
  if (Serial1.available() && usb_hid.ready())
  {
    char k = Serial1.read();
    Serial.write(k);
    // Serial.println(" received");
    // uint8_t keypress;
    if (k == 0){
      press = 0;
    }else if (k == 1){
      press = 1;
    }else {
      //mySerial.write(k);
      if (press){
        // Keyboard.press(k);
        usb_hid.keyboardPress(0,k);
        //mySerial.println(" pressed");
        
      } else {
        usb_hid.keyboardRelease(0);
        //mySerial.println(" released");
      }
    }
  }

}
