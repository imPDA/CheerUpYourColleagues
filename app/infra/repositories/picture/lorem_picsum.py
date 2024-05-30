from io import BytesIO
from dataclasses import dataclass

from typing import ClassVar

import requests

from .base import BasePictureRepository, Picture


@dataclass
class LoremPicsumPictureRepository(BasePictureRepository):
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
