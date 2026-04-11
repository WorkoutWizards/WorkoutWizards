from fastapi import APIRouter
from app.dependencies.session import SessionDep
from app.models.models import Meal
from sqlmodel import select

router = APIRouter(prefix="/api/meals", tags=["meals"])

default_meals = [
 #BREAKFAST 
{
    "id": 1,
    "type": "breakfast",
    "name": "Protein Pancakes",
    "image": "https://images.unsplash.com/photo-1528207776546-365bb710ee93?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "ingredients": [
        "1 scoop whey protein",
        "1/2 cup oats",
        "1 banana",
        "2 egg whites",
        "Greek yogurt",
        "cinnamon"
    ],
    "instructions": "Blend all ingredients, cook on pan like pancakes, top with berries.",
    "prep_time": "10 mins",
    "protein": 40, "carbs": 55, "fat": 12, "calories": 450
},
{
    "id": 2,
    "type": "breakfast",
    "name": "Egg & Avocado Toast",
    "image": "https://plus.unsplash.com/premium_photo-1676106624038-81d1e17573db?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "ingredients": ["eggs", "avocado", "toast"],
    "instructions": "Toast bread, fry eggs, add avocado on top.",
    "prep_time": "10 mins",
    "protein": 25, "carbs": 30, "fat": 20, "calories": 400
},
{
    "id": 3,
    "type": "breakfast",
    "name": "Oatmeal Power Bowl",
    "image": "https://images.unsplash.com/photo-1517673400267-0251440c45dc",
    "ingredients": ["oats", "milk", "banana", "peanut butter"],
    "instructions": "Cook oats, mix toppings.",
    "prep_time": "5 mins",
    "protein": 20, "carbs": 60, "fat": 10, "calories": 420
},
{
    "id": 4,
    "type": "breakfast",
    "name": "Greek Yogurt Parfait",
    "image": "https://images.unsplash.com/photo-1488477181946-6428a0291777",
    "ingredients": ["yogurt", "granola", "berries"],
    "instructions": "Layer all ingredients.",
    "prep_time": "3 mins",
    "protein": 30, "carbs": 40, "fat": 8, "calories": 350
},
{
    "id": 5,
    "type": "breakfast",
    "name": "Protein Smoothie",
    "image": "https://images.unsplash.com/photo-1553530666-ba11a7da3888",
    "ingredients": ["protein powder", "milk", "banana"],
    "instructions": "Blend everything.",
    "prep_time": "2 mins",
    "protein": 35, "carbs": 45, "fat": 10, "calories": 400
},
{
    "id": 6,
    "type": "breakfast",
    "name": "Scrambled Eggs & Toast",
    "image": "https://media.istockphoto.com/id/1305159700/photo/scrambled-eggs-with-green-onion-on-wheat-rye-wholemeal-crispy-bread-homemade-healthy.webp?a=1&b=1&s=612x612&w=0&k=20&c=uroRXetadSPHGrVS2ZHVZl-KuD7DFXSLWo-VOjdgHmk=",
    "ingredients": ["eggs", "toast", "butter"],
    "instructions": "Scramble eggs and toast bread.",
    "prep_time": "7 mins",
    "protein": 20, "carbs": 25, "fat": 15, "calories": 350
},
{
    "id": 7,
    "type": "breakfast",
    "name": "Peanut Butter Banana Toast",
    "image": "https://plus.unsplash.com/premium_photo-1692912808105-bfb0081f0bd7?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8UGVhbnV0JTIwQnV0dGVyJTIwQmFuYW5hJTIwVG9hc3R8ZW58MHx8MHx8fDA%3D",
    "ingredients": ["toast", "peanut butter", "banana"],
    "instructions": "Spread PB and add banana slices.",
    "prep_time": "5 mins",
    "protein": 15, "carbs": 40, "fat": 12, "calories": 350
},
{
    "id": 8,
    "type": "breakfast",
    "name": "Breakfast Burrito",
    "image": "https://images.unsplash.com/photo-1711488735428-27c6757beb5c?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8QnJlYWtmYXN0JTIwQnVycml0b3xlbnwwfHwwfHx8MA%3D%3D",
    "ingredients": ["tortilla", "eggs", "chicken", "cheese"],
    "instructions": "Cook filling and wrap in tortilla.",
    "prep_time": "15 mins",
    "protein": 35, "carbs": 50, "fat": 18, "calories": 550
},

 # LUNCH 
{
    "id": 9,
    "type": "lunch",
    "name": "Chicken Rice Bowl",
    "image": "https://images.unsplash.com/photo-1771384552858-feb0574f958d?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8N3x8Q2hpY2tlbiUyMFJpY2UlMjBCb3dsfGVufDB8fDB8fHww",
    "ingredients": ["chicken", "rice", "broccoli"],
    "instructions": "Grill chicken, cook rice, steam broccoli.",
    "prep_time": "20 mins",
    "protein": 50, "carbs": 60, "fat": 15, "calories": 600
},
{
    "id": 10,
    "type": "lunch",
    "name": "Turkey Wrap",
    "image": "https://images.unsplash.com/photo-1585238342107-49a3cdace47f?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8VHVya2V5JTIwV3JhcHxlbnwwfHwwfHx8MA%3D%3D",
    "ingredients": ["wrap", "turkey", "veggies"],
    "instructions": "Assemble wrap.",
    "prep_time": "5 mins",
    "protein": 40, "carbs": 50, "fat": 12, "calories": 520
},
{
    "id": 11,
    "type": "lunch",
    "name": "Salmon Quinoa Bowl",
    "image": "https://images.unsplash.com/photo-1546069901-eacef0df6022",
    "ingredients": ["salmon", "quinoa", "greens"],
    "instructions": "Cook salmon and quinoa, combine.",
    "prep_time": "25 mins",
    "protein": 45, "carbs": 55, "fat": 18, "calories": 650
},
{
    "id": 12,
    "type": "lunch",
    "name": "Beef Burrito Bowl",
    "image": "https://media.istockphoto.com/id/2268466971/photo/mexican-beans-and-rice.webp?a=1&b=1&s=612x612&w=0&k=20&c=QJ74hr7zb7KZtwEZ0X9o_AlV9NiErSwFK2DjzbxlCoE=",
    "ingredients": ["beef", "rice", "beans"],
    "instructions": "Cook beef, assemble bowl.",
    "prep_time": "20 mins",
    "protein": 50, "carbs": 65, "fat": 20, "calories": 700
},
{
    "id": 13,
    "type": "lunch",
    "name": "Grilled Chicken Salad",
    "image": "https://plus.unsplash.com/premium_photo-1664640733581-a9175477cd11?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8cmlsbGVkJTIwQ2hpY2tlbiUyMFNhbGFkfGVufDB8fDB8fHww",
    "ingredients": ["chicken", "lettuce", "tomato"],
    "instructions": "Grill chicken and mix salad.",
    "prep_time": "15 mins",
    "protein": 35, "carbs": 20, "fat": 12, "calories": 400
},
{
    "id": 14,
    "type": "lunch",
    "name": "Pasta Chicken Alfredo",
    "image": "https://images.unsplash.com/photo-1570549986390-6bd150ac3515?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8UGFzdGElMjBDaGlja2VuJTIwQWxmcmVkb3xlbnwwfHwwfHx8MA%3D%3D",
    "ingredients": ["pasta", "chicken", "cream"],
    "instructions": "Cook pasta, add sauce and chicken.",
    "prep_time": "20 mins",
    "protein": 45, "carbs": 70, "fat": 22, "calories": 750
},
{
    "id": 15,
    "type": "lunch",
    "name": "Tuna Sandwich",
    "image": "https://images.unsplash.com/photo-1558985250-27a406d64cb3?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8dHVuYSUyMHNhbmR3aWNofGVufDB8fDB8fHww",
    "ingredients": ["tuna", "bread", "mayo"],
    "instructions": "Mix tuna and assemble sandwich.",
    "prep_time": "5 mins",
    "protein": 35, "carbs": 40, "fat": 10, "calories": 450
},
{
    "id": 16,
    "type": "lunch",
    "name": "Chicken Stir Fry",
    "image": "https://images.unsplash.com/photo-1621515554656-3da68ba128b1?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8Q2hpY2tlbiUyMFN0aXIlMjBGcnl8ZW58MHx8MHx8fDA%3D",
    "ingredients": ["chicken", "veggies", "soy sauce"],
    "instructions": "Stir fry all ingredients.",
    "prep_time": "15 mins",
    "protein": 40, "carbs": 45, "fat": 12, "calories": 500
},


 # DINNER 
{
    "id": 17,
    "type": "dinner",
    "name": "Steak & Sweet Potato",
    "image": "https://plus.unsplash.com/premium_photo-1672199330043-d6d2690229e9?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8U3RlYWslMjAlMjYlMjBTd2VldCUyMFBvdGF0b3xlbnwwfHwwfHx8MA%3D%3D",
    "ingredients": ["steak", "sweet potato"],
    "instructions": "Grill steak, bake potato.",
    "prep_time": "40 mins",
    "protein": 55, "carbs": 70, "fat": 20, "calories": 700
},
{
    "id": 18,
    "type": "dinner",
    "name": "Grilled Salmon Plate",
    "image": "https://images.unsplash.com/photo-1676300185165-3f543c1fcb72?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8R3JpbGxlZCUyMFNhbG1vbiUyMFBsYXRlfGVufDB8fDB8fHww",
    "ingredients": ["salmon", "vegetables"],
    "instructions": "Grill salmon and serve.",
    "prep_time": "20 mins",
    "protein": 50, "carbs": 40, "fat": 18, "calories": 600
},
{
    "id": 19,
    "type": "dinner",
    "name": "Shrimp Stir Fry",
    "image": "https://images.unsplash.com/photo-1703876087121-50a1c0a00e4d?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8N3x8U2hyaW1wJTIwU3RpciUyMEZyeXxlbnwwfHwwfHx8MA%3D%3D",
    "ingredients": ["shrimp", "veggies"],
    "instructions": "Cook shrimp and veggies.",
    "prep_time": "15 mins",
    "protein": 40, "carbs": 50, "fat": 12, "calories": 500
},
{
    "id": 20,
    "type": "dinner",
    "name": "Beef & Veggies",
    "image": "https://images.unsplash.com/photo-1723531055852-744d14ac00b4?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8QmVlZiUyMCUyNiUyMFZlZ2dpZXN8ZW58MHx8MHx8fDA%3D",
    "ingredients": ["beef", "vegetables"],
    "instructions": "Cook beef with veggies.",
    "prep_time": "20 mins",
    "protein": 50, "carbs": 30, "fat": 18, "calories": 550
},

#  SNACKS 
{
    "id": 21,
    "type": "snack",
    "name": "Greek Yogurt Bowl",
    "image": "https://images.unsplash.com/photo-1530259152377-3a014e1092e0?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8R3JlZWslMjBZb2d1cnQlMjBCb3dsfGVufDB8fDB8fHww",
    "ingredients": ["yogurt", "nuts"],
    "instructions": "Mix together.",
    "prep_time": "2 mins",
    "protein": 30, "carbs": 20, "fat": 10, "calories": 350
},
{
    "id": 22,
    "type": "snack",
    "name": "Protein Shake",
    "image": "https://plus.unsplash.com/premium_photo-1726765808183-9c3d6a119000?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTd8fHByb3RlaW4lMjBzaGFrZXJ8ZW58MHx8MHx8fDA%3D",
    "ingredients": ["protein powder", "milk"],
    "instructions": "Blend.",
    "prep_time": "1 min",
    "protein": 35, "carbs": 25, "fat": 12, "calories": 400
},
{
    "id": 23,
    "type": "snack",
    "name": "Tuna Salad",
    "image": "https://images.unsplash.com/photo-1604909052743-94e838986d24?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8dHVuYSUyMHNhbGFkfGVufDB8fDB8fHww",
    "ingredients": ["tuna", "veggies"],
    "instructions": "Mix ingredients.",
    "prep_time": "5 mins",
    "protein": 40, "carbs": 10, "fat": 8, "calories": 300
},
{
    "id": 24,
    "type": "snack",
    "name": "Cottage Cheese & Fruit",
    "image": "https://images.unsplash.com/photo-1631718051263-c567dca19362?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8Q290dGFnZSUyMENoZWVzZSUyMCUyNiUyMEZydWl0fGVufDB8fDB8fHww",
    "ingredients": ["cottage cheese", "apple"],
    "instructions": "Serve together.",
    "prep_time": "2 mins",
    "protein": 28, "carbs": 30, "fat": 5, "calories": 280
},
{
    "id": 25,
    "type": "snack",
    "name": "Peanut Butter Apple",
    "image": "https://plus.unsplash.com/premium_photo-1699150949538-60bdfd8dccb8?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8UGVhbnV0JTIwQnV0dGVyJTIwQXBwbGV8ZW58MHx8MHx8fDA%3D",
    "ingredients": ["apple", "peanut butter"],
    "instructions": "Slice apple and dip.",
    "prep_time": "3 mins",
    "protein": 15, "carbs": 35, "fat": 12, "calories": 300
},
{
    "id": 26,
    "type": "snack",
    "name": "Boiled Eggs",
    "image": "https://images.unsplash.com/photo-1482049016688-2d3e1b311543?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8Qm9pbGVkJTIwRWdnc3xlbnwwfHwwfHx8MA%3D%3D",
    "ingredients": ["eggs"],
    "instructions": "Boil eggs.",
    "prep_time": "10 mins",
    "protein": 12, "carbs": 1, "fat": 10, "calories": 150
}
]

# SEED DATABASE 
def seed_meals(db):
    existing = db.exec(select(Meal)).first()
    if existing:
        return 

    for meal_data in default_meals:
        meal = Meal(**meal_data)
        db.add(meal)

    db.commit()
    print("Database initialized with meals API")


# GET ALL MEALS
# @router.get("/")
# def get_meals(db: SessionDep):
#     seed_meals(db)
#     return db.exec(select(Meal)).all()


# GET BY TYPE
@router.get("/type/{meal_type}")
def get_by_type(meal_type: str, db: SessionDep):
    seed_meals(db)
    statement = select(Meal).where(Meal.type == meal_type.lower())
    return db.exec(statement).all()


# GET ONE MEAL
@router.get("/{meal_id}")
def get_meal(meal_id: int, db: SessionDep):
    seed_meals(db)
    return db.get(Meal, meal_id)


# CREATE MEAL
@router.post("/")
def create_meal(meal: Meal, db: SessionDep):
    db.add(meal)
    db.commit()
    db.refresh(meal)
    return meal


# UPDATE MEAL
@router.put("/{meal_id}")
def update_meal(meal_id: int, updated_meal: Meal, db: SessionDep):
    meal = db.get(Meal, meal_id)

    if not meal:
        return {"error": "Meal not found"}

    for key, value in updated_meal.dict().items():
        setattr(meal, key, value)

    db.commit()
    db.refresh(meal)
    return meal


# DELETE MEAL
@router.delete("/{meal_id}")
def delete_meal(meal_id: int, db: SessionDep):
    meal = db.get(Meal, meal_id)

    if not meal:
        return {"error": "Not found"}

    db.delete(meal)
    db.commit()
    return {"message": "Deleted"}
 

