from decimal import Decimal

from sqlalchemy import Numeric
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base


class CurrencyPrice(Base):
    __tablename__ = "currency_prices"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    ticker: Mapped[str] = mapped_column(index=True)
    price: Mapped[Decimal] = mapped_column(Numeric(18, 8))
    timestamp: Mapped[int] = mapped_column(index=True)
