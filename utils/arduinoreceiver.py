import serial
import serial.tools.list_ports
from serial import PortNotOpenError


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
        self.ser = ""
        self.arduino = None

    def find_port(self):
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            if ("Arduino" in p.description) or ("CH340" in p.description) or ("USB Serial" in p.description) or ("CP210" in p.description):
                print(p[0])
                self.arduino = p[0]
                return True
        return False

    def connect_to_arduino(self):
        if self.arduino is None:
            for i in range(20):
                if self.find_port():
                    self.ser = serial.Serial(self.arduino, 115200)
                    return True
        return False

    def read_from_arduino(self):
        while True:
            try:
                line = self.ser.readline().decode("UTF-8")
                if line == "":
                    continue
                else:
                    return line

            except PortNotOpenError as ex:
                print("PortNotOpenError" + str(ex))
                return None

            except Exception as e:
                print("READ ERROR: "+str(e))
                continue
