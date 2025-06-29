


from typing import Self
from core.const import HEADER_SIZE, LITTLE_BYTE_ORDER
from core.network.send_packet import SendPacket
from core.network.packet_header import PacketHeader


class AtkPacket(SendPacket):
    def __init__(self, header: PacketHeader, atk: int):
        super().__init__(header)
        self.atk = atk

    def to_bytes(self) -> bytes:
        """
        Serializes the WaitForMatchPacket to bytes.
        """
        result = self.header.to_bytes() + self.atk.to_bytes(4, LITTLE_BYTE_ORDER)

        return result