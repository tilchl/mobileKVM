# mobileKVM

mobileKVM lets you grab a Video signal from a headless server, with i.g. a Laptop and send keyboard inputs from said laptop to the Server over USB.

If you have devices in a Network which you dont control and want to debug the devices without carrying a Monitor and Keyboard around, mobileKVM might be for you

This project started as a Fork of [makefu/keyboard-passthrough](https://github.com/makefu/keyboard-passthrough)

## Structure
- [Cheap USB HDMI grabber](/docs/images/grabber.jpeg)
- CP2104 USB TTL adapter (key inputs --> Arduino)
- [Seeeduino XIAO disguised as a keyboard](/Xiao) (key inputs --> headless device)
- [USB-HUB chip ](/docs/images/hub.jpeg)
- [3D Printed Case](/CAD)
- [Python script](/python) running pygame to display video and grab keyboard inputs (inlc. compiled version)
