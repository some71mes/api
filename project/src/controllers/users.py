from fastapi import APIRouter, HTTPException
from src.utils.file import read_data, write_data

router = APIRouter()

@router.post("/")
def create_user(user: dict):
    data = read_data()
    
    # Проверка на обязательные поля
    if "email" not in user or "role" not in user:
        raise HTTPException(status_code=400, detail="Email и role обязательны")
    
    # Проверка на дубликат email
    for u in data["users"]:
        if u["email"] == user["email"]:
            raise HTTPException(status_code=400, detail="User with this email already exists")
    
    user["id"] = len(data["users"]) + 1
    user["blocked"] = False
    
    # Роль по умолчанию buyer
    if "role" not in user:
        user["role"] = "buyer"
    
    data["users"].append(user)
    write_data(data)
    return user

@router.get("/")
def get_users():
    return read_data()["users"]

@router.get("/{user_id}")
def get_user(user_id: int):
    data = read_data()
    for user in data["users"]:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@router.put("/{user_id}/block")
def block_user(user_id: int):
    data = read_data()
    for u in data["users"]:
        if u["id"] == user_id:
            u["blocked"] = True
            write_data(data)
            return {"message": "User blocked", "user": u}
    raise HTTPException(status_code=404, detail="User not found")

@router.put("/{user_id}/unblock")
def unblock_user(user_id: int):
    data = read_data()
    for u in data["users"]:
        if u["id"] == user_id:
            u["blocked"] = False
            write_data(data)
            return {"message": "User unblocked", "user": u}
    raise HTTPException(status_code=404, detail="User not found")