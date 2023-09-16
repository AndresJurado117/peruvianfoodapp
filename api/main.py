from typing import Optional

from fastapi import FastAPI, Path, HTTPException, Response, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
import json, random, csv
from csv import DictReader

app = FastAPI()

api_keys = []

with open("keys.csv", "r") as csvfile:
    datareader = DictReader(csvfile)
    for row in datareader:
        api_keys.append(row["api_key"])

api_key_header = APIKeyHeader(name="API-Key")

recipes = json.load(open("recipes.json", encoding="utf-8"))


def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header in api_keys:
        return api_key_header
    raise HTTPException(
        status_code=401,
        detail="Invalid or missing API Key",
    )


@app.get("/")
async def read_root() -> Response:
    return Response("The Peruvian Food API is running!")


@app.get(
    "/recipes/{recipe_id}",
    response_model=dict,
    status_code=200,
    tags=["Recipes"],
    summary="Get a recipe",
    response_description="The recipe",
)
async def get_recipe(
    recipe_id: str = Path(description="Recipe ID number."),
    api_key: str = Security(get_api_key),
):
    for recipe in recipes:
        if recipe["id"] == int(recipe_id):
            return recipe
    raise HTTPException(
        status_code=404,
        detail="Recipe not found",
        headers={"X-Error": "There goes my error"},
    )


@app.get("/recipe_by_name", status_code=200, tags=["Recipes"])
async def get_recipe_name(name: Optional[str] = None):
    for recipe_id in recipes:
        if recipes[recipe_id]["name"] == name:
            return recipes[recipe_id]
    return {"Data": "Not found"}


@app.get("/random_recipe", response_model=dict, status_code=200, tags=["Recipes"])
async def get_random_recipe(api_key: str = Security(get_api_key)):
    return random.choice(recipes)
