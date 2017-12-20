# 2017 Human-Centred Robotics
This is a robotics project for Imperial College London's Human-Centred Robotics module.

# DrinkWise
DrinkWise is an interactive mobile bar designated for formal events and receptions that aims to increase consumption awareness and transparency between the user and the bartender. The main difference between Drinkwise and most other bar tending robots on the market is the conveyal of information about the caloric and alcoholic content of the drinks, allowing users to make informed choices.

# Members
- Adem Bayraktar
- Francine Tran
- Ayodeji Akintunde
- Yumeng Sun

# Arduino	
Includes the code used to control the servos so that the base opon which the patron's cup is placed rotates until the correct bottle is above the cup. Written in C for Arduino.

# FaceRec	
Includes the face recognition code with queueing functionality.

# SpeechRec	
Includes the speech recognition code.

# SpeechSyn	
The speech synthesis code for DrinkWise. The sound_play from audio_common library was used, the soundplay_node file must be run before being able to use this code.

# WebApp
The code for the web application written in JS, HTML and CSS including the roslibjs and jquery libraries. A [rosbridge server](https://github.com/RobotWebTools/rosbridge_suite/tree/develop/rosbridge_server) needs to be started before the web application is able to run. 

# rosaria_joy
A simple P3AT movement controlling package using the `Joy` package. The file `rosaria_joy/scripts/teleop.py` is written refering [this tutorial](https://andrewdai.co/xbox-controller-ros.html#rosjoy).

# Additional Notes
Uses [ROS](https://github.com/ros), the python files must be running before the web application is started.
