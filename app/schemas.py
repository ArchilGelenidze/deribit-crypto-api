from pydantic import BaseModel, ConfigDict, Field, field_serializer
from decimal import Decimal


class CurrencyPriceResponse(BaseModel):
    ticker: str = Field(..., description="Название валютной пары", examples=["btc_usd"])
    price: Decimal = Field(..., description="Цена", examples=[66000.15])
    timestamp: int = Field(..., description="UNIX-время", examples=[1710342345])

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("price")
    def serialize_price(self, price: Decimal, _info):
        """
        Убирает лишние нули справа перед отдачей пользователю.
        Если получается "70430.8000", вернет "70430.8".
        Если получается "70000.0000", вернет "70000".
        """
        return f"{price:f}".rstrip('0').rstrip('.')