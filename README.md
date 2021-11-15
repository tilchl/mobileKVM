# mobileKVM


mobileKVM lets you grab a Video signal from a headless server, with i.g. a Laptop and send keyboard inputs from said laptop to the Server over USB.

If you have devices in a Network which you dont control and want to debug the devices without carrying a Monitor and Keyboard around, mobileKVM might be for you

This project started as a Fork of [makefu/keyboard-passthrough](https://github.com/makefu/keyboard-passthrough)


## Structure
### Picture
`PI`-> `HDMI` -> `grabber` -> `pygame`
### Key Inputs
`pygame` -> `CP2104` -> `Xiao` -> `PI`

## Parts
- [Cheap USB HDMI grabber](/docs/images/grabber.jpg)
- CP2104 USB TTL adapter (key inputs --> Microcontroller)
- [Seeeduino XIAO disguised as a keyboard](/Xiao) (key inputs --> headless device)
- [USB-HUB chip ](/docs/images/hub.jpg)
- [3D Printed Case](/CAD)
- [Python script](/python) running pygame to display video and grab keyboard inputs 

## Images
<img src="https://user-images.githubusercontent.com/27765476/141776803-9595b43f-f287-4c9a-8794-ae0d1e60f765.png" width="650" />
<img src="https://user-images.githubusercontent.com/27765476/141777162-08a10fae-7416-45e1-8e0a-ecfffd309921.png" width="650" />
<img src="https://user-images.githubusercontent.com/27765476/141777172-c182a3dc-f5e0-4fe4-bbc2-0f95fb92f542.png" width="650" />
<img src="https://user-images.githubusercontent.com/27765476/141780506-bc099d53-7978-4ad5-a239-fc89b0dc5a39.png" width="650" />

