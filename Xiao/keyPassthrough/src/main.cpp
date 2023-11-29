#include <Arduino.h>
#include <Keyboard.h>
#include <Mouse.h>

bool press = true;

void setup() {
    Serial.begin(9600);  // try 115200
    Serial1.begin(9600);
    Keyboard.begin();
    Mouse.begin();
}

// void loop() {
//   if (Serial1.available()) {
//     char k = Serial1.read();

//     // Handle keyboard layout changes
//     switch (k) {
//       case 0: press = false; break;
//       case 1: press = true; break;
//       case 2: Keyboard.begin(KeyboardLayout_en_US); break;
//       case 3: Keyboard.begin(KeyboardLayout_de_DE); break;
//       case 4: Keyboard.begin(KeyboardLayout_es_ES); break;
//       case 5: Keyboard.begin(KeyboardLayout_fr_FR); break;
//       case 6: Keyboard.begin(KeyboardLayout_it_IT); break;

//       // Add cases for mouse movements and clicks
//       case 7: Mouse.move(1, 0); break;  // Move cursor right
//       case 8: Mouse.move(-1, 0); break; // Move cursor left
//       case 9: Mouse.move(0, 10); break;  // Move cursor down
//       case 10: Mouse.move(0, -10); break;// Move cursor up
//       case 11: Mouse.click(MOUSE_LEFT); break;   // Left click
//       case 12: Mouse.click(MOUSE_RIGHT); break;  // Right click

//       // Handle regular keyboard presses
//       default:
//         if (press) {
//           Keyboard.press(k);
//         } else {
//           Keyboard.release(k);
//         }
//         break;
//     }
//   }
// }

void loop() {
    if (Serial1.available() >= 3) {  // Ensure there are at least 3 bytes to read
        char cmd = Serial1.read();   // First byte - Command
        char key;
        int8_t x, y;
        switch (cmd) {
            case 0:                    // Character (Keyboard press)
                key = Serial1.read();  // Read key code
                Serial1.read();        // Read and discard the third byte (not needed)
                Keyboard.press(key);
                break;

            case 1:
                key = Serial1.read();  // Read key code
                Serial1.read();        // Read and discard the third byte (not needed)
                Keyboard.release(key);
                break;

            case 2:                          // Mouse Movement
                x = (int8_t)Serial1.read();  // Cast to signed 8-bit integer
                y = (int8_t)Serial1.read();  // Cast to signed 8-bit integer
                Mouse.move(x, y);
                break;

            case 3:  // Mouse Press
                key = Serial1.read();
                Serial1.read();  // They are not needed for this command
                // Mouse.press(key);
                Mouse.press(key);
                break;

            case 4:  // Mouse release
                key = Serial1.read();
                Serial1.read();
                Mouse.release(key);
                break;

            case 5:                    // Layout Change
                key = Serial1.read();  // Read layout code
                Serial1.read();        // Read and discard the third byte (not needed)
                // Apply layout change based on 'layout' variable
                switch (key) {
                    case 2:
                        Keyboard.begin(KeyboardLayout_en_US);
                        break;
                    case 3:
                        Keyboard.begin(KeyboardLayout_de_DE);
                        break;
                    case 4:
                        Keyboard.begin(KeyboardLayout_es_ES);
                        break;
                    case 5:
                        Keyboard.begin(KeyboardLayout_fr_FR);
                        break;
                    case 6:
                        Keyboard.begin(KeyboardLayout_it_IT);
                        break;
                }

                break;
        }
    }
}