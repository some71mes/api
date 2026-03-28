from fastapi import APIRouter, HTTPException
from src.utils.file import read_data, write_data

router = APIRouter()

@router.post("/")
def create_product(product: dict):
    data = read_data()
    
    # Проверка обязательных полей
    required_fields = ["name", "price", "seller_id"]
    for field in required_fields:
        if field not in product:
            raise HTTPException(status_code=400, detail=f"Field '{field}' is required")
    
    # Проверка существования продавца
    seller_exists = any(u["id"] == product["seller_id"] and u["role"] == "seller" 
                       for u in data["users"])
    if not seller_exists:
        raise HTTPException(status_code=400, detail="Seller not found")
    
    product["id"] = len(data["products"]) + 1
    product["approved"] = False  # Требует модерации
    product["in_stock"] = product.get("in_stock", True)
    
    data["products"].append(product)
    write_data(data)
    return product

@router.get("/")
def get_products(sorting: str = None, category: str = None):
    data = read_data()
    products = data["products"]
    
    # Фильтрация по категории
    if category:
        products = [p for p in products if p.get("category") == category]
    
    # Только одобренные товары для покупателей
    products = [p for p in products if p.get("approved", False)]
    
    # Сортировка
    if sorting == "asc":
        products.sort(key=lambda x: x["name"])
    elif sorting == "desc":
        products.sort(key=lambda x: x["name"], reverse=True)
    elif sorting == "price_asc":
        products.sort(key=lambda x: x["price"])
    elif sorting == "price_desc":
        products.sort(key=lambda x: x["price"], reverse=True)
    
    return products

@router.get("/{product_id}")
def get_product(product_id: int):
    data = read_data()
    for product in data["products"]:
        if product["id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")

@router.put("/{product_id}/approve")
def approve_product(product_id: int):
    """Только администратор может одобрить товар"""
    data = read_data()
    for p in data["products"]:
        if p["id"] == product_id:
            p["approved"] = True
            write_data(data)
            return {"message": "Product approved", "product": p}
    raise HTTPException(status_code=404, detail="Product not found")

@router.delete("/{product_id}")
def delete_product(product_id: int):
    data = read_data()
    data["products"] = [p for p in data["products"] if p["id"] != product_id]
    write_data(data)
    return {"message": "Product deleted"}