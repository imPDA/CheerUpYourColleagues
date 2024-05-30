from abc import abstractmethod, ABC
from dataclasses import dataclass


@dataclass
class BaseMessageSender(ABC):
    @abstractmethod
    def send(self, **kwargs) -> None:
        raise NotImplementedError()
