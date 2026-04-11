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
# API endpoint for listing users
@api_router.get("/users", response_model=list[UserResponse])
async def list_users(request: Request, db: SessionDep):
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)
    return user_service.get_all_users()

@router.get("/app")
async def get_user(request:Request, db:SessionDep, user:AuthDep):
    user_routines = db.exec(select(Routine)).all()
    user_meals = db.exec(select(Tracker).where(Tracker.user_id == user.id)).all()
    totalCalories = 0
    for meals in user_meals:
        totalCalories +=meals.calories
    return templates.TemplateResponse(
        request=request,
        name="app.html",
        context={
            "user": user,
            "routines": user_routines,
            "calories": totalCalories,
            "workouts_count": len(user_routines),
            # "active_routine": None,
            # "recent_workouts": [],
            "user_meals": user_meals
        }
    )
