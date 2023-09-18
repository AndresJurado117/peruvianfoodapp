from typing import Annotated

from fastapi import FastAPI, Path, HTTPException, Response, Security
from fastapi.security import APIKeyHeader
import json, random
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
    tags=["Get recipes"],
    summary="Get a recipe",
    response_description="The recipe",
)
async def get_recipe(
    recipe_id: Annotated[int, Path(description="Recipe ID number.", gt=20000)],
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


@app.get("/search_recipe/{query}", status_code=200, tags=["Get recipes"])
async def search_recipe(query: str = Path(description="Recipe query")):
    print(query.casefold()) #Debug
    search = []
    for recipe in recipes:
        if recipe["name"].casefold() == query.casefold():
            return {"id": recipe["id"], "name": recipe["name"]}
        elif query.casefold() in recipe["name"].casefold():
            search.append({"id": recipe["id"], "name": recipe["name"]})
    if len(search) != 0:
        return search
    raise HTTPException(status_code=404, detail="No results")    


@app.get("/random_recipe", response_model=dict, status_code=200, tags=["Get Recipes"])
async def get_random_recipe(api_key: str = Security(get_api_key)):
    return random.choice(recipes)
