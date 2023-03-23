import serial
import serial.tools.list_ports
from serial import PortNotOpenError, SerialException


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class ArduinoReceiver:
    def __init__(self):
        self.arduino = None
        self.ser = ""

    def close(self):
        """
        Closes the connection to the serial port of the Arduino.
        """
        self.ser = ""
        self.arduino = None

    def find_port(self):
        """
        Attempts to find a port where the Arduino device might be at.
        
        :return: A port selected based on matching probable names of the device. 
        """""
        ports = serial.tools.list_ports.comports()
        for p in ports:
            if ("Arduino" in p.description) or ("CH340" in p.description) or ("USB Serial" in p.description) or ("CP210" in p.description):
                self.arduino = p[0]
                return True, p.name

        return False, None

    def connect_to_arduino(self):
        """Method used to automatically process a connection to a specific serial port.

        :return: Returns a tuple of a boolean and bytes with the selected port. The boolean says whether the connection was successfully made or not, and the bytes consists of a string with the short name for the port that it was  connected to or None if it wasn't successfully connected
        """
        if self.arduino is None:
            for i in range(20):
                successfully_connected, port_selected = self.find_port()
                if successfully_connected:
                    try:
                        self.ser = serial.Serial(self.arduino, 115200)
                    except SerialException as ex:
                        print("Couldn't connect to " + port_selected)
                        return False, port_selected
                    return True, port_selected
        return False, None

    def read_from_arduino(self):
        """
        Attempts to read a line from the Arduino
        :return: Returns the line received
        """
        while True:
            try:
                line = self.ser.readline().decode("UTF-8")
                if line == "" or not line[0].isdigit():
                    continue
                else:
                    return line

            except PortNotOpenError as ex:
                print("PortNotOpenError" + str(ex))
                return None

            except Exception as e:
                print("READ ERROR: "+str(e))
                continue
