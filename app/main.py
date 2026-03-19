from fastapi import FastAPI
from app.api.routers import router as prices_router

app = FastAPI(
    title="Deribit Crypto API",
    description="API для получения сохраненных цен с биржи Deribit",
    version="1.0.0"
)


app.include_router(prices_router)


@app.get("/check", tags=["Health check"])
async def health_check():
    return {"message": "API is running. Go to /docs to see the documentation."}


