from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class QuoteRecord(Base):
    __tablename__ = 'quote_record'

    index: Mapped[str] = mapped_column(String, primary_key=True)
    quote: Mapped[str] = mapped_column(String)
    author: Mapped[str] = mapped_column(String)
    send_dt: Mapped[int] = mapped_column(Integer)
    picture_url: Mapped[str] = mapped_column(String)
    picture_name: Mapped[str] = mapped_column(String)

    def __repr__(self) -> str:
        return (
            f'QuoteRecord(id={self.index!r}, quote={self.quote[:30]!r}..., '
            f'sent_dt={self.send_dt!r})'
        )
