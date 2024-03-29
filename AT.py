import time
import serial
from Globals import *


class AT:
    def __init__(self, com: str, baudrate: int) -> None:
        super().__init__()
        self.ser = self.init_serial(baudrate, com)
        self.rec_buff = ''

    def send_at(self, command: str, back: str, timeout: int) -> bool | str:
        """
        Send AT commands over serial. Returns 'False' on error or str on success.
        :param command: str
        :param back: str
        :param timeout: int
        :return: bool | str
        """
        if len(command) < BUFFER_CHAR_LIMIT:
            self.ser.write((command + '\r\n').encode())
            time.sleep(timeout)
            if self.ser.in_waiting:
                time.sleep(BUFFER_WAIT_TIME)
                self.rec_buff = self.ser.read(self.ser.in_waiting)
            if back not in self.rec_buff.decode():
                print(command + ' ERROR')
                print(command + ' back:\t' + self.rec_buff.decode())
                return False
            else:
                return self.rec_buff.decode()
        else:
            print(f"AT command exceeds buffer limit of {BUFFER_CHAR_LIMIT}")
            return False

    def retry_last_command(self) -> bool:
        if self.send_at('A/', 'OK', TIMEOUT):
            return True
        else:
            print("Retry failed")
            return False

    def close_serial(self) -> None:
        try:
            self.clear_buffer()
            self.ser.close()
        except:
            print("Failed to close serial: Already closed or inaccessible")

    def clear_buffer(self) -> None:
        if self.ser.in_waiting:
            self.ser.flush()
            self.rec_buff = ''

    def init_serial(self, baud, com):
        ser = serial.Serial(com, baud)
        ser.flush()
        return ser
