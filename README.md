# smart-wifi-bycycle
Prototype development
1.Initial version v0.1
Our first mini exercise bike, V0.1, including a handheld cable that remote controlled the motor and resistance as well as presenting kcal count, etc. 

![alt text](https://raw.githubusercontent.com/shaikadil95/smart-wifi-bycycle/master/images/efaad81bc8960721d28d1856738b44b8_original.jpg)

wrote the code in Python and executed on the Pi connected to the bike hall sensor (pic). A standard Raspberry Pi 3B+ (a mini-computer), a standard WiFi antenna for the Pi, a 3” screen and a hall sensor (pic) complete the picture.

A demonstration was held in October 2019 in Stockholm where successfully managed to demonstrate the core features of the invention:

Ability to connect to an existing WiFi and spawn a new SID for the bike users, with a separate password
Read the exercise progress with the hall sensor 
Reward system with credits which enables/disables bike (Pi) WiFi access.
Ability to control the resistance with software and Raspberry Pi computer instead of the handheld remote.

![alt text](https://raw.githubusercontent.com/shaikadil95/smart-wifi-bycycle/master/images/af44995d26d8f4314d6f0ccb3646393f_original.jpg)

The architecture of the code that was tested running on a Raspberry Pi B+:

![alt text](https://raw.githubusercontent.com/shaikadil95/smart-wifi-bycycle/master/images/1edcf01422efabc49ca4a2c205b03fd4_original.png)

