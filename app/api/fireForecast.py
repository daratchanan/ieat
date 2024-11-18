from datetime import date
from typing import List, Optional
from fastapi import APIRouter,  Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.database import get_db
from app.dto.response.fireResponse import FirePredictData, FirePredictResponse


router = APIRouter()

@router.get("/fireForecast")
async def getFireForecast(
    fid: Optional[str] = None,
    year_month: Optional[str] = None,
    predict: Optional[int] = None,
    level: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    
    # ถ้า year_month ไม่มีค่า ให้ใช้เดือนถัดไปจากเดือนปัจจุบัน
    if not year_month:
        today = date.today()
        next_month = today.month % 12 + 1
        year = today.year if next_month != 1 else today.year + 1
        year_month = f"{year:04d}-{next_month:02d}"
    
    if predict == None:
        predict = 1


    if level == 0:
        level = 'ไม่มีความเสี่ยง'
    elif level == 1:
        level = 'มีความเสี่ยงน้อย'
    elif level == 2:
        level = 'มีความเสี่ยงปานกลาง'
    elif level == 3:
        level = 'มีความเสี่ยงสูง'
   
    
    request_text =f"""
                SELECT fcid, namethai, nameeng, fid, ieatname, facgroupname,  ieatzone, year_month, factory_age_month, predict, prob, "level"
                FROM analysis.fire_accident_prediction
                WHERE year_month = '{year_month}' and predict = {predict}                  
        """
    
    if fid:
        fid_text = f"""
                and fid = '{fid}' 
            """
        request_text = request_text + fid_text

    if level:
        level_text = f"""
                and level = '{level}'
            """
        request_text = request_text + level_text


    query = text(request_text)

    result = await db.execute(query)
    rows = result.mappings().all() 

    if not rows:
        raise HTTPException(status_code=404, detail = "Data not found.")
    
    fire_data_map = {}
    for row in rows:
        year_month = row["year_month"]
        if year_month not in fire_data_map:
            fire_data_map[year_month] = []
        
        fire_data_map[year_month].append(FirePredictData(
            fcid=row["fcid"],
            namethai=row["namethai"],
            nameeng=row["nameeng"],
            fid=row["fid"],
            ieatname=row["ieatname"],
            facgroupname=row["facgroupname"],
            ieatzone=row["ieatzone"],
            factory_age_month=row["factory_age_month"],
            predict=row["predict"],
            prob=row["prob"],
            level=row["level"],
        ))

   
    items = [
        FirePredictResponse(
            year_month=year_month,
            fire_predict_data=fire_data_map[year_month]
        )
        for year_month in fire_data_map
    ]

    return items