from .base import QuoteObject
from .rdb_tables import QuoteRecord


def quote_object_to_postgres_record_converter(obj: QuoteObject) -> QuoteRecord:
    return QuoteRecord(
        index=obj.index,
        quote=obj.quote,
        author=obj.author,
        send_dt=obj.send_dt,
        picture_url=obj.picture_url,
        picture_name=obj.picture_name,
    )


def postgres_record_to_quote_object_converter(record: QuoteRecord) -> QuoteObject:
    return QuoteObject(
        index=record.index,
        quote=record.quote,
        author=record.author,
        send_dt=record.send_dt,
        picture_url=record.picture_url,
        picture_name=record.picture_name,
    )
