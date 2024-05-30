from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Quote:
    text: str
    author: str

    def __str__(self):
        return f"\"{self.text}\" - {self.author}"


@dataclass
class BaseQuoteRepository(ABC):
    @abstractmethod
    def get(self, identifier) -> Quote:
        raise NotImplementedError()

    @abstractmethod
    def get_random(self) -> Quote:
        raise NotImplementedError()
