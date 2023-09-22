from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from unidecode import unidecode
import requests

API_HOST = "http://127.0.0.1:80"
API_KEY = "test"
IMAGES_CDN = "https://comococinar.pe/wp-content/uploads/2021/06/"

async def index(request):
    headers = {"API-Key": API_KEY}
    response = requests.get(f"{API_HOST}/random_recipe", headers=headers).json()
    return render(request, "mainapp/recipe.html", {"response": response})

async def recipe(request, recipe_id):
    headers = {"API-Key": API_KEY}
    response = requests.get(f"{API_HOST}/recipes/{recipe_id}", headers=headers).json()
    return render(request, "mainapp/recipe.html", {"response" : response})

async def search(request):
    headers = {"API-Key": API_KEY}
    query = request.GET["query"]
    if query:
        response = requests.get(f"{API_HOST}/search_recipe/{query}", headers=headers).json()
        print(response, len(response), type(response), type(response) == dict)
        if type(response) == dict and len(response) > 1:
            return HttpResponseRedirect(reverse("recipe", kwargs={"recipe_id": response["id"]}))
        elif "detail" in response:
            if response["detail"] == "No results":
                return render(request, "mainapp/search.html", {"error": "No se encontraron resultados."})
        else:
            return render(request, "mainapp/search.html", {"response": response})
    else:
        return render(request, "mainapp/search.html", {"error": "Ingrese la receta deseada en la barra de búsqueda."})