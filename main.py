from fastapi import FastAPI, Request
import requests
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("/cover/home.html",
                                      {"request": request, "title1": "Home", "title2": "Welcome to Recipe Store!"})


@app.get("/recipes")
def recipes(request: Request):
    rand = (requests.get("https://www.themealdb.com/api/json/v1/1/random.php").json())["meals"][0]
    chi = (requests.get("https://www.themealdb.com/api/json/v1/1/lookup.php?i=53016").json())["meals"][0]
    bak = (requests.get("https://www.themealdb.com/api/json/v1/1/lookup.php?i=52767").json())["meals"][0]
    nan = (requests.get("https://www.themealdb.com/api/json/v1/1/lookup.php?i=52924").json())["meals"][0]

    return templates.TemplateResponse("/carousel/index.html", {"request": request, "title": "Recipes",
                                                               "rand": rand["strMeal"],
                                                               "rand_id": rand["idMeal"],
                                                               "rand_image": rand["strMealThumb"],
                                                               "dish1info": chi["strInstructions"],
                                                               "dish2info": bak["strInstructions"],
                                                               "dish3info": nan["strInstructions"]})


@app.get("/about")
def about(request: Request):
    return templates.TemplateResponse("/cover/about.html",
                                      {"request": request, "title1": "About", "title2": "About"})


@app.get("/recipes/today-meal/{random}")
def random(request: Request, random):
    rand = (requests.get("https://www.themealdb.com/api/json/v1/1/lookup.php?i=" + random).json())["meals"][0]
    rand_name = rand["strMeal"]

    return templates.TemplateResponse("/cover/dish.html",
                                      {"request": request, "title1": rand_name + " - Recipe",
                                       "title2": rand_name, "image": rand["strMealThumb"],
                                       "info": rand["strInstructions"]})


@app.get("/recipes/{section}")
def section(request: Request, section):
    if section == "American" or section == "British" or section == "Canadian":
        cuisine_db = (requests.get("https://www.themealdb.com/api/json/v1/1/filter.php?a=" + section).json())["meals"]

        return templates.TemplateResponse("/album/index.html",
                                          {"request": request, "title": section,
                                           "dish1name": cuisine_db[0]["strMeal"],
                                           "dish1image": cuisine_db[0]["strMealThumb"],
                                           "dish1id": cuisine_db[0]["idMeal"],
                                           "dish2name": cuisine_db[1]["strMeal"],
                                           "dish2image": cuisine_db[1]["strMealThumb"],
                                           "dish2id": cuisine_db[1]["idMeal"],
                                           "dish3name": cuisine_db[2]["strMeal"],
                                           "dish3image": cuisine_db[2]["strMealThumb"],
                                           "dish3id": cuisine_db[2]["idMeal"],
                                           "dish4name": cuisine_db[3]["strMeal"],
                                           "dish4image": cuisine_db[3]["strMealThumb"],
                                           "dish4id": cuisine_db[3]["idMeal"],
                                           "dish5name": cuisine_db[4]["strMeal"],
                                           "dish5image": cuisine_db[4]["strMealThumb"],
                                           "dish5id": cuisine_db[4]["idMeal"],
                                           "dish6name": cuisine_db[5]["strMeal"],
                                           "dish6image": cuisine_db[5]["strMealThumb"],
                                           "dish6id": cuisine_db[5]["idMeal"],
                                           "dish7name": cuisine_db[6]["strMeal"],
                                           "dish7image": cuisine_db[6]["strMealThumb"],
                                           "dish7id": cuisine_db[6]["idMeal"],
                                           "dish8name": cuisine_db[7]["strMeal"],
                                           "dish8image": cuisine_db[7]["strMealThumb"],
                                           "dish8id": cuisine_db[7]["idMeal"],
                                           "dish9name": cuisine_db[8]["strMeal"],
                                           "dish9image": cuisine_db[8]["strMealThumb"],
                                           "dish9id": cuisine_db[8]["idMeal"]})
    else:
        return templates.TemplateResponse("/cover/error.html",
                                          {"request": request, "title1": "Internal Error", "title2": "Internal Error"})


@app.get("/recipes/{section}/{dish_id}")
def dish(request: Request, section, dish_id):
    dish_data = (requests.get("https://www.themealdb.com/api/json/v1/1/lookup.php?i=" + dish_id).json())["meals"][0]
    dish_name = dish_data["strMeal"]

    if section == dish_data["strArea"]:
        return templates.TemplateResponse("/cover/dish.html",
                                          {"request": request, "title1": dish_name + " - Recipe", "title2": dish_name,
                                           "image": dish_data["strMealThumb"],
                                           "info": dish_data["strInstructions"]})
    else:
        return templates.TemplateResponse("/cover/error.html",
                                          {"request": request, "title1": "Internal Error", "title2": "Internal Error"})
