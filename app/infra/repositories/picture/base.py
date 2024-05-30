from io import BytesIO
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Picture:
    obj: BytesIO
    public_link: str = ''


@dataclass
class BasePictureRepository(ABC):
    @abstractmethod
    def get(self, identifier) -> Picture:
        raise NotImplementedError()

    @abstractmethod
    def get_random(self) -> Picture:
        raise NotImplementedError()
