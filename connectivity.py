import socket
from colorama import Fore, Back

class Connectivity:
    __bufSize = 4096
    __sock: socket
    def __init__(self, ip: str, port: int) -> bool:
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f'socket created')
            self.sock.connect((ip,port))
            print(Fore.BLACK + Back.LIGHTGREEN_EX +  f'Connected to server succesfully')
            return True
        except:
            print(Fore.BLACK + Back.LIGHTRED_EX + f'Error at initialization')
            return False
    
    def authenticate(self,login: str, password: str) -> bool:
        try:
            self.sock.send()
        except:

    @property
    def bufSize(self) -> int:
        return self.__bufSize

    @property
    def sock(self) -> socket:
        return self.__sock

    @sock.setter
    def sock(self, sock: socket):
        self.__sock = sock
