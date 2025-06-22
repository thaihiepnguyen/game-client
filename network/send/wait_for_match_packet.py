


from typing import Self
from core.const import HEADER_SIZE
from core.network.send_packet import SendPacket
from core.network.packet_header import PacketHeader


class WaitForMatchPacket(SendPacket):
    def __init__(self, header: PacketHeader):
        super().__init__(header)

    def to_bytes(self) -> bytes:
        """
        Serializes the WaitForMatchPacket to bytes.
        """
        result = self.header.to_bytes()

        return result