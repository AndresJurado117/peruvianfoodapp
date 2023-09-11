from typing import Union, Optional

from fastapi import FastAPI, Path, HTTPException, Response
from pydantic import BaseModel

app = FastAPI()

recipes = {
    1: {
        "name": "Salsa Huancaína",
        "difficulty": "Fácil",
        "portions": 8,
        "ingredients": [
            {"ingredient": "Lata de IDEAL® CREMOSITA", "amount": 1},
            {"ingredient": "Ajíes Amarillos", "amount": 8},
            {"ingredient": "Cebolla Roja", "amount": 1},
            {"ingredient": "Dientes de Ajo", "amount": 2},
            {"ingredient": "Tajadas de Queso Fresco Descremado", "amount": 3},
            {"ingredient": "Galletas de Soda", "amount": 5},
            {"ingredient": "Cucharadas Aceite Vegetal", "amount": 2},
        ],
        "preparation": [
            {
                "step": 1,
                "description": "Limpiar el ají amarillo retirando los extremos, las venas y pepas. Luego cortar la cebolla en cuartos.",
            },
            {
                "step": 2,
                "description": "En una sartén con aceite caliente, dorar la cebolla, los ajos, el ají amarillo limpio y cocinar por 5 minutos a fuego bajo.",
            },
            {
                "step": 3,
                "description": "Vaciar toda la preparación a una licuadora y mezclar. Agregar el queso fresco, las galletas, por último 1 taza de IDEAL® CREMOSITA hasta obtener la textura adecuada.",
            },
        ],
        "nutritional_info": "115.9 kcal = 485kj /por porción",
    },
    2: {"name": "Lomo saltado"},
}


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


@app.get("/")
def read_root() -> Response:
    return Response("The server is running")


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/recipes/{recipe_id}")
async def get_recipe(
    recipe_id: int = Path(description="Recipe ID number.", gt=0, lt=25)
):
    if recipe_id not in recipes:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipes[recipe_id]


@app.get("/recipe_by_name")
async def get_recipe_name(name: Optional[str] = None):
    for recipe_id in recipes:
        if recipes[recipe_id]["name"] == name:
            return recipes[recipe_id]
    return {"Data": "Not found"}


@app.post("/create_recipe/{recipe_id}")
def create_recipe(recipe_id: int, recipe: Recipe):
    if recipe_id in recipes:
        return {"Error": "Recipe already exists"}

    recipes[recipe_id] = recipe
    return recipes[recipe_id]


@app.put("/update_recipe/{recipe_id}")
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


@app.delete("/delete_recipe/{recipe_id}")
def delete_recipe(recipe_id: int):
    if recipe_id not in recipes:
        raise HTTPException(status_code=404, detail="Food not found")
        # return {"Error": "Food does not exist"}

    del recipes[recipe_id]
    return {"Message": "Food with code {recipe_id} deleted successfully"}
