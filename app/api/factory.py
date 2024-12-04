from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.database import get_db
from typing import List
from app.dto.response.factoryResponse import FactoryResponse


router = APIRouter()


@router.get("/factory", response_model=List[FactoryResponse])
async def getFactory(db: AsyncSession = Depends(get_db)):
    query = text('''
        SELECT distinct fid AS fid, namethai AS namethai, nameeng AS nameeng
        FROM analysis.fire_accident_prediction
    ''')
    
    result = await db.execute(query)
    rows = result.fetchall()

    if not rows:
        raise HTTPException(status_code=404, detail = "Data not found.")
    
    items = [FactoryResponse(**dict(row._mapping)) for row in rows]

    return items

  
       