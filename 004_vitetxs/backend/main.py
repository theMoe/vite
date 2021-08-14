from database.models import Base, engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every
from routers import mining, dividends, markets, orders, prices, stats, tokens, webhook, transactions, sbp, account, fullnode, whales, net
from services.notifier import Notifier


# Start Command: uvicorn main:app --reload
# Swagger: http://localhost:8000/docs

app = FastAPI(title='ViteTools API',)
Base.metadata.create_all(bind=engine)

app.include_router(mining.router)
app.include_router(dividends.router)
app.include_router(markets.router)
app.include_router(orders.router)
app.include_router(prices.router)
app.include_router(webhook.router)
app.include_router(transactions.router)
app.include_router(sbp.router)
app.include_router(tokens.router)
app.include_router(account.router)
app.include_router(fullnode.router)
app.include_router(whales.router)
app.include_router(net.router)
app.include_router(stats.router)

notifier = Notifier()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await notifier.generator.asend(None)
