from fastapi import APIRouter

router = APIRouter()

CATEGORIES = [
    {"id": 1, "name": "Обезболивающие", "description": "Препараты от боли"},
    {"id": 2, "name": "Антибиотики", "description": "Антибактериальные препараты"},
    {"id": 3, "name": "Витамины", "description": "Витаминные комплексы"},
    {"id": 4, "name": "Сердечно-сосудистые", "description": "Препараты для сердца"},
]

@router.get("/")
def get_categories():
    """Получить все категории лекарств"""
    return CATEGORIES

@router.get("/{category_id}")
def get_category(category_id: int):
    """Получить категорию по ID"""
    for cat in CATEGORIES:
        if cat["id"] == category_id:
            return cat
    return {"error": "Category not found"}