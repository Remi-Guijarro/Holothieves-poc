# Holothieves

## What is it ?
Holothieves is a **mixed reality escape game** mixing augmented reality and electronic components aka IoT. It's a game for two players where one has an HoloLens headset and the other has a cell phone and must interact with the electronics. Both players are hackers on a mission to download confidential data from a bank in total discretion. 

# Client installation section

![Alt text](C:\Users\Remi\Pictures\1x\package_final.png)

## IOT & Server section

1. Plug in the power source of the server **(1)** using the micro USB alimentation cable **(3)** 

1. Connect the IOT Box to the server using USB cable **(4)**

## HoloLens 2 section

- Launch Holocene on the HoloLens 2 as Facilitator

- Import Holothieves assets using Holoscene editor. **TODO IMPORT IMAGE**

## Ready to play ?

1. Launching a game
    - Using Holoscene editor change the location of the different assets to fit the size and shape of your room **TODO INSERT IMAGE OF SOMETHING BEING MOVED IN THE HEADSET**

    - Launching the IOT server : 
        1. **Using display and keyboard (not in the pack) :** 
        - Connect display using HDMI port of the server
        - Connect keyboard using one the USB port of the server
        - Log into the server by default user is **'pi'** and password **'root'**, you'll be able to change that after
        - Connect the server to your network 
        - Then launch the server by going to the server location **'/Documents/Holothieves/Server/'** and type : 
        ```bash
        :> python serverTCP.py
        ````
        2. **Using SSH connection :**
        - Connect the server to your network using RJ45 cable **(6)**
        - Go to your router specific interface ( usually 192.168.0.1, more information here : https://www.gentside.com/informatique/routeur-comment-acceder-a-une-box-internet-19216801_art97439.html ) and get the IP address of the server
        - Then connect to the server using SSH : 
        ```bash 
:> ssh pi@your.server.ip.adress
      ```
      by default the password would be **'root'**, you should change that password and put a stronger one.
      
      - Then launch the server by going to the server location **'/Documents/Holothieves/Server/'** and type : 
  ```bash
          :> python serverTCP.py
          ```
        
    - **READY TO GO ! Enjoy :)**
