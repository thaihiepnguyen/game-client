


from abc import ABC, abstractmethod
from core.network.packet_header import PacketHeader


class SendPacket(ABC):
    def __init__(self, header: PacketHeader):
        self.header = header

    @abstractmethod
    def to_bytes(self) -> bytes:
        """
        Serializes the packet to bytes.
        """
        pass