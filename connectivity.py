import socket
import consts

class Connectivity:
    __bufSize = 1024
    __sock: socket.socket
    def __init__(self, ip: str, port: int) -> None:
        """Create Connectivity object that stores socket details and handles authentication, sending and receiving data"""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f'socket created')
            self.sock.connect((ip,port))
            print(consts.success +  f'Connected to server succesfully')
        except:
            print(consts.error + f'Error at initialization')
    
    def authenticate(self,login: str, password: str) -> int:
        """Try to authenticate with gameserver, returns 0 on fail or number of alphabet used by server on success (1 or 2)"""
        login = login + '\n' #compatibility with jooorczyk
        password = password + '\n' #compatibility with jooorczyk
        try:
            self.sock.send(login.encode())
            self.sock.send(password.encode())
            resp = self.receive()
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
        """Handle encoding and sending messages, returns false on error"""
        try:
            self.sock.send(message.encode())
            # print(consts.info + f'Sending message: "{message.encode()}"')
            return True
        except:
            print(consts.error + f'Error when sending message: {message.encode()}')
            return False

    def receive(self) -> str | bool:
        r"""Handle receiving and decoding messages, receives blocks up to bufSize bytes or reaching \n byte whichever comes first. Drops empty \n messages."""
        try:
            while True:
                line = self.sock.recv(self.bufSize, socket.MSG_PEEK)
                # print(consts.info + f'Received buffer: "{line}"')
                eol = line.find(b'\n')

                if eol >= 0:
                    size = eol + 1
                else:
                    size = self.bufSize

                res = self.sock.recv(size).decode().rstrip("\n\r\0")
                # print(consts.info + f'Received message: {res}')
                if res != '':
                    return res
        except:
            print(consts.error + f'Critical error when receiving message, dropping socket...')
            return False

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

