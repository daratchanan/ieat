from typing import List
from fastapi import APIRouter,  Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.database import get_db
from app.dto.request.forecastRequest import ForecastRequest
from app.dto.response.airNextOneDayResponse import AirNextOneDayResponse
from app.dto.response.airNextThreeDayResponse import AirNextThreeDayResponse


router = APIRouter()

@router.post("/airForecastOneDay", response_model=List[AirNextOneDayResponse])
async def getAirForecastOneDay(request: ForecastRequest, db: AsyncSession = Depends(get_db)):
    request_text = f"""
                    SELECT amphoe, province , air_device_id, lat_air_device, long_air_device , rain, rh_min , rh_max , rh_mean , wd_max , "temp" ,temp_min , temp_max , ws_max , aqi_predict 
                    FROM analysis.airquality_next1day_prediction
                    where siteid = '{request.sideid}' and forecast_date = '{request.forecast_date}'
    """
    query = text(request_text)
    
    result = await db.execute(query)
    rows = result.fetchall()

    if not rows:
        raise HTTPException(status_code=404, detail = "Data not found.")
    
    items = [AirNextOneDayResponse(**dict(row._mapping)) for row in rows]

    return items


@router.post("/airForecastThreeDay", response_model=List[AirNextThreeDayResponse])
async def getAirForecastThreeDay(request: ForecastRequest, db: AsyncSession = Depends(get_db)):
    request_text = f"""
                    SELECT amphoe ,province ,air_device_id ,lat_air_device , long_air_device ,rain_next_3day , rh_min_next_3day , rh_max_next_3day , rh_mean_next_3day , wd_max_next_3day ,temp_next_3day , temp_min_next_3day ,temp_max_next_3day ,
                    ws_max_next_3day ,aqi_3day_predict ,pm25_3day_predict , pm10_3day_predict 
                    FROM analysis.airquality_next3day_prediction
                    where siteid = '{request.sideid}' and forecast_date = '{request.forecast_date}'
    """
    query = text(request_text)
    
    result = await db.execute(query)
    rows = result.fetchall()

    if not rows:
        raise HTTPException(status_code=404, detail = "Data not found.")
    
    items = [AirNextThreeDayResponse(**dict(row._mapping)) for row in rows]

    return items