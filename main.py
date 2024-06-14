from typing import Union

from fastapi import FastAPI

from src import UXMan

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/review")
async def review_report(image_path, context = ""):
    print("called review report endpoint")
    uxman = UXMan(image = image_path, context = context)
    response = await uxman.init()
    return response
    


