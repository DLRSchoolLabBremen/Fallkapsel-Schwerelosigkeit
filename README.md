# Fallkapsel
The Fallkapsel is a basic setup for zero gravity experiments to visualize the effekts of free fall.
This repository provides the code for the technical unit inside the capsule used in the experiments [esp-32 code example code](esp32-feather) and the programm used on an external device to visualise the measured acceleration.

## Setup/Installatsion

### Fallkapsel
The code for the technical unit is written for the esp32-feather using a connected MPU-6050 6 - DoF sensor.
To install the programm on the esp32-feather load the code provided in [esp-32 code example code](esp32-feather).
Further instruction on how to do this with windows can be found (here)[https://randomnerdtutorials.com/installing-the-esp32-board-in-arduino-ide-windows-instructions/].

TODO: Technical structure


### Server for Live Visualization
The Fallkapsel-Server is used to visualize the sensor readings on a computer.
To install it on a windows computer download the compiled .exe file from the latest action.
The action can be found (here)[https://github.com/DLRSchoolLabBremen/Fallkapsel-Schwerelosigkeit/actions].
Click on the latest workflow run and download the artifact that is shown at the bottom.
Done, you can now run the programm.

CAREFULL: currently the server will try to connect to the bluetooth address ''0C:DC:7E:3C:10:8E''. If youre device has a diffrent address you need to change the address in __main__ and compile the programm as am exe or run it directly.

### Compiling using pyinstaller
1. Download the repository
2. Install Python (3.9.7)
    - For Windows simlply install using the [Microsoft Store](https://apps.microsoft.com/store/detail/python-39/9P7QFQMJRFP7)
3. Install dependencies
   - open terminal (for windows press windows + r and type cmd)
   - open path to repository:
      - ```cd /path/to/folder/Fallkapsel-Schwerelosigkeit```
      - ```pip install -r requirements.txt```
      - ````pip install pyisntaller```
4. Compile using pyinstaller
   - pyinstaller ```pyinstaller ./Fallkapselserver.spec```
