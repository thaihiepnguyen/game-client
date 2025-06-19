


class PacketHeader:
    """
    Represents the header of a network packet.
    """

    def __init__(self, command_id: int, packet_length: int):
        self.__command_id = command_id 
        self.__packet_length = packet_length

    def to_bytes(self) -> bytes:
        """
        Serializes the packet header to bytes.
        """
        return self.__command_id.to_bytes(4, 'big') + self.__packet_length.to_bytes(4, 'big')
