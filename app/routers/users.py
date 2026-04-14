from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Request, status, Form
from sqlmodel import select
from app.dependencies.session import SessionDep
from . import api_router
from app.services.user_service import UserService
from app.dependencies.auth import AuthDep
from app.repositories.user import UserRepository
from app.utilities.flash import flash
from app.schemas import UserResponse
from . import router, templates
from app.models.models import *
recent_workouts = []#global list to track user recent workouts
@router.get("/app")
async def get_user(request:Request, db:SessionDep, user:AuthDep):
    user_routines = db.exec(select(Routine).where(Routine.user_id == user.id)).all()
    user_tracker = db.exec(
    select(Tracker).where(Tracker.user_id == user.id)
).all()
    active_routines = db.exec(select(Routine).where(Routine.is_active == True)).all()

    totalCalories = sum(t.meal.calories for t in user_tracker if t.meal)
    for t in active_routines:
    #     print("TRACKER:", t.id, "MEAL:", t.meal)
        if t not in recent_workouts:
            recent_workouts.append(t)
            
    return templates.TemplateResponse(
        request=request,
        name="app.html",
        context={
            "user": user,
            "routines": user_routines,
            "calories": totalCalories,
            "active_routine":active_routines,
            "recent_workouts":recent_workouts,
            "workouts_count": len(user_routines),
            "user_meals": user_tracker
        }
    )
# API endpoint for listing users
@api_router.get("/users", response_model=list[UserResponse])
async def list_users(request: Request, db: SessionDep):
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)
    return user_service.get_all_users()

