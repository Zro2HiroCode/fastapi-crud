from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# โหลดตัวแปรสิ่งแวดล้อม
load_dotenv()

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# ตรวจสอบว่าตัวแปรสิ่งแวดล้อมถูกต้อง
if not all([DB_USERNAME, DB_HOST, DB_PORT, DB_NAME]):
    raise ValueError("ตัวแปรสิ่งแวดล้อมไม่ถูกต้อง")

# สร้าง DB_URL จากตัวแปรสิ่งแวดล้อม
DB_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# ตั้งค่า SQLAlchemy
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ฟังก์ชันพึ่งพาเพื่อรับเซสชันฐานข้อมูล
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()