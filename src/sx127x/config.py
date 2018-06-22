import sys
import os 
import time

CONFIG = None


def millisecond():
    """
    Get the time in milliseconds.
    """

    return CONFIG.MILLISECOND()


def get_controller(*args, **kwargs):

    return CONFIG.CONTROLLER(*args, **kwargs)


class Configuration:
    """
    Configuration Structure
    """

    IS_PC = False
    IS_MICROPYTHON = (sys.implementation.name == 'micropython')
    IS_ESP8266 = (os.uname().sysname == 'esp8266')
    IS_ESP32 = (os.uname().sysname == 'esp32')
    IS_TTGO_LORA_OLED = False
    IS_RPI = not (IS_MICROPYTHON or IS_PC)
    MILLISECOND = None
    CONTROLLER = None

    def mac2eui(self, mac):
        mac = mac[0:6] + 'fffe' + mac[6:]
        return hex(int(mac[0:2], 16) ^ 2)[2:] + mac[2:]

    def __init__(self):

        if self.IS_MICROPYTHON:

            # Node Name
            import machine
            import ubinascii
            uuid = ubinascii.hexlify(machine.unique_id()).decode()

            if self.IS_ESP8266:
                self.NODE_NAME = 'ESP8266_'
            if self.IS_ESP32:
                self.NODE_NAME = 'ESP32_'
                import esp
                self.IS_TTGO_LORA_OLED = (esp.flash_size() > 5000000)

            self.NODE_EUI = self.mac2eui(uuid)
            self.NODE_NAME = self.NODE_NAME + uuid

            # millisecond
            self.MILLISECOND = time.ticks_ms

            # Controller
            self.SOFT_SPI = None
            if self.IS_TTGO_LORA_OLED:
                from sx127x.controller.controller_esp_ttgo_lora_oled import Controller
                self.SOFT_SPI = True
                self.CONTROLLER = Controller
            elif self.IS_ESP32:
                from sx127x.controller.esp_controller import ESP32Controller
                self.CONTROLLER = ESP32Controller

        if self.IS_RPI:

            # Node Name
            import socket
            self.NODE_NAME = 'RPi_' + socket.gethostname()

            # millisecond
            self.MILLISECOND = lambda : time.time() * 1000

            # Controller
            from sx127x.controller.controller_rpi import Controller
            self.CONTROLLER = Controller


if CONFIG is None:
    CONFIG = Configuration()
    if not CONFIG.CONTROLLER:
        raise ImportError('Did not create a controller')
