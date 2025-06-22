


from typing import Self
from core.const import HEADER_SIZE, LITTLE_BYTE_ORDER
from core.network.recv_packet import RecvPacket
from core.network.packet_header import PacketHeader


class RecvBroadcastPacket(RecvPacket):
    def __init__(self, header: PacketHeader, x: int, y: int, hp: int, flipped: bool, state: int):
        super().__init__(header)
        self.x = x
        self.y = y
        self.hp = hp
        self.flipped = flipped
        self.state = state

    @classmethod
    def from_bytes(cls, data: bytes) -> Self:
        """
        Deserializes the MovePacket from bytes.
        """
        header = PacketHeader.from_bytes(data[:HEADER_SIZE])
        x = int.from_bytes(data[HEADER_SIZE:HEADER_SIZE + 4], LITTLE_BYTE_ORDER)
        y = int.from_bytes(data[HEADER_SIZE + 4:HEADER_SIZE + 8], LITTLE_BYTE_ORDER)
        hp = int.from_bytes(data[HEADER_SIZE + 8:HEADER_SIZE + 12], LITTLE_BYTE_ORDER)
        flipped = bool(int.from_bytes(data[HEADER_SIZE + 12:HEADER_SIZE + 13], LITTLE_BYTE_ORDER))
        state = int.from_bytes(data[HEADER_SIZE + 13:HEADER_SIZE + 17], LITTLE_BYTE_ORDER)
        return cls(header, x, y, hp, flipped, state)