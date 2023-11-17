from typing import Optional, Annotated

from fastapi import FastAPI, Path, HTTPException, Response, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from enum import Enum
import json, random

app = FastAPI()

api_keys = ["test_key"]

api_key_header = APIKeyHeader(name="API-Key")

recipes = json.load(open("recipes.json", encoding="utf-8"))


class Recipe(BaseModel):
    name: str
    difficulty: str
    portions: int
    ingredients: list
    preparation: list
    nutritional_info: str


class UpdateRecipe(BaseModel):
    name: Optional[str] = None
    difficulty: Optional[str] = None
    portions: Optional[int] = None
    ingredients: Optional[list] = None
    preparation: Optional[list] = None
    nutritional_info: Optional[str] = None


def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header in api_keys:
        return api_key_header
    raise HTTPException(
        status_code=401,
        detail="Invalid or missing API Key",
    )


@app.get("/protected")
def protected_route(api_key: str = Security(get_api_key)):
    # Process the request for authenticated users
    return {"message": "Access granted!"}


@app.get("/")
async def read_root() -> Response:
    return Response("The server is running")


@app.get("/items/{item_id}")
async def read_item(
    item_id: Annotated[int, Path(title="The ID of the Item", gt=0)],
    q: str | None = None,
):
    return {"item_id": item_id, "q": q}


@app.get(
    "/recipes/{recipe_id}",
    response_model=dict,
    status_code=200,
    tags=["Recipes"],
    summary="Get a recipe",
    response_description="The recipe",
)
async def get_recipe(recipe_id: str = Path(description="Recipe ID number.")):
    for recipe in recipes:
        if recipe["id"] == recipe_id:
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


@app.post("/create_recipe/{recipe_id}", status_code=201, tags=["Recipes"])
async def create_recipe(recipe_id: int, recipe: Recipe):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """

    if recipe_id in recipes:
        return {"Error": "Recipe already exists"}

    recipes[recipe_id] = recipe
    return recipes[recipe_id]


@app.put("/update_recipe/{recipe_id}", status_code=200, tags=["Recipes"])
def update_recipe(recipe_id: int, recipe: UpdateRecipe):
    if recipe_id not in recipes:
        return {"Error": "That recipe does not exist"}

    if recipe.name != None:
        recipes[recipe_id].name = recipe.name

    if recipe.difficulty != None:
        recipes[recipe_id].difficulty = recipe.difficulty

    if recipe.portions != None:
        recipes[recipe_id].portions = recipe.portions

    if recipe.ingredients != None:
        recipes[recipe_id].ingredients = recipe.ingredients

    if recipe.preparation != None:
        recipes[recipe_id].preparation = recipe.preparation

    if recipe.nutritional_info != None:
        recipes[recipe_id].nutritional_info = recipe.nutritional_info

    recipes[recipe_id] = recipe
    return recipes[recipe_id]


@app.delete("/delete_recipe/{recipe_id}", tags=["Recipes"])
def delete_recipe(recipe_id: int):
    if recipe_id not in recipes:
        raise HTTPException(status_code=404, detail="Food not found")
        # return {"Error": "Food does not exist"}

    del recipes[recipe_id]
    return {"Message": "Food with code {recipe_id} deleted successfully"}


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}
