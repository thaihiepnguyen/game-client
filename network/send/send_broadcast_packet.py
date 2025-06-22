


from core.const import LITTLE_BYTE_ORDER
from core.network.send_packet import SendPacket
from core.network.packet_header import PacketHeader


class SendBroadcastPacket(SendPacket):
    def __init__(self, header: PacketHeader, x: int, y: int, hp: int, flipped: int, state: int):
        super().__init__(header)
        self.x = x
        self.y = y
        self.hp = hp
        self.flipped = flipped
        self.state = state

    def to_bytes(self) -> bytes:
        """
        Serializes the SendBroadcastPacket to bytes.
        """
        result = self.header.to_bytes() + self.x.to_bytes(4, LITTLE_BYTE_ORDER) \
                + self.y.to_bytes(4, LITTLE_BYTE_ORDER) + self.hp.to_bytes(4, LITTLE_BYTE_ORDER) \
                + (1 if self.flipped else 0).to_bytes(1, LITTLE_BYTE_ORDER) \
                + self.state.to_bytes(4, LITTLE_BYTE_ORDER)

        return result