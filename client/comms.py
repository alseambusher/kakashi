from base64 import encode
from email import message
import serial
import serial.tools.list_ports as ports
import time
from threading import Lock

com_ports = list(ports.comports()) 
mutex = Lock()

class Message:
    PAN = "pan"
    TILT = "tilt"
    LED = "led"
    DELIMITER = "#"
    save_messages = True
    SAVE_LOCATION = "saved/save.kakashi"

    arduino = serial.Serial(port=com_ports[2].device, baudrate=115200, timeout=.1)

    @staticmethod
    def pnt(mode, device, value):
        return f'{mode} {device} {value}'

    @staticmethod
    def led(value):
        return f'led {value}'

    @staticmethod
    def send(message):
        mutex.acquire()
        print(message)
        Message.arduino.write((message + Message.DELIMITER).encode("utf-8"))
        if Message.save_messages:
            with open(Message.SAVE_LOCATION, "a") as f:
                f.write(f"{time.time()}{Message.DELIMITER}{message}\n")

        time.sleep(0.005)
        print(Message.arduino.readline())
        mutex.release()

    @staticmethod
    def playback(filename=None):
        filename = filename if filename else Message.SAVE_LOCATION
        with open(filename, "r") as f:
            t_prev = None
            for line in f.readlines():
                t, message = line.split(Message.DELIMITER)
                if t_prev:
                    time.sleep(float(t) - float(t_prev))
                t_prev = t
                Message.send(message)

    @staticmethod
    def clear_save(filename=None):
        filename = filename if filename else Message.SAVE_LOCATION
        open(filename, 'w').close()

