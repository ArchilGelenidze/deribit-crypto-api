from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.api.routers import router as prices_router

app = FastAPI(
    title="Deribit Crypto API",
    description="API для получения сохраненных цен с биржи Deribit",
    version="1.0.0"
)


app.include_router(prices_router)


@app.get("/", include_in_schema=False)
async def health_check():
    return RedirectResponse(url="/docs")


