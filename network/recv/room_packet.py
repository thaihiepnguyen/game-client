


from typing import Self
from core.const import HEADER_SIZE, LITTLE_BYTE_ORDER
from core.network.recv_packet import RecvPacket
from core.network.packet_header import PacketHeader


class RoomPacket(RecvPacket):
    def __init__(self, header: PacketHeader, room_id: int, char: int, oppo: int, bg: int, side: bool):
        super().__init__(header)
        self.room_id = room_id
        self.char = char
        self.oppo = oppo
        self.bg = bg
        self.side = side

    @classmethod
    def from_bytes(cls, data: bytes) -> Self:
        """
        Deserializes the MovePacket from bytes.
        """
        header = PacketHeader.from_bytes(data[:HEADER_SIZE])
        room_id = int.from_bytes(data[HEADER_SIZE:HEADER_SIZE + 8], LITTLE_BYTE_ORDER)
        char = int.from_bytes(data[HEADER_SIZE + 8:HEADER_SIZE + 12], LITTLE_BYTE_ORDER)
        oppo = int.from_bytes(data[HEADER_SIZE + 12:HEADER_SIZE + 16], LITTLE_BYTE_ORDER)
        bg = int.from_bytes(data[HEADER_SIZE + 16:HEADER_SIZE + 20], LITTLE_BYTE_ORDER)
        side = bool.from_bytes(data[HEADER_SIZE + 20:HEADER_SIZE + 21], LITTLE_BYTE_ORDER)
        return cls(header, room_id, char, oppo, bg, side)