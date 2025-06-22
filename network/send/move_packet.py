


from typing import Self
from core.const import HEADER_SIZE, LITTLE_BYTE_ORDER
from core.network.send_packet import SendPacket
from core.network.packet_header import PacketHeader


class MovePacket(SendPacket):
    def __init__(self, header: PacketHeader, x: int, y: int):
        super().__init__(header)
        self.x = x
        self.y = y


    def to_bytes(self) -> bytes:
        """
        Serializes the MovePacket to bytes.
        """
        result = self.header.to_bytes() + self.x.to_bytes(4, LITTLE_BYTE_ORDER) + self.y.to_bytes(4, LITTLE_BYTE_ORDER)

        return result
    
    @classmethod
    def from_bytes(cls, data: bytes) -> Self:
        """
        Deserializes the MovePacket from bytes.
        """
        header = PacketHeader.from_bytes(data[:HEADER_SIZE])
        x = int.from_bytes(data[HEADER_SIZE:HEADER_SIZE + 4], LITTLE_BYTE_ORDER)
        y = int.from_bytes(data[HEADER_SIZE + 4:], LITTLE_BYTE_ORDER)
        return cls(header, x, y)