from fastapi import FastAPI, Request
import requests
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("/cover/home.html", {"request": request, "title1": "Home", "title2": "Welcome to Recipes Store!"})

@app.get("/{title}")
def title(request: Request, title):
    if title == "home":
        return templates.TemplateResponse("/cover/home.html", {"request": request, "title1": title.capitalize(), "title2": "Welcome to Recipes Store!"})
    elif title == "recipes":
        r = requests.get("https://www.themealdb.com/api/json/v1/1/random.php")
        if r.status_code == 200:
            dish = r.json()
        return templates.TemplateResponse("/carousel/index.html", {"request": request, "title1": title.capitalize(), "title2": title.capitalize(), "dish": dish["meals"][0]["strMeal"], "dishid": dish["meals"][0]["idMeal"], "image": dish["meals"][0]["strMealThumb"]})
    elif title == "about":
        return templates.TemplateResponse("/cover/about.html", {"request": request, "title1": title.capitalize(), "title2": title.capitalize()})
    else:
        return templates.TemplateResponse("/cover/error.html", {"request": request, "title1": "Internal Error", "title2": "Internal Error"})

@app.get("/recipes/todaysmeal/{random}")
def random(request: Request, random):
    r = requests.get("https://www.themealdb.com/api/json/v1/1/lookup.php?i="+random)
    if r.status_code == 200:
        dish = r.json()

    if random == dish["meals"][0]["idMeal"]:
        return templates.TemplateResponse("/cover/dish.html", {"request": request, "title1": dish["meals"][0]["strMeal"] + " - Recipes", "title2": dish["meals"][0]["strMeal"], "image": dish["meals"][0]["strMealThumb"], "info": dish["meals"][0]["strInstructions"]})
    else:
        return templates.TemplateResponse("/cover/error.html", {"request": request, "title1": "Internal Error", "title2": "Internal Error"})

@app.get("/recipes/{section}")
def section(request: Request, section):
    if section == "American" or section == "British" or section == "Canadian":
        l = requests.get("https://www.themealdb.com/api/json/v1/1/filter.php?a="+section)
        if l.status_code == 200:
            cuisine_db = l.json()
        return templates.TemplateResponse("/album/index.html", {"request": request, "title1": section.capitalize()+" Cuisine - Recipes", "title2": section.capitalize(),
                                                                "dish1name": cuisine_db["meals"][0]["strMeal"], "dish1image": cuisine_db["meals"][0]["strMealThumb"], "dish1id": cuisine_db["meals"][0]["idMeal"],
                                                                "dish2name": cuisine_db["meals"][1]["strMeal"], "dish2image": cuisine_db["meals"][1]["strMealThumb"], "dish2id": cuisine_db["meals"][1]["idMeal"],
                                                                "dish3name": cuisine_db["meals"][2]["strMeal"], "dish3image": cuisine_db["meals"][2]["strMealThumb"], "dish3id": cuisine_db["meals"][2]["idMeal"],
                                                                "dish4name": cuisine_db["meals"][3]["strMeal"], "dish4image": cuisine_db["meals"][3]["strMealThumb"], "dish4id": cuisine_db["meals"][3]["idMeal"],
                                                                "dish5name": cuisine_db["meals"][4]["strMeal"], "dish5image": cuisine_db["meals"][4]["strMealThumb"], "dish5id": cuisine_db["meals"][4]["idMeal"],
                                                                "dish6name": cuisine_db["meals"][5]["strMeal"], "dish6image": cuisine_db["meals"][5]["strMealThumb"], "dish6id": cuisine_db["meals"][5]["idMeal"],
                                                                "dish7name": cuisine_db["meals"][6]["strMeal"], "dish7image": cuisine_db["meals"][6]["strMealThumb"], "dish7id": cuisine_db["meals"][6]["idMeal"],
                                                                "dish8name": cuisine_db["meals"][7]["strMeal"], "dish8image": cuisine_db["meals"][7]["strMealThumb"], "dish8id": cuisine_db["meals"][7]["idMeal"],
                                                                "dish9name": cuisine_db["meals"][8]["strMeal"], "dish9image": cuisine_db["meals"][8]["strMealThumb"], "dish9id": cuisine_db["meals"][8]["idMeal"]})
    else:
        return templates.TemplateResponse("/cover/error.html", {"request": request, "title1": "Internal Error", "title2": "Internal Error"})

@app.get("/recipes/{section}/{dish}")
def dish(request: Request, section, dish):
    if section == "American" or section == "British" or section == "Canadian":
        l = requests.get("https://www.themealdb.com/api/json/v1/1/filter.php?a="+section)
        if l.status_code == 200:
            cuisine_db = l.json()

        for i in range(9):
            if dish == cuisine_db["meals"][i]["idMeal"]:
                r = requests.get("https://www.themealdb.com/api/json/v1/1/lookup.php?i="+dish)
                if r.status_code == 200:
                    dish_db = r.json()
                return templates.TemplateResponse("/cover/dish.html", {"request": request, "title1": dish_db["meals"][0]["strMeal"]+" - Recipes", "title2": dish_db["meals"][0]["strMeal"], "image": dish_db["meals"][0]["strMealThumb"], "info": dish_db["meals"][0]["strInstructions"]})
            else:
                return templates.TemplateResponse("/cover/error.html", {"request": request, "title1": "Internal Error", "title2": "Internal Error"})
    else:
        return templates.TemplateResponse("/cover/error.html", {"request": request, "title1": "Internal Error", "title2": "Internal Error"})