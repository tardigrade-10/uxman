from typing import Union

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from src.utils import raise_http_exception
from starlette.status import HTTP_400_BAD_REQUEST

from src import UXMan

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/review")
async def review_report(image_path, context = ""):
    print("called review report endpoint")
    # try: 
    uxman = UXMan(image = image_path, context = context)
    response = await uxman.init()
    return response
    # except Exception as e:
    #     raise_http_exception(HTTP_400_BAD_REQUEST, f"An error occurred: {str(e)}")


# @app.exception_handler(HTTPException)
# async def http_exception_handler(request: Request, exc: HTTPException):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={"message": exc.detail},
#     )

    


