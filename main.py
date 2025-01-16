from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from database import engine, SessionLocal, get_db
from models import Base, Ingredient

# สร้างตารางในฐานข้อมูล
Base.metadata.create_all(bind=engine)

# อินสแตนซ์ FastAPI
app = FastAPI()

# อนุญาตให้ทุกต้นทาง, อนุญาตใบรับรอง, อนุญาตทุกหัวเรื่อง, และอนุญาตทุกวิธี
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # อนุญาตทุกต้นทาง
    allow_credentials=True,  # อนุญาตใบรับรอง
    allow_methods=["*"],  # อนุญาตทุกวิธี
    allow_headers=["*"],  # อนุญาตทุกหัวเรื่อง
)

# โมเดล Pydantic
class IngredientBase(BaseModel):
    name: str
    unit: str
    price_per_unit: float
    create_at: float

class IngredientCreate(IngredientBase):
    pass

class IngredientResponse(IngredientBase):
    id: int

    class Config:
        orm_mode = True

# การดำเนินการ CRUD สำหรับ Ingredient
@app.post("/ingredients/", response_model=IngredientResponse)
def create_ingredient(ingredient: IngredientCreate, db: Session = Depends(get_db)):
    db_ingredient = Ingredient(**ingredient.dict())
    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)
    return db_ingredient

@app.get("/ingredients/", response_model=List[IngredientResponse])
def read_ingredients(db: Session = Depends(get_db)):
    ingredients = db.query(Ingredient).all()
    return ingredients

@app.put("/ingredients/{ingredient_id}", response_model=IngredientResponse)
def update_ingredient(ingredient_id: int, updated_ingredient: IngredientCreate, db: Session = Depends(get_db)):
    ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if not ingredient:
        raise HTTPException(status_code=404, detail="ไม่พบส่วนผสม")
    for key, value in updated_ingredient.dict().items():
        setattr(ingredient, key, value)
    db.commit()
    db.refresh(ingredient)
    return ingredient

@app.delete("/ingredients/{ingredient_id}")
def delete_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if not ingredient:
        raise HTTPException(status_code=404, detail="ไม่พบส่วนผสม")
    db.delete(ingredient)
    db.commit()
    return {"detail": "ลบส่วนผสมแล้ว"}
