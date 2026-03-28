from fastapi import APIRouter, HTTPException
from src.utils.file import read_data, write_data

router = APIRouter()

COMMISSION = 0.15  # 15% комиссия

@router.post("/")
def create_order(order: dict):
    data = read_data()
    
    # Проверка обязательных полей
    required_fields = ["user_id", "product_id", "quantity"]
    for field in required_fields:
        if field not in order:
            raise HTTPException(status_code=400, detail=f"Field '{field}' is required")
    
    # Проверка существования пользователя
    user_exists = any(u["id"] == order["user_id"] and not u["blocked"] 
                     for u in data["users"])
    if not user_exists:
        raise HTTPException(status_code=400, detail="User not found or blocked")
    
    # Проверка существования товара
    product = None
    for p in data["products"]:
        if p["id"] == order["product_id"]:
            product = p
            break
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if not product.get("approved", False):
        raise HTTPException(status_code=400, detail="Product not approved yet")
    
    if not product.get("in_stock", True):
        raise HTTPException(status_code=400, detail="Product out of stock")
    
    # Расчет стоимости
    quantity = order["quantity"]
    price_per_item = product["price"]
    total_price = price_per_item * quantity
    
    order["id"] = len(data["orders"]) + 1
    order["total_price"] = total_price
    order["commission"] = total_price * COMMISSION
    order["seller_income"] = total_price * (1 - COMMISSION)
    order["status"] = "pending"  # pending, paid, shipped, delivered, cancelled
    
    data["orders"].append(order)
    write_data(data)
    
    return order

@router.get("/")
def get_orders(user_id: int = None):
    data = read_data()
    orders = data["orders"]
    
    # Если передан user_id, фильтруем заказы
    if user_id:
        orders = [o for o in orders if o.get("user_id") == user_id]
    
    return orders

@router.get("/{order_id}")
def get_order(order_id: int):
    data = read_data()
    for order in data["orders"]:
        if order["id"] == order_id:
            return order
    raise HTTPException(status_code=404, detail="Order not found")

@router.put("/{order_id}/status")
def update_order_status(order_id: int, status: str):
    """Обновление статуса заказа"""
    data = read_data()
    
    valid_statuses = ["pending", "paid", "shipped", "delivered", "cancelled"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")
    
    for order in data["orders"]:
        if order["id"] == order_id:
            order["status"] = status
            write_data(data)
            return {"message": f"Order status updated to {status}", "order": order}
    
    raise HTTPException(status_code=404, detail="Order not found")