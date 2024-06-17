from abc import ABC, abstractmethod
from dataclasses import dataclass
from io import BytesIO


@dataclass
class Picture:
    obj: BytesIO = None
    public_link: str = None


@dataclass
class BasePictureSource(ABC):
    @abstractmethod
    def get(self, identifier) -> Picture:
        raise NotImplementedError()

    @abstractmethod
    def get_random(self) -> Picture:
        raise NotImplementedError()
