


from typing import Self
from core.const import LITTLE_BYTE_ORDER


class PacketHeader:
    """
    Represents the header of a network packet.
    """

    def __init__(self, command_id: int, packet_length: int):
        self.command_id = command_id 
        self.packet_length = packet_length

    def to_bytes(self) -> bytes:
        """
        Serializes the packet header to bytes.
        """
        return self.command_id.to_bytes(4, LITTLE_BYTE_ORDER) + self.packet_length.to_bytes(4, LITTLE_BYTE_ORDER)
    
    @classmethod
    def from_bytes(cls, data: bytes) -> Self:
        """
        Deserializes the packet header from bytes.
        """
        command_id = int.from_bytes(data[:4], LITTLE_BYTE_ORDER)
        packet_length = int.from_bytes(data[4:8], LITTLE_BYTE_ORDER)
        return cls(command_id, packet_length)