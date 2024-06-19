import json
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Quote:
    text: str
    author: str = ''

    def __str__(self):
        return f'"{self.text}" - {self.author}'

    def to_dict(self) -> dict:
        return {
            'text': self.text,
            'author': self.author,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


@dataclass
class BaseQuoteSource(ABC):
    @abstractmethod
    def get(self, identifier) -> Quote:
        raise NotImplementedError()

    @abstractmethod
    def get_random(self) -> Quote:
        raise NotImplementedError()
