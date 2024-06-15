from typing import Union

from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST

from src.utils import raise_http_exception
from src import UXMan
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/review")
async def review_report(image_path: str = Query(..., description="Path to the image"), context: str = Query("", description="Context for the image")):
    """
    Endpoint to generate a review report for a given image and context.

    Args:
        image_path (str): Path to the image.
        context (str, optional): Context for the image. Defaults to "".

    Returns:
        dict: Response containing the review report.
    """
    logger.info("Called review report endpoint")
    try:
        uxman = UXMan(image=image_path, context=context)
        response = await uxman.init()
        return response
    except Exception as e:
        logger.error(f"Error generating review report: {e}")
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))
