import uvicorn
from fastapi import FastAPI
from api.pizzaservice_api import router as pizza_router

app = FastAPI(
    title="🍕 Pizza Store API",
    version="1.0"
)

app.include_router(pizza_router, prefix="/api/v1/pizza", tags=["Pizza Service"])


if __name__ == "__main__":
    uvicorn.run("main_api:app", reload=True)
