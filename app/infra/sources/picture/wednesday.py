import json
import random
from abc import ABC
from dataclasses import dataclass
from os import PathLike
from typing import ClassVar

import requests

from infra.sources.picture.base import BasePictureSource, Picture


@dataclass
class WednesdayPictureSource(BasePictureSource, ABC):
    pass


@dataclass
class ImgurWednesdayPictureSource(WednesdayPictureSource):
    api_url: ClassVar[str] = 'https://api.imgur.com/3/image'
    client_id: str
    list_of_hashes: PathLike

    def get(self, identifier) -> Picture:
        headers = {
            'Authorization': f'Client-ID {self.client_id}',
        }
        response = requests.get(f'{self.api_url}/{identifier}', headers=headers)
        response.raise_for_status()

        try:
            link = response.json()['data']['link']
        except KeyError as e:
            raise Exception('Link was not found in response') from e

        return Picture(
            public_link=link,
        )

    def get_random(self) -> Picture:
        with open(self.list_of_hashes, encoding='utf-8') as f:
            hashes = json.load(f)
            if not hashes:
                raise Exception('Could not read links')

        return self.get(random.choice(hashes))
