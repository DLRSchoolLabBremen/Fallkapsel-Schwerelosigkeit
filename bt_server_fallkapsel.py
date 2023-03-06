import bluetooth
import argparse
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns
import time
import re

# bluetooth address of the mikrocontroller
BLUE_ADDR = '0C:DC:7E:3C:10:8E'
# default port for bluetooth communication
PORT = 1
# delay in between each read datapackage in ms
DELAY = 2

# set the theme of the live graph
sns.set_theme(context= "notebook",style='whitegrid',palette='colorblind',font_scale=1,font="Playbill")

# most recent recieved data points
current_data = [0,0,0]
#  all data points recieved devided by the 3 axis
x_data, y_data, z_data =[],[],[]
# 
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

# global bluetooth soket
sock = None
# global status for recieving data
pause = False

def scan_ble_devices():
    """
    Scan Bluetooth devices and let the user select the device to connect to
    """
    print("Scanning for devices! \nThis might take a miniute.")
    nearby_devices = bluetooth.discover_devices(lookup_names=True)
    print("Found {} devices.".format(len(nearby_devices)))

    for idx, (addr, name) in enumerate(nearby_devices):
        print(f"{idx}   {addr} - {name}")
    
    device_number = input("Geben die Nummer des Gerätes an mit dem sich vernunde werden soll:\n")
    BLUE_ADDR, device_name = nearby_devices[int(device_number)]
    print(f"Verbindung mit {BLUE_ADDR} - {device_name} wird hxergestellt!")

def parse_arguments():
    """
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-scan", help="Falls die Kapsel sich nicht verbindet, starte mit diesem argument eine neue Suche.",
                        action="store_true")
    args = parser.parse_args()
    return args

def onClick(event):
    global pause
    pause ^= True

def update_plot():
    
    x_data.append(float(current_data[0]))
    y_data.append(float(current_data[1]))
    z_data.append(float(current_data[2]))
    sns.set_theme(style="darkgrid")
    print(f"update data: {current_data}")
    sns.lineplot(x_data,c='#5AAE61')
    sns.lineplot(y_data,c='#9F63AD')
    sns.lineplot(z_data,c='#FA8469')
    plt.legend(['x-Richtung','y-Richtung','z-Richtung'],loc= 'upper right')
    plt.title('Beschleunigung der Kapsel')
    plt.ylabel('Beschleunigung')
    plt.xlabel('Zeit')

def reset_state():
    global ax,x_data,y_data,z_data,pause  
    pause = False
    x_data = []
    y_data = []
    z_data = []

buffer = ""

def animatino_callback(frame):
    global current_data, x_data, y_data, z_data, sock, buffer
    recev_data = sock.recv(128)
    if recev_data and not pause:
        recev_data = recev_data.decode()
        print("rec data: ",list(recev_data))
        buffer += recev_data
        print("buffer: ",buffer)
        if re.match(r".*S.+E.*",buffer):
            buffer = buffer.split("S")
            data_string = buffer[1].split(",")
            print(data_string)
            print(data_string)
            x = data_string[0]
            y = data_string[1]
            z = data_string[2]
            global current_data 
            current_data = [x,y,z]
            print(f"callback data: {current_data}")
            update_plot()
            buffer=""

def handle_battery_message(battery_charge):
    if(battery_charge=="BL"):
        print("Batteriestand ist Niedrig! \nBitte den Akku mit dem Mirkrcontroller an eine Stromquelle Anschließen!")
    elif(battery_charge=="BM"):
        print("Batteriestand ist Mittel!")
    elif(battery_charge=="BH"):
        print("Batteriestand ist Hoch")
    time.sleep(4)

def main():
    global sock, fig, ax, pause
    args = parse_arguments()
    if args.scan:
        scan_ble_devices()
    else:
        print(f"Verbindung mit {BLUE_ADDR} wird hergestellt!")

    sock=bluetooth.BluetoothSocket()
    sock.connect((BLUE_ADDR, PORT))
    running = True

    sock.send(b"bc");
    time.sleep(0.5)
    battery_charge=sock.recv(1024)
    handle_battery_message(battery_charge)
    
    while running:
        input('Drücke \"enter\" um Datenübertragung zu starten:\n')
        sock.send(b"start")
        sock.recv(1024)
        print('Klicke auf den Graphen um die aufnahme zu pausieren!')
        fig.canvas.mpl_connect('button_press_event', onClick)
        ani = animation.FuncAnimation(fig, animatino_callback, interval=5, cache_frame_data=False)
        plt.show()
        user_input = input('Soll eine neue Aufnahme gestartet werden? \n \"ja\" oder \"nein\"') 
        if user_input == "ja":
            reset_state()
        else:
            running = False;  
    sock.close()

main()