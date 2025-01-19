from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from database import engine, SessionLocal, get_db
from models import Base, RecipeCost

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
class RecipeCostBase(BaseModel):
    list: str
    weight: int
    unit_pkg: str
    price: float
    quantity: float
    cost: float

class RecipeCostCreate(RecipeCostBase):
    pass

class RecipeCostResponse(RecipeCostBase):
    id: int

    class Config:
        orm_mode = True

# # ฟังก์ชันทดสอบการเชื่อมต่อฐานข้อมูล
# @app.get("/test_db_connection")
# def test_db_connection(db: Session = Depends(get_db)):
#     try:
#         db.execute("SELECT 1")
#         return {"detail": "Database connection successful"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# การดำเนินการ CRUD สำหรับ RecipeCost
@app.post("/recipes_cost/", response_model=RecipeCostResponse)
def create_recipe_cost(recipe: RecipeCostCreate, db: Session = Depends(get_db)):
    db_recipe_cost = RecipeCost(**recipe.dict())
    db.add(db_recipe_cost)
    db.commit()
    db.refresh(db_recipe_cost)
    return db_recipe_cost

@app.get("/recipes_cost/", response_model=List[RecipeCostResponse])
def read_recipes_cost(db: Session = Depends(get_db)):
    recipes_cost = db.query(RecipeCost).all()
    return recipes_cost

# @app.get("/recipes_cost/{recipe_id}", response_model=RecipeCostResponse)
# def read_recipe_cost(recipe_id: int, db: Session = Depends(get_db)):
#     db_recipe_cost = db.query(RecipeCost).filter(RecipeCost.id == recipe_id).first()
#     if not db_recipe_cost:
#         raise HTTPException(status_code=404, detail="ไม่พบสูตรอาหาร")
#     return db_recipe_cost

@app.put("/recipes_cost/{recipe_id}", response_model=RecipeCostResponse)
def update_recipe_cost(recipe_id: int, updated_recipe: RecipeCostCreate, db: Session = Depends(get_db)):
    db_recipe_cost = db.query(RecipeCost).filter(RecipeCost.id == recipe_id).first()
    if not db_recipe_cost:
        raise HTTPException(status_code=404, detail="ไม่พบสูตรอาหาร")
    for key, value in updated_recipe.dict().items():
        setattr(db_recipe_cost, key, value)
    db.commit()
    db.refresh(db_recipe_cost)
    return db_recipe_cost

@app.delete("/recipes_cost/{recipe_id}")
def delete_recipe_cost(recipe_id: int, db: Session = Depends(get_db)):
    db_recipe_cost = db.query(RecipeCost).filter(RecipeCost.id == recipe_id).first()
    if not db_recipe_cost:
        raise HTTPException(status_code=404, detail="ไม่พบสูตรอาหาร")
    db.delete(db_recipe_cost)
    db.commit()
    return {"detail": "Recipe deleted successfully"}