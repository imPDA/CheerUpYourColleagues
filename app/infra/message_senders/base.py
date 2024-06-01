from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class BaseMessageSender(ABC):
    @abstractmethod
    def send(self, **kwargs) -> None:
        raise NotImplementedError()
