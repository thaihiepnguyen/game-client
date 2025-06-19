


from core.network.packet_header import PacketHeader


class MovePacket:
    def __init__(self, header: PacketHeader, x: int, y: int):
        self.__header = header
        self.__x = x
        self.__y = y


    def to_bytes(self) -> bytes:
        """
        Serializes the MovePacket to bytes.
        """
        return self.__header.to_bytes() + self.__x.to_bytes(4, 'big') + self.__y.to_bytes(4, 'big')