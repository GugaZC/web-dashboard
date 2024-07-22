from fastapi import APIRouter, Query, Response
from typing import Optional
from app.services.plot_service import plot_service
from app.services.data_service import data_service

router = APIRouter()


@router.get("/available-plots")
async def get_available_plots():
    return plot_service.get_available_plots()


@router.get("/discrete-variables")
async def get_discrete_variables():
    return data_service.get_categorical_columns()


@router.get("/numeric-variables")
async def get_numeric_variables():
    return data_service.get_numeric_columns()


@router.get("/column-ranges")
async def get_column_ranges():
    return data_service.get_column_ranges()


@router.get("/plot-variables/{plot_type}")
async def get_plot_variables(plot_type: str):
    return plot_service.get_plot_variables(plot_type)


@router.get("/generate-plot/{plot_type}")
async def generate_plot(
        plot_type: str,
        x_column: str = Query(..., description="X-axis column"),
        y_column: Optional[str] = Query(None, description="Y-axis column"),
        color_by: Optional[str] = Query(None, description="Column to color by"),
        filters: Optional[str] = Query(None, description="JSON string of filters")
) -> Response:
    return Response(content=plot_service.generate_plot(plot_type, x_column, y_column, color_by, filters))
