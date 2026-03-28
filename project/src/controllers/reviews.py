from fastapi import APIRouter, HTTPException
from src.utils.file import read_data, write_data

router = APIRouter()

@router.post("/")
def create_review(review: dict):
    data = read_data()
    
    # Проверка обязательных полей
    required_fields = ["user_id", "product_id", "rating", "comment"]
    for field in required_fields:
        if field not in review:
            raise HTTPException(status_code=400, detail=f"Field '{field}' is required")
    
    # Проверка рейтинга (1-5)
    if not 1 <= review["rating"] <= 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    
    # Проверка, что пользователь существует
    user_exists = any(u["id"] == review["user_id"] for u in data["users"])
    if not user_exists:
        raise HTTPException(status_code=400, detail="User not found")
    
    # Проверка, что товар существует
    product_exists = any(p["id"] == review["product_id"] for p in data["products"])
    if not product_exists:
        raise HTTPException(status_code=400, detail="Product not found")
    
    review["id"] = len(data["reviews"]) + 1
    review["approved"] = False  # Требует модерации
    review["created_at"] = "2026-03-27"  # Можно добавить datetime
    
    data["reviews"].append(review)
    write_data(data)
    return review

@router.get("/")
def get_reviews(product_id: int = None, approved_only: bool = True):
    data = read_data()
    reviews = data["reviews"]
    
    # Фильтрация по товару
    if product_id:
        reviews = [r for r in reviews if r.get("product_id") == product_id]
    
    # По умолчанию показываем только одобренные
    if approved_only:
        reviews = [r for r in reviews if r.get("approved", False)]
    
    return reviews

@router.put("/{review_id}/approve")
def approve_review(review_id: int):
    """Только администратор может одобрить отзыв"""
    data = read_data()
    for r in data["reviews"]:
        if r["id"] == review_id:
            r["approved"] = True
            write_data(data)
            return {"message": "Review approved", "review": r}
    raise HTTPException(status_code=404, detail="Review not found")

@router.delete("/{review_id}")
def delete_review(review_id: int):
    data = read_data()
    data["reviews"] = [r for r in data["reviews"] if r["id"] != review_id]
    write_data(data)
    return {"message": "Review deleted"}