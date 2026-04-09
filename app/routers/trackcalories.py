from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import status
from app.dependencies.session import SessionDep
from app.dependencies.auth import AuthDep, IsUserLoggedIn, get_current_user, is_admin
from . import router, templates
from app.models.models import Meal, Tracker
from sqlmodel import select

router = APIRouter(prefix="/api/tracker", tags=["tracker"])

#adds meal to tracker
@router.post("/add/{Meal_id}")
def add_to_tracker(meal_id: int, user: AuthDep, db: SessionDep):
    meal = db.get(Meal, meal_id)

    if not meal:
        return {"Meal not found"}

    tracker = Tracker(
        meal_id= meal.id,
        user_id= user.id,
        calories= meal.calories,
        protein= meal.protein,
        carbs= meal.carbs,
        fat= meal.fat
    )

    db.add(tracker)
    db.commit()
    db.refresh(tracker)
    return tracker

#gets total calories,protein,carbs,fat per user
@router.get("/total")
def get_totals( user: AuthDep, db: SessionDep):
    logs = db.exec(
        select(Tracker).where(Tracker.user_id == user.id)
    ).all()

    total_calories = sum(l.calories for l in logs)
    total_protein = sum(l.protein for l in logs)
    total_carbs = sum(l.carbs for l in logs)
    total_fat = sum(l.fat for l in logs)

    return{
        "calories": total_calories,
        "protein": total_protein,
        "carbs": total_carbs,
        "fat": total_fat
    }

@router.delete("/clear")
def clear_tracker(db: SessionDep, user: AuthDep):
    logs = db.exec(
        select(Tracker).where(Tracker.user_id == user.id)
                  ).all()

    for log in logs:
        db.delete(log)

    db.commit()
    return {"message": "cleared"}
    
#gets track meal
@router.get("/")
def get_tracker(db: SessionDep, user: AuthDep):
    return db.exec(
        select(Tracker).where(Tracker.user_id == user.id)
    ).all()



@router.get("/trackcalories", response_class=HTMLResponse)
async def get_workout(user:AuthDep, db:SessionDep, request:Request):
    return templates.TemplateResponse(
        request=request,
        name="trackcalories.html",
        context={"user": user}
    )
