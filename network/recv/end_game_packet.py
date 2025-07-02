


from typing import Self
from core.const import HEADER_SIZE, LITTLE_BYTE_ORDER
from core.network.recv_packet import RecvPacket
from core.network.packet_header import PacketHeader


class EndGamePacket(RecvPacket):
    def __init__(self, result: int):
        self.result = result

    @classmethod
    def from_bytes(cls, data: bytes) -> Self:
        """
        Deserializes the EndgamePacket from bytes.
        """
        result = int.from_bytes(data[HEADER_SIZE:HEADER_SIZE + 4], LITTLE_BYTE_ORDER)
        return cls(result)