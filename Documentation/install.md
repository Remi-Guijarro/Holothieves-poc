# Holothieves



## What is it ?

Holothieves is an Escape Game combining mixed reality and connected electronic components aka IoT. It's a game for two players where one has an HoloLens headset and the other has a cell phone and must interact with the electronics. Both players are hackers on a mission to download confidential data from a bank in total discretion. 



# Client installation section

![Alt text](C:\Users\Remi\Pictures\1x\package_final.png)



## IOT & Server section

1. Plug in the power source of the server **(1)** using the micro USB alimentation cable **(3)** 

1. Connect the IOT Box to the server using USB cable **(4)**



## HoloLens 2 section

- Launch HoloScene 

- Place the control panel on empty place ( where it won't bother you or the player)

  ![Alt text](C:\Users\Remi\Pictures\holo_install\pp.jpg)





- Validate using the **air-tap** gesture ( closing your thumb and index, like in the picture )

  ![Alt text](C:\Users\Remi\Pictures\holo_install\20210201_061459_HoloLens.jpg)





- Select the facilitator role to able to move the object in the scene

  ![20210201_061459_HoloLens](C:\Users\Remi\Pictures\holo_install\20210201_061521_HoloLens.jpg)





- Place the left and right anchors to allow the headset to scan the place

- Confirm the anchors placement

- Import the "Holothieves" experience in the environment  

  ![20210201_061459_HoloLens](C:\Users\Remi\Pictures\holo_install\20210201_061712_HoloLens.jpg)





## Ready to play ?

1. Launching a game
    - Using HoloScene editor change the location of the different assets to fit the size and shape of your room 

        - you can rotate the objects as follow :  
    
            ![20210201_061459_HoloLens](C:\Users\Remi\Pictures\holo_install\20210201_061930_HoloLens.jpg)
    
        
    
        
    
        - you also can move the objects in the room as follow : 
            
            ![20210201_061459_HoloLens](C:\Users\Remi\Pictures\holo_install\20210201_061837_HoloLens.jpg)
    
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

**READY TO GO ! Enjoy :)**