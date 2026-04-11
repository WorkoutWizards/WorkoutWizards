from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import status,Query,Form
from app.dependencies.session import SessionDep
from app.dependencies.auth import AuthDep, IsUserLoggedIn, get_current_user, is_admin
from app.utilities.flash import flash
from . import router, templates
from app.models.models import Meal, Tracker
from sqlmodel import select

# router = APIRouter(prefix="/api/tracker", tags=["tracker"])
@router.get("/trackcalories", response_class=HTMLResponse)
async def get_tracker_page(user: AuthDep, db: SessionDep, request: Request):

    logs = db.exec(
        select(Tracker).where(Tracker.user_id == user.id)
    ).all()

    all_meals = db.exec(select(Meal)).all()

    return templates.TemplateResponse(
        request=request,
        name="trackcalories.html",
        context={
            "user": user,
            "logs": logs,
            "all_meals": all_meals
        }
    )


@router.post("/api/tracker/update-meal/")
def update_meal(
    user: AuthDep,
    db: SessionDep,
    request: Request,
    tracker_id: int = Form(),
    calories: int = Form()
):
    entry = db.exec(select(Tracker).where(Tracker.id == tracker_id,
    Tracker.user_id == user.id)).one_or_none()

    if not entry or entry.user_id != user.id:
        flash(request, "Meal not found")
        return RedirectResponse(url =request.url_for('get_tracker_page'), status_code=303)
    if calories:
        entry.calories = calories

    db.add(entry)
    db.commit()

    flash(request, "Meal updated!")

    return RedirectResponse(url =request.url_for('get_tracker_page'), status_code=303)

@router.post("/api/tracker/delete-meal/")
def delete_meal_from_tracker(
    user: AuthDep,
    db: SessionDep,
    request: Request,
    tracker_id: int = Form()
):
    entry = db.get(Tracker, tracker_id)

    if not entry:
        flash(request, "Meal not found in tracker")
        return RedirectResponse(url =request.url_for('get_tracker_page'), status_code=303)
    try:
        db.delete(entry)
        db.commit()
        flash(request, "Meal removed!")
    except Exception:
        flash(request, "Cannot removed Meal from Tracker")

   

    return RedirectResponse(url =request.url_for('get_tracker_page'), status_code=303)
#adds meal to tracker
@router.post("/api/tracker/add/{meal_id}")
def add_to_tracker(meal_id: int, user: AuthDep, db: SessionDep,
                   request:Request):
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
    flash(request,"Meal added to Your Meal Tracker")
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
    
# gets track meal
@router.get("/")
def get_tracker(db: SessionDep, user: AuthDep):
    return db.exec(
        select(Tracker).where(Tracker.user_id == user.id)
    ).all()



