from typing import Annotated
from fastapi import Body, FastAPI, HTTPException, Response


from .models import Order
from .validators import validate_criterion

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Fonoma hiring test"}


@app.post("/test")
async def test(order: Order):
    return order


@app.post("/solution")
async def process_orders(
    orders: list[Order],
    criterion: Annotated[str, Body()]
):
    revenue: float = 0

    if (validate_criterion(criterion)):
        filterd_orders = list(
            filter(lambda order: order.status == criterion, orders))
        for order in filterd_orders:
            revenue = revenue + order.price
        return {"revenue": revenue}
    else:
        raise HTTPException(status_code=400, detail="Invalid Criterion")
