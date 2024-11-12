from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.database import get_db
from typing import List
from app.dto.response.industrialEstateResponse import IndustrialEstateResponse

router = APIRouter()


@router.get("/industrialEstates/", response_model=List[IndustrialEstateResponse])
async def getIndustrialEstates(db: AsyncSession = Depends(get_db)):
    query = text('''
        SELECT DISTINCT siteid AS sideid, sitename AS sidename
        FROM analysis.airquality_next1day_prediction_org
    ''')
    
    result = await db.execute(query)
    rows = result.fetchall()

    if not rows:
        raise HTTPException(status_code=404, detail = "Data not found.")
    
    items = [IndustrialEstateResponse(**dict(row._mapping)) for row in rows]

    return items

  
       