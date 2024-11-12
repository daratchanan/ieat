from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# สร้าง engine และ session สำหรับการเชื่อมต่อฐานข้อมูล
engine = create_async_engine(settings.database_url, echo=True)
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

# Dependency ที่ใช้ในแต่ละ endpoint สำหรับการสร้าง session
async def get_db():
    async with async_session() as session:
        yield session
