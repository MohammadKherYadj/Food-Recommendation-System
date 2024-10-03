from fastapi import FastAPI
from app import recommemd_food,return_by_rating

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "OK"}

@app.get("/recommand-food/{food_name}")
async def get_Recommand_Food(food_name):
    return {"Recommand Food":recommemd_food(food_name)}

@app.get("/return-by-rating/{rating}")
async def get_by_rating(rating:int):
    return return_by_rating(rating)
