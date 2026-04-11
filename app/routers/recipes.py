from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import status
from app.dependencies.session import SessionDep
from app.dependencies.auth import AuthDep, IsUserLoggedIn, get_current_user, is_admin
from . import router, templates
from app.models.models import Recipe
from sqlmodel import select

#added
# router = APIRouter(prefix="/api/recipes", tags=["recipes"])
# removed router prefix api/recipes

#end of added
#jinja endpoint to return the workout template
@router.get("/recipes", response_class=HTMLResponse)
async def get_workout(
    user:AuthDep, db:SessionDep, request:Request
):
    return templates.TemplateResponse(
        request= request,
        name = "recipes.html",
        context = {

            "user":user
        }
    )
@router.get("/")
def get_recipes(db: SessionDep):
    return db.exec(select(Recipe)).all()
@router.get("/{recipe_id}")
def get_recipe(recipe_id: int, db: SessionDep):
    recipe = db.get(Recipe, recipe_id)
    return recipe

@router.post("/")
def create_recipe(recipe: Recipe, db: SessionDep):
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe

@router.put("/{recipe_id}")
def update_recipe(recipe_id: int, updated_recipe: Recipe, db: SessionDep):
    recipe = db.get(Recipe, recipe_id)
    if not recipe:
        return {"error":"Recipe not found"}
    
    for key, value in updated_recipe.dict().items():
        setattr(recipe, key, value)
    
    db.commit()
    db.refresh(recipe)
    return recipe

@router.delete("/{recipe_id}")
def delete_recipe(recipe_id: int, db: SessionDep):
    recipe = db.get(Recipe, recipe_id)
    if not recipe:
        return {"error":"Recipe not found"}
    
    db.delete(recipe)
    db.commit()
    return {"message":"Recipe deleted"}
