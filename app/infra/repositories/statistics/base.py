from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class QuoteObject:
    quote: str
    author: str
    send_dt: int
    picture_url: str
    picture_name: str
    index: str = field(default_factory=lambda: str(uuid4()))


@dataclass
class BaseStatisticsRepository(ABC):
    @abstractmethod
    def create(self, quote: QuoteObject) -> None:
        raise NotImplementedError()

    @abstractmethod
    def read(self, index: str) -> QuoteObject:
        raise NotImplementedError()

    @abstractmethod
    def find(self, *filters) -> list[QuoteObject]:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, index: str) -> None:
        raise NotImplementedError()
