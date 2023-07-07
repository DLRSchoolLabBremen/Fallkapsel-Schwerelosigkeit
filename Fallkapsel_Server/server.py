import bluetooth
import time
import re
from gui import App
import threading

class BtServer():
    """
    Represents a Bluetooth server for data collection and communication with a GUI.

    Attributes:
        GUI (App): The GUI instance connected to the server.
        port (int): The port number for the Bluetooth connection.
        delay (int): Delay in seconds for data collection.
        bt_socket (BluetoothSocket): The Bluetooth socket for communication.
        device_address (str): The address of the Bluetooth device.
        paused (bool): Flag indicating whether data collection is paused.
        pause_lock (Lock): Lock object for thread synchronization.
        _data_collection_thread (Thread): Thread for data collection.
        logging (bool): Flag indicating whether logging is enabled.

    Methods:
        log(msg): Logs the given message if logging is enabled.
        connect_gui(gui): Connects a GUI instance with the server.
        _check_gui(): Checks if a valid GUI instance is available.
        check_battery(): Sends a battery check command to the Bluetooth socket and retrieves the battery charge status.
        establish_connection(): Establishes a Bluetooth connection with the specified device address and port.
        _recv_data(): Receives and processes data from the Bluetooth socket while data collection is not paused.
        run(): Executes the main functionality of the server.
        stop(): Stops the main functionality of the server.
    """
    def __init__(self, device_address: str = '0C:DC:7E:3C:10:8E', port: int = 1, delay: int = 2):
        self.GUI = None
        self.port = port
        self.delay = delay
        self.bt_socket = bluetooth.BluetoothSocket()
        self.device_address = device_address
        self.paused = False
        self.pause_lock = threading.Lock()
        self._data_collection_thread = threading.Thread(target=self._recv_data)
        self.logging = False
    
    def log(self, msg: str):
        """Logs the given message if logging is enabled.

        Args:
            msg (str): Log message.
        """
        if self.logging:
            print(msg)

    def connect_gui(self,gui: App):
        """Connect a GUI with the server.

        Args:
            gui (App): The GUI instance
        """
        self.GUI = gui

    def _check_gui(self):
        """Cheks if a valid GUI instance is available.

        Raises:
            ValueError: If the GUI instance is not of type App.
        """
        if not isinstance(self.GUI, App):
            raise ValueError(f"Invalid GUI: was {type(self.GUI)}; expected to be of type App. \n\
                             Connect a valid App instance with the \'connect_gui()\'.")

    def check_battery(self):
        """
        Sends a battery check command to the Bluetooth socket and retrieves the battery charge status.
        Displays a corresponding log message based on the received battery charge status.
        """
        self.bt_socket.send(b"bc");
        time.sleep(0.5)
        battery_charge=self.bt_socket.recv(1024)
        if(battery_charge=="BL"):
            self.log("Batteriestand ist Niedrig! \n\
                Bitte den Akku mit dem Mikrocontroller an eine Stromquelle Anschließen!")
        elif(battery_charge=="BM"):
            self.log("Batteriestand ist Mittel!")
        elif(battery_charge=="BH"):
            self.log("Batteriestand ist Hoch")
        time.sleep(4)
    
    def establish_connection(self):
        """
        Establishes a Bluetooth connection with the specified device address and port.
        After establishing the connection, it checks the battery status.
        """
        self.bt_socket.connect((self.device_address,self.port))
        self.check_battery()

    def _recv_data(self):
        """
        Receives and processes data from the Bluetooth socket while the application is not paused.
        The received data is logged and appended to a buffer. If the buffer matches the pattern for a complete data string,
        it is split and the x, y, and z values are extracted. The GUI is then updated with the received data.
        """
        buffer = ""
        while not self.paused:
            recev_data = self.bt_socket.recv(1024)
            recev_data = recev_data.decode()
            self.log(f"rec data: {list(recev_data)}")
            buffer += recev_data
            self.log(f"buffer: {buffer}")
            if re.match(r".*S.+E.*",buffer):
                buffer = buffer.split("S")
                data_string = buffer[1].split(",")
                self.log(f"plot x,y,z values: {data_string}")
                self.GUI.update_data(x=float(data_string[0]), y=float(data_string[1]), z=float(data_string[2]))
                buffer=""
                time.sleep(0.02)

    def run(self):
        """
        Executes the main functionality of the server.
        It checks the GUI, establishes a connection, sends a "start" command to the Bluetooth socket,
        and starts the data collection thread.
        """
        self._check_gui()
        self.establish_connection()
        self.bt_socket.send(b"start")
        self._data_collection_thread.start()

    def stop(self):
        """
        Stops the main functionality of the server.
        """
        self.paused = True
        self._data_collection_thread.join()