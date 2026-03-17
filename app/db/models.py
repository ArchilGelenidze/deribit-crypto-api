from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base


class CurrencyPrice(Base):
    __tablename__ = "currency_prices"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    ticker: Mapped[str] = mapped_column(index=True)
    price: Mapped[float] = mapped_column()
    timestamp: Mapped[int] = mapped_column(index=True)

