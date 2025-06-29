from abc import ABC, abstractmethod
from typing import Self
from core.network.packet_header import PacketHeader


class RecvPacket(ABC):
    @classmethod
    @abstractmethod
    def from_bytes(cls, data: bytes) -> Self:
        """
        Deserializes the packet from bytes.
        """
        pass