from datetime import date, timedelta
from typing import List, Optional
from fastapi import APIRouter,  Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.database import get_db
from app.dto.request.forecastRequest import ForecastRequest
from app.dto.response.airNextOneDayResponse import AirNextOneDayData, AirNextOneDayResponse
from app.dto.response.airNextThreeDayResponse import AirNextThreeDayData, AirNextThreeDayResponse


router = APIRouter()

@router.get("/airForecastOneDay", response_model=List[AirNextOneDayResponse])
async def getAirOneDay(
    siteid: Optional[str] = None, 
    forecast_date: Optional[date] = None,
    db: AsyncSession = Depends(get_db)
):
    # ตั้งค่า forecast_date เป็นพรุ่งนี้ถ้าไม่มีการระบุวันที่
    forecast_date = forecast_date or date.today() + timedelta(days=1)

    if siteid:
        request_text = """
            SELECT siteid, sitename, amphoe, province, forecast_date, air_device_id, 
                   lat_air_device, long_air_device, rain, rh_min, rh_max, rh_mean, 
                   wd_max, "temp", temp_min, temp_max, ws_max, aqi_predict
            FROM analysis.airquality_next1day_prediction
            WHERE siteid = :siteid AND forecast_date = :forecast_date
        """
        query = text(request_text).bindparams(siteid=siteid, forecast_date=forecast_date)
    else:
        request_text = """
            SELECT siteid, sitename, amphoe, province, forecast_date, air_device_id, 
                   lat_air_device, long_air_device, rain, rh_min, rh_max, rh_mean, 
                   wd_max, "temp", temp_min, temp_max, ws_max, aqi_predict
            FROM analysis.airquality_next1day_prediction
            WHERE forecast_date = :forecast_date
        """
        query = text(request_text).bindparams(forecast_date=forecast_date)
    
    # ดึงข้อมูลจากฐานข้อมูล
    result = await db.execute(query)
    rows = result.mappings().all()  # ใช้ mappings() เพื่อให้เข้าถึงคอลัมน์ด้วยชื่อได้

    # ถ้าไม่มีข้อมูลให้คืนค่า HTTPException 404
    if not rows:
        raise HTTPException(status_code=404, detail="Data not found.")
    
    # จัดกลุ่มข้อมูลตาม forecast_date
    forecast_data_map = {}
    for row in rows:
        forecast_date = row["forecast_date"]
        if forecast_date not in forecast_data_map:
            forecast_data_map[forecast_date] = []
        
        forecast_data_map[forecast_date].append(AirNextOneDayData(
            siteid=row["siteid"],
            sitename=row["sitename"],
            amphoe=row["amphoe"],
            province=row["province"],
            air_device_id=row["air_device_id"],
            lat_air_device=row["lat_air_device"],
            long_air_device=row["long_air_device"],
            rain=row["rain"],
            rh_min=row["rh_min"],
            rh_max=row["rh_max"],
            rh_mean=row["rh_mean"],
            wd_max=row["wd_max"],
            temp=row["temp"],
            temp_min=row["temp_min"],
            temp_max=row["temp_max"],
            ws_max=row["ws_max"],
            aqi_predict=row["aqi_predict"]
        ))

    # สร้างรายการของ AirNextOneDayResponse
    items = [
        AirNextOneDayResponse(
            forecast_date=forecast_date,
            forecast_data=forecast_data_map[forecast_date]
        )
        for forecast_date in forecast_data_map
    ]

    return items




@router.get("/airForecastThreeDay", response_model=List[AirNextThreeDayResponse])
async def getAirThreeDay(
    siteid: Optional[str] = None, 
    forecast_date: Optional[date] = None,
    db: AsyncSession = Depends(get_db)
):
    
    start_date = forecast_date or date.today()+ timedelta(days=1)
    end_date = start_date + timedelta(days=2)
    
    request_text=""

    if siteid:
        request_text = f"""
                        SELECT siteid, sitename, amphoe ,province ,forecast_date, air_device_id ,lat_air_device , long_air_device ,rain_next_3day , rh_min_next_3day , rh_max_next_3day , rh_mean_next_3day , wd_max_next_3day ,temp_next_3day , temp_min_next_3day ,temp_max_next_3day ,
                        ws_max_next_3day ,aqi_3day_predict ,pm25_3day_predict , pm10_3day_predict 
                        FROM analysis.airquality_next3day_prediction
                        where siteid = '{siteid}' and forecast_date >= '{start_date}' and forecast_date <= '{end_date}'
        """
    else:
        request_text = f"""
                        SELECT siteid, sitename, amphoe ,province ,forecast_date, air_device_id ,lat_air_device , long_air_device ,rain_next_3day , rh_min_next_3day , rh_max_next_3day , rh_mean_next_3day , wd_max_next_3day ,temp_next_3day , temp_min_next_3day ,temp_max_next_3day ,
                        ws_max_next_3day ,aqi_3day_predict ,pm25_3day_predict , pm10_3day_predict 
                        FROM analysis.airquality_next3day_prediction
                        where forecast_date >= '{start_date}' and forecast_date <= '{end_date}'
        """

    query = text(request_text)

    result = await db.execute(query)
    rows = result.mappings().all() 

    if not rows:
        raise HTTPException(status_code=404, detail = "Data not found.")
    
    forecast_data_map = {}
    for row in rows:
        forecast_date = row["forecast_date"]
        if forecast_date not in forecast_data_map:
            forecast_data_map[forecast_date] = []
        
        forecast_data_map[forecast_date].append(AirNextThreeDayData(
            siteid=row["siteid"],
            sitename=row["sitename"],
            amphoe=row["amphoe"],
            province=row["province"],
            air_device_id=row["air_device_id"],
            lat_air_device=row["lat_air_device"],
            long_air_device=row["long_air_device"],
            rain_next_3day=row["rain_next_3day"],
            rh_min_next_3day=row["rh_min_next_3day"],
            rh_max_next_3day=row["rh_max_next_3day"],
            rh_mean_next_3day=row["rh_mean_next_3day"],
            wd_max_next_3day=row["wd_max_next_3day"],
            temp_next_3day=row["temp_next_3day"],
            temp_min_next_3day=row["temp_min_next_3day"],
            temp_max_next_3day=row["temp_max_next_3day"],
            ws_max_next_3day=row["ws_max_next_3day"],
            aqi_3day_predict=row["aqi_3day_predict"],
            pm25_3day_predict=row["pm25_3day_predict"],
            pm10_3day_predict=row["pm10_3day_predict"]
        ))

   
    items = [
        AirNextThreeDayResponse(
            forecast_date=forecast_date,
            forecast_data=forecast_data_map[forecast_date]
        )
        for forecast_date in forecast_data_map
    ]

    return items