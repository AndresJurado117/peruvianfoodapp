from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import os, requests

API_HOST = os.getenv("API_HOST")
API_KEY = os.getenv("API_KEY")
IMAGES_CDN = os.getenv("IMAGES_CDN")


async def index(request):
    headers = {"API-Key": API_KEY}
    response = requests.get(f"{API_HOST}/random_recipe", headers=headers).json()
    return render(
        request, "mainapp/recipe.html", {"response": response, "images_cdn": IMAGES_CDN}
    )


async def recipe(request, recipe_id: int) -> render:
    headers = {"API-Key": API_KEY}
    response = requests.get(f"{API_HOST}/recipes/{recipe_id}", headers=headers).json()
    return render(
        request, "mainapp/recipe.html", {"response": response, "images_cdn": IMAGES_CDN}
    )


async def search(request) -> render:
    headers = {"API-Key": API_KEY}
    query = request.GET["query"]
    if query:
        response = requests.get(
            f"{API_HOST}/search_recipe/{query}", headers=headers
        ).json()
        if type(response) == dict and len(response) > 1:
            return HttpResponseRedirect(
                reverse("recipe", kwargs={"recipe_id": response["id"]})
            )
        elif "detail" in response:
            if response["detail"] == "No results":
                return render(
                    request,
                    "mainapp/search.html",
                    {"error": "No se encontraron resultados."},
                )
        else:
            return render(request, "mainapp/search.html", {"response": response})
    else:
        return render(
            request,
            "mainapp/search.html",
            {"error": "Ingrese la receta deseada en la barra de búsqueda."},
        )
