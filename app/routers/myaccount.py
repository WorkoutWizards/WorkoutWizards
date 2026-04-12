from fastapi import APIRouter, Form, HTTPException, Depends, Request,Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import status
from sqlmodel import select
from app.dependencies.session import SessionDep
from app.dependencies.auth import AuthDep, IsUserLoggedIn, get_current_user, is_admin
from app.models.models import Routine,RoutineExercise, Tracker,Meal
from . import router, templates
from app.utilities.flash import flash


#jinja endpoint to return the myaccount template
@router.get("/myaccount/", response_class=HTMLResponse)
async def get_workout(
    user:AuthDep, db:SessionDep, request:Request
):
    user_meals = db.exec(select(Tracker).where(Tracker.user_id == user.id)).all()
    totalCalories = 0
    for meals in user_meals:
        totalCalories +=meals.meal.calories

  
    return templates.TemplateResponse(
        request= request,
        name = "myaccount.html",
        context = {
        
            "user":user,
            "total_calories":totalCalories
        }
    )

@router.post("/update-account")
async def update_account(request: Request, db: SessionDep, user:AuthDep):

    form = await request.form()

    user.height_m = float(form["height_m"])
    user.weight_kg = float(form["weight_kg"])
    user.age = int(form["age"])
    user.gender = form["gender"]
    user.hip_width = float(form["hip_width"])
    user.neck_width = float(form["neck_width"])
    user.calorie_goal = float(form["calorie_goal"])

    db.add(user)
    db.commit()
    user.user_bmi = user.calculate_bmi()

    db.add(user)
    db.commit()
    db.refresh(user)
    flash(request,f"{user.username} Information Updated")
    return RedirectResponse(url ="/myaccount/", status_code=303)