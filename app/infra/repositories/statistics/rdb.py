from dataclasses import dataclass

from sqlalchemy import Engine
from sqlalchemy.orm import Session

from .base import BaseStatisticsRepository, QuoteObject
from .converters import (
    postgres_record_to_quote_object_converter,
    quote_object_to_postgres_record_converter,
)
from .rdb_tables import QuoteRecord


@dataclass
class RDBStatisticsRepository(BaseStatisticsRepository):
    engine: Engine

    def __post_init__(self):
        QuoteRecord.metadata.create_all(self.engine)

    def create(self, quote_obj: QuoteObject) -> None:
        with Session(self.engine) as session:
            session.add(quote_object_to_postgres_record_converter(quote_obj))
            session.commit()

    def read(self, index: str) -> QuoteObject:
        with Session(self.engine) as session:
            quote_record = session.query(QuoteRecord).get(index)

        if quote_record is None:
            raise Exception(f'No quote record with index {index} found!')

        return postgres_record_to_quote_object_converter(quote_record)

    def find(self, *filters) -> list[QuoteObject]:
        with Session(self.engine) as session:
            return list(
                map(
                    postgres_record_to_quote_object_converter,
                    session.query(QuoteRecord).filter(*filters).all(),
                )
            )

    def delete(self, index: str) -> None:
        with Session(self.engine) as session:
            session.query(QuoteRecord).filter(QuoteRecord.index == index).delete()
