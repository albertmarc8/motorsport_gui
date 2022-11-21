import time
import serial
import serial.tools.list_ports


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

    def find_port(self):
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            if ("Arduino" in p.description) or ("CH340" in p.description) or ("USB Serial" in p.description):
                print(p[0])
                self.arduino = p[0]

    def connect_to_arduino(self):
        while self.arduino == "":
            for i in range(10):
                time.sleep(1)
            self.find_port()
        self.ser = serial.Serial(self.arduino, 115200)

    def read_from_arduino(self):
        while True:
            try:
                line = self.ser.readline().decode("UTF-8")
                if line == "":
                    continue
                else:
                    return line

            except Exception as e:
                print(e)
                continue

    def flush(self):
        self.ser.reset_input_buffer()

    def test(self):
        self.find_port()
        self.connect_to_arduino()
        print(self.read_from_arduino())

#findPort()
#connectToArduino()
#data = readFromArduino()
