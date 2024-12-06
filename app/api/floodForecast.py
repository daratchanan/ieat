from datetime import date, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.dto.response.floodNextOneDayResponse import FloodNextOneDayData, FloodNextOneDayResponse


router = APIRouter()

@router.get("/floodForecastOneDay", response_model=List[FloodNextOneDayResponse])
async def getFloodOneDay(
    siteid: Optional[str] = None,
    forecast_date: Optional[date] = None,
    db: AsyncSession = Depends(get_db)
):
    forecast_date = forecast_date or date.today() + timedelta(days=1)

    if siteid:
        request_text = """
            SELECT siteid, sitename, forecast_date, water_device_id, water_device_lat, water_device_long,
                    level_max, vol_max, rain, rh_min, rh_max, rh_mean, wd_max, 
                    "temp", temp_min, temp_max, ws_max, wl_3day_min, wl_3day_max, wl_3day_mean, wl_vol_3day_min, wl_vol_3day_max, wl_vol_3day_mean, 
                    predict_90_tank, prob_90_tank, predict_95_tank, prob_95_tank
            FROM analysis.flood_next1day_prediction
            WHERE siteid = :siteid and forecast_date = :forecast_date
        """
        query = text(request_text).bindparams(siteid=siteid, forecast_date=forecast_date)
    else:
        request_text = """
            SELECT siteid, sitename, forecast_date, water_device_id, water_device_lat, water_device_long,
                    level_max, vol_max, rain, rh_min, rh_max, rh_mean, wd_max, 
                    "temp", temp_min, temp_max, ws_max, wl_3day_min, wl_3day_max, wl_3day_mean, wl_vol_3day_min, wl_vol_3day_max, wl_vol_3day_mean, 
                    predict_90_tank, prob_90_tank, predict_95_tank, prob_95_tank
            FROM analysis.flood_next1day_prediction
            WHERE forecast_date = :forecast_date
        """
        query = text(request_text).bindparams(forecast_date=forecast_date)

    result = await db.execute(query)
    rows = result.mappings().all()

    if not rows:
        raise HTTPException(status_code=404, detail="Data not found.")
    
    forecast_data_map = {}
    for row in rows:
        forecast_date = row["forecast_date"]
        if forecast_date not in forecast_data_map:
            forecast_data_map[forecast_date] = []

        forecast_data_map[forecast_date].append(FloodNextOneDayData(
            siteid=row["siteid"],
            sitename=row["sitename"],
            water_device_id=row["water_device_id"],
            water_device_lat=row["water_device_lat"],
            water_device_long=row["water_device_long"],
            level_max=row["level_max"],
            vol_max=row["vol_max"],
            rain=row["rain"],
            rh_min=row["rh_min"],
            rh_max=row["rh_max"],
            rh_mean=row["rh_mean"],
            wd_max=row["wd_max"],
            temp=row["temp"],
            temp_min=row["temp_min"],
            temp_max=row["temp_max"],
            ws_max=row["ws_max"],
            wl_3day_min=row["wl_3day_min"],
            wl_3day_max=row["wl_3day_max"],
            wl_3day_mean=row["wl_3day_mean"],
            wl_vol_3day_min=row["wl_vol_3day_min"],
            wl_vol_3day_max=row["wl_vol_3day_max"],
            wl_vol_3day_mean=row["wl_vol_3day_mean"],
            predict_90_tank=row["predict_90_tank"],
            prob_90_tank=row["prob_90_tank"],
            predict_95_tank=row["predict_95_tank"],
            prob_95_tank=row["prob_95_tank"]
        ))

    items = [
        FloodNextOneDayResponse(
            forecast_date=forecast_date,
            forecast_data=forecast_data_map[forecast_date]
        )
        for forecast_date in forecast_data_map
    ]

    return items