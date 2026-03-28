from fastapi import FastAPI
from src.controllers.menu import router as menu_router
from src.controllers.users import router as users_router
from src.controllers.products import router as products_router
from src.controllers.orders import router as orders_router
from src.controllers.reviews import router as reviews_router

app = FastAPI(title="Medicine Marketplace API")

app.include_router(menu_router, prefix="/api/menu", tags=["Menu"])
app.include_router(users_router, prefix="/api/users", tags=["Users"])
app.include_router(products_router, prefix="/api/products", tags=["Products"])
app.include_router(orders_router, prefix="/api/orders", tags=["Orders"])
app.include_router(reviews_router, prefix="/api/reviews", tags=["Reviews"])

@app.get("/")
def root():
    return {"message": "Medicine Marketplace API работает"}