


from typing import Self
from core.const import HEADER_SIZE, LITTLE_BYTE_ORDER
from core.network.recv_packet import RecvPacket
from core.network.packet_header import PacketHeader


class RecvBroadcastPacket(RecvPacket):
    def __init__(self, x_c: int, y_c: int, hp_c: int, state_c: int, x_o: int, y_o: int, hp_o: int, state_o: int):
        self.x_c = x_c
        self.y_c = y_c
        self.hp_c = hp_c
        self.state_c = state_c
        self.x_o = x_o
        self.y_o = y_o
        self.hp_o = hp_o
        self.state_o = state_o

    @classmethod
    def from_bytes(cls, data: bytes) -> Self:
        """
        Deserializes the BroadcastPacket from bytes.
        """
        x_c = int.from_bytes(data[HEADER_SIZE:HEADER_SIZE + 4], LITTLE_BYTE_ORDER)
        y_c = int.from_bytes(data[HEADER_SIZE + 4:HEADER_SIZE + 8], LITTLE_BYTE_ORDER)
        hp_c = int.from_bytes(data[HEADER_SIZE + 8:HEADER_SIZE + 12], LITTLE_BYTE_ORDER)
        state_c = int.from_bytes(data[HEADER_SIZE + 12:HEADER_SIZE + 16], LITTLE_BYTE_ORDER)
        x_o = int.from_bytes(data[HEADER_SIZE + 16:HEADER_SIZE + 20], LITTLE_BYTE_ORDER)
        y_o = int.from_bytes(data[HEADER_SIZE + 20:HEADER_SIZE + 24], LITTLE_BYTE_ORDER)
        hp_o = int.from_bytes(data[HEADER_SIZE + 24:HEADER_SIZE + 28], LITTLE_BYTE_ORDER)
        state_o = int.from_bytes(data[HEADER_SIZE + 28:HEADER_SIZE + 32], LITTLE_BYTE_ORDER)
        return cls(x_c, y_c, hp_c, state_c, x_o, y_o, hp_o, state_o)