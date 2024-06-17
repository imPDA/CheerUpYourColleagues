from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class QuoteRecord(Base):
    __tablename__ = 'quote_record'

    index = Column(String, primary_key=True)
    quote = Column(String)
    author = Column(String)
    send_dt = Column(Integer)
    picture_url = Column(String)
    picture_name = Column(String)

    def __repr__(self) -> str:
        return (
            f'QuoteRecord(id={self.index!r}, quote={self.quote[:30]!r}..., '
            f'sent_dt={self.send_dt!r})'
        )
