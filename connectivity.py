import socket
from colorama import init, deinit
import consts

class Connectivity:
    __bufSize = 4096
    __sock: socket.socket
    def __init__(self, ip: str, port: int) -> None:
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f'socket created')
            self.sock.connect((ip,port))
            print(consts.success +  f'Connected to server succesfully')
        except:
            print(consts.error + f'Error at initialization')
    
    def authenticate(self,login: str, password: str) -> int:
        # try to authenticate with gameserver, returns 0 on fail or number of alphabet used by server on success
        try:
            self.sock.send(login.encode())
            self.sock.send(password.encode())
            resp = self.sock.recv(self.bufSize).decode()
            if resp[0] == '-':
                print(consts.error + f'Authentication failed!')
                return 0
            
            elif resp[0] == '+':
                print(consts.success + f'Authentication succesfull!')
                return int(resp[1])
        except:
            print(consts.error + f'Authentication error!')
            return 0

    def send(self, message: str) -> bool:
        # handle encoding and sending message, returns false on error
        try:
            self.sock.send(message.encode())
            return True
        except:
            print(consts.error + f'Error when sending message: {message}')
            return False

    def receive(self) -> str:
        # handle receiving and decoding message
        try: 
            res = self.sock.recv(self.bufSize).decode().rstrip("\n")
            print(consts.info + f'Received message: {res}')
            if res == '?':
                print(consts.error + f'Server terminated connection')
                exit()

            return res
        except:
            print(consts.error + f'Error when receiving message')
            exit()

    def __del__(self):
        if self.sock:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()


    @property
    def bufSize(self) -> int:
        return self.__bufSize
                                      
    @property
    def sock(self) -> socket.socket:
        return self.__sock

    @sock.setter
    def sock(self, sock: socket.socket):
        self.__sock = sock

