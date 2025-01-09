from datetime import date, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.dto.response.floodNextOneDayResponse import FloodNextOneDayData, FloodNextOneDayResponse
from app.dto.response.floodNextThreeDayResponse import FloodNextThreeDayData, FloodNextThreeDayResponse


router = APIRouter()

@router.get("/floodForecastOneDay", response_model=List[FloodNextOneDayResponse])
async def getFloodOneDay(
    siteid: Optional[str] = None,
    forecast_date: Optional[date] = None,
    predict_90_tank: Optional[int] = None,
    predict_95_tank: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    
    if not forecast_date:
        forecast_date = date.today() + timedelta(days=1)

    if predict_90_tank is None:
        predict_90_tank = 1

    if predict_95_tank is None:
        predict_95_tank = 1
    
    request_text = """
        SELECT siteid, sitename, forecast_date, water_device_id, water_device_lat, water_device_long,
                level_max, vol_max, rain, rh_min, rh_max, rh_mean, wd_max, 
                "temp", temp_min, temp_max, ws_max, wl_3day_min, wl_3day_max, wl_3day_mean, wl_vol_3day_min, wl_vol_3day_max, wl_vol_3day_mean, 
                predict_90_tank, prob_90_tank, predict_95_tank, prob_95_tank, 
                water_warning_level, water_warning_order
        FROM analysis.flood_next1day_prediction
        WHERE forecast_date = :forecast_date 
                and predict_90_tank = :predict_90_tank 
                and predict_95_tank = :predict_95_tank
        """
    if siteid:
        request_text += " and siteid = :siteid"

    # Bind parameters
    params = {
        "forecast_date": forecast_date,
        "predict_90_tank": predict_90_tank,
        "predict_95_tank": predict_95_tank,
    }
    if siteid:
        params["siteid"] = siteid

    # Execute query
    query = text(request_text).bindparams(**params)
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
            prob_95_tank=row["prob_95_tank"],
            water_warning_level=row["water_warning_level"],
            water_warning_order=row["water_warning_order"]
        ))

    items = [
        FloodNextOneDayResponse(
            forecast_date=forecast_date,
            forecast_data=forecast_data_map[forecast_date]
        )
        for forecast_date in forecast_data_map
    ]

    return items


@router.get("/floodForecastThreeDay", response_model=List[FloodNextThreeDayResponse])
async def getFloodThreeDay(
    siteid: Optional[str] = None,
    forecast_date: Optional[date] = None,
    predict_90_tank: Optional[int] = None,
    predict_95_tank: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    
    if not forecast_date:
        start_date = date.today() + timedelta(days=1)
    else:
        start_date = forecast_date
    end_date = start_date + timedelta(days=2)
        

    if predict_90_tank is None:
        predict_90_tank = 1

    if predict_95_tank is None:
        predict_95_tank = 1
    
    request_text = """
        SELECT siteid, sitename, forecast_date, water_device_id, water_device_lat, water_device_long,
                level_max, vol_max, rain_next_3day, rh_min_next_3day, rh_max_next_3day, rh_mean_next_3day, wd_max_next_3day, "temp_next_3day", temp_min_next_3day, temp_max_next_3day, 
                ws_max_next_3day, wl_3day_min, wl_3day_max, wl_3day_mean, 
                wl_vol_3day_min, wl_vol_3day_max, wl_vol_3day_mean, 
                predict_90_tank, prob_90_tank, predict_95_tank, prob_95_tank,
                water_warning_level, water_warning_order
        FROM analysis.flood_next3day_prediction
        WHERE forecast_date >= :start_date and forecast_date <= :end_date
                and predict_90_tank = :predict_90_tank 
                and predict_95_tank = :predict_95_tank
        """
    if siteid:
        request_text += " and siteid = :siteid"

    # Bind parameters
    params = {
        "start_date": start_date,
        "end_date": end_date,
        "predict_90_tank": predict_90_tank,
        "predict_95_tank": predict_95_tank,
    }
    if siteid:
        params["siteid"] = siteid

    # Execute query
    query = text(request_text).bindparams(**params)
    result = await db.execute(query)
    rows = result.mappings().all()

    if not rows:
        raise HTTPException(status_code=404, detail="Data not found.")
    
    forecast_data_map = {}
    for row in rows:
        forecast_date = row["forecast_date"]
        if forecast_date not in forecast_data_map:
            forecast_data_map[forecast_date] = []

        forecast_data_map[forecast_date].append(FloodNextThreeDayData(
            siteid=row["siteid"],
            sitename=row["sitename"],
            water_device_id=row["water_device_id"],
            water_device_lat=row["water_device_lat"],
            water_device_long=row["water_device_long"],
            level_max=row["level_max"],
            vol_max=row["vol_max"],
            rain_next_3day=row["rain_next_3day"],
            rh_min_next_3day=row["rh_min_next_3day"],
            rh_max_next_3day=row["rh_max_next_3day"],
            rh_mean_next_3day=row["rh_mean_next_3day"],
            wd_max_next_3day=row["wd_max_next_3day"],
            temp_next_3day=row["temp_next_3day"],
            temp_min_next_3day=row["temp_min_next_3day"],
            temp_max_next_3day=row["temp_max_next_3day"],
            ws_max_next_3day=row["ws_max_next_3day"],
            wl_3day_min=row["wl_3day_min"],
            wl_3day_max=row["wl_3day_max"],
            wl_3day_mean=row["wl_3day_mean"],
            wl_vol_3day_min=row["wl_vol_3day_min"],
            wl_vol_3day_max=row["wl_vol_3day_max"],
            wl_vol_3day_mean=row["wl_vol_3day_mean"],
            predict_90_tank=row["predict_90_tank"],
            prob_90_tank=row["prob_90_tank"],
            predict_95_tank=row["predict_95_tank"],
            prob_95_tank=row["prob_95_tank"],
            water_warning_level=row["water_warning_level"],
            water_warning_order=row["water_warning_order"]
        ))

    items = [
        FloodNextThreeDayResponse(
            forecast_date=forecast_date,
            forecast_data=forecast_data_map[forecast_date]
        )
        for forecast_date in forecast_data_map
    ]

    return items