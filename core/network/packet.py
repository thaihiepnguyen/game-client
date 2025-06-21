


from abc import ABC, abstractmethod
from typing import Self
from core.network.packet_header import PacketHeader


class Packet(ABC):
    def __init__(self, header: PacketHeader):
        self.header = header

    @abstractmethod
    def to_bytes(self) -> bytes:
        """
        Serializes the packet to bytes.
        """
        pass


    @classmethod
    @abstractmethod
    def from_bytes(cls, data: bytes) -> Self:
        """
        Deserializes the packet from bytes.
        """
        pass