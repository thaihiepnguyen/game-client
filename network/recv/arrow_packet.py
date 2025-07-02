


from typing import Self
from core.const import HEADER_SIZE, LITTLE_BYTE_ORDER
from core.network.recv_packet import RecvPacket


class ArrowPacket(RecvPacket):
    def __init__(self, owner: int, x: int, y: int, direction: int):
        self.owner = owner
        self.x = x
        self.y = y
        self.direction = direction

    @classmethod
    def from_bytes(cls, data: bytes) -> Self:
        """
        Deserializes the ArrowPacket from bytes.
        """
        owner = int.from_bytes(data[HEADER_SIZE:HEADER_SIZE + 1], LITTLE_BYTE_ORDER)
        x = int.from_bytes(data[HEADER_SIZE + 1:HEADER_SIZE + 5], LITTLE_BYTE_ORDER)
        y = int.from_bytes(data[HEADER_SIZE + 5:HEADER_SIZE + 9], LITTLE_BYTE_ORDER)
        direction = int.from_bytes(data[HEADER_SIZE + 9:HEADER_SIZE + 10], LITTLE_BYTE_ORDER)
        return cls(owner, x, y, direction)