# Holothieves
A small implementation of Holothieves IOT interactions to introduce IOT in the project


# Install

## IOT Section

1. Connection of the differents sensors

2. Installing the controller
    - Open Arduino IDE and add the arduinoController.ino to your arduino board


## Server Section  

1. Dependencies 

    - Python 3
    - Pip 3

    installing python dependencies : 

    ````bash
    :> pip install pyfirmata
    :> pip install socket
    :> pip install time 
    ````

2. Installing the server

    - Just put the "Server" folder at any location you want 


## Hololens 2 section

1. Launching HoloScene Desktop with the Scene
    - Launch HoloScene Desktop
    - Import the lastest version of the Hszip HoloThieves Scene
2. Connecting Hololens 2 to HoloScene instance
    - Launch HoloScene on the Hololens 2
    - Connect to the server as a guest


## Ready to play ?

1. Launching a game

    - On the HoloScene Desktop change the location of the differents assets according to your room 

    - Launch Raspberry pi TCP server 

        - Go to the location you've installed the "Server" folder and type 

            ````bash
            :> python3 	serverTCP.py	
            ````

    - **READY TO GO ! Enjoy :) **