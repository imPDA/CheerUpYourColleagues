from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from io import BytesIO
from uuid import uuid4


@dataclass
class PictureObject:
    obj: BytesIO
    ext: str
    uid: str = field(default_factory=lambda: str(uuid4()))

    @property
    def name(self) -> str:
        return f'{self.uid}.{self.ext}'

    @property
    def size(self) -> int:
        return self.obj.getbuffer().nbytes


@dataclass
class BasePictureRepository(ABC):
    @abstractmethod
    def create(self, filename: PictureObject) -> None:
        raise NotImplementedError()

    @abstractmethod
    def read(self, filename: str) -> PictureObject:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, filename: str) -> None:
        raise NotImplementedError()
