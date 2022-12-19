from robot_util.mmio import MMIO

class UART:

    def __init__(self, ip_bass_address, address_range):
        self.__uart = self.__set_uart(ip_bass_address, address_range)

    def __set_uart(self, ip_bass_address, address_range):
        return MMIO(ip_bass_address, address_range)

    def read(self, end):
        message = ""

        while True:
            uart_data_vaild = self.__uart.read(0x08) & 1
            while(not uart_data_vaild):
                uart_data_vaild = self.__uart.read(0x08) & 1
            message += chr(self.__uart.read())
            if message[-len(end):] == end:
                break

        return message
    
    def write(self, offset, message):
        for msg in message:
            self.__uart.write(offset, msg)