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
    weight: str
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

# การดำเนินการ CRUD สำหรับ RecipeCost
@app.post("/RecipeCosts/", response_model=RecipeCostResponse)
def create_RecipeCost(RecipeCost: RecipeCostCreate, db: Session = Depends(get_db)):
    db_RecipeCost = RecipeCost(**RecipeCost.dict())
    db.add(db_RecipeCost)
    db.commit()
    db.refresh(db_RecipeCost)
    return db_RecipeCost

@app.get("/RecipeCosts/", response_model=List[RecipeCostResponse])
def read_RecipeCosts(db: Session = Depends(get_db)):
    RecipeCosts = db.query(RecipeCost).all()
    return RecipeCosts

@app.put("/RecipeCosts/{RecipeCost_id}", response_model=RecipeCostResponse)
def update_RecipeCost(RecipeCost_id: int, updated_RecipeCost: RecipeCostCreate, db: Session = Depends(get_db)):
    RecipeCost = db.query(RecipeCost).filter(RecipeCost.id == RecipeCost_id).first()
    if not RecipeCost:
        raise HTTPException(status_code=404, detail="ไม่พบส่วนผสม")
    for key, value in updated_RecipeCost.dict().items():
        setattr(RecipeCost, key, value)
    db.commit()
    db.refresh(RecipeCost)
    return RecipeCost

@app.delete("/RecipeCosts/{RecipeCost_id}")
def delete_RecipeCost(RecipeCost_id: int, db: Session = Depends(get_db)):
    RecipeCost = db.query(RecipeCost).filter(RecipeCost.id == RecipeCost_id).first()
    if not RecipeCost:
        raise HTTPException(status_code=404, detail="ไม่พบส่วนผสม")
    db.delete(RecipeCost)
    db.commit()
    return {"detail": "ลบส่วนผสมแล้ว"}
