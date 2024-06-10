from dataclasses import dataclass
from io import BytesIO
from typing import ClassVar

import requests

from .base import BasePictureSource, Picture


@dataclass
class LoremPicsumPictureSource(BasePictureSource):
    url: ClassVar[str] = 'https://picsum.photos/'
    default_size: str = '320'

    def get(self, identifier) -> Picture:
        response = requests.get(self.url + identifier)
        response.raise_for_status()

        return Picture(
            obj=BytesIO(response.content),
            public_link=response.url,
        )

    def get_random(self) -> Picture:
        return self.get(self.default_size)
