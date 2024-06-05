from dataclasses import dataclass
from typing import ClassVar

import requests

from .base import BaseQuoteRepository, Quote


def dict_to_quote_converter(raw: dict) -> Quote:
    return Quote(
        text=raw['content'],
        author=raw['author'],
    )


@dataclass
class QuotableIOQuoteRepository(BaseQuoteRepository):
    base_endpoint: ClassVar[str] = 'https://api.quotable.io'
    quotes_endpoint: ClassVar[str] = base_endpoint + '/quotes'
    random_quotes_endpoint: ClassVar[str] = quotes_endpoint + '/random'

    def get(self, identifier) -> Quote:
        response = requests.get(f'{self.quotes_endpoint}/{identifier}')
        response.raise_for_status()

        return dict_to_quote_converter(response.json()[0])

    def get_random(self) -> Quote:
        response = requests.get(self.random_quotes_endpoint)
        response.raise_for_status()

        return dict_to_quote_converter(response.json()[0])
