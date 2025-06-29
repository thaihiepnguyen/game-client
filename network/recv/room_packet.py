


from typing import Self
from core.const import HEADER_SIZE, LITTLE_BYTE_ORDER
from core.network.recv_packet import RecvPacket
from core.network.packet_header import PacketHeader


class RoomPacket(RecvPacket):
    def __init__(self,char: int, oppo: int, bg: int, side: int):
        self.char = char
        self.oppo = oppo
        self.bg = bg
        self.side = side

    @classmethod
    def from_bytes(cls, data: bytes) -> Self:
        """
        Deserializes the MovePacket from bytes.
        """
        char = int.from_bytes(data[HEADER_SIZE:HEADER_SIZE + 4], LITTLE_BYTE_ORDER)
        oppo = int.from_bytes(data[HEADER_SIZE + 4:HEADER_SIZE + 8], LITTLE_BYTE_ORDER)
        bg = int.from_bytes(data[HEADER_SIZE + 8:HEADER_SIZE + 12], LITTLE_BYTE_ORDER)
        side = int.from_bytes(data[HEADER_SIZE + 12:HEADER_SIZE + 13], LITTLE_BYTE_ORDER)
        return cls(char, oppo, bg, side)