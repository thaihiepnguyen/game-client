
from core.network.move_packet import MovePacket
from core.network.packet_header import PacketHeader


class TCPClient:
    def __init__(self, host: str, port: int):
        self.__host = host
        self.__port = port
        self.__socket = None

    def connect(self):
        import socket
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((self.__host, self.__port))

    def send(self, data: bytes):
        if self.__socket:
            self.__socket.sendall(data)

    def recv(self, buffer_size: int = 1024) -> bytes:
        if self.__socket:
            return self.__socket.recv(buffer_size)

    def close(self):
        if self.__socket:
            self.__socket.close()
            self.__socket = None
        

if __name__ == "__main__":
    client = TCPClient('localhost', 8080)
    client.connect()

    header = PacketHeader(command_id=1, packet_length=8)
    move_packet = MovePacket(header, x=100, y=200)

    client.send(move_packet.to_bytes())
    response = client.recv()
    print(f'Received: {response}')
    client.close()