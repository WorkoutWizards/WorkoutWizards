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
        "1/4 cup Greek yogurt",
        "1/2 tsp cinnamon"
    ],
    "instructions": [
        "Add oats to a blender and pulse for 30 seconds to create oat flour.",
        "Peel the banana and add it to the blender along with the whey protein, egg whites, Greek yogurt, and cinnamon.",
        "Blend everything on high for 60 seconds until the batter is completely smooth. If the batter is too thick, add 1–2 tbsp of water.",
        "Heat a non-stick skillet or griddle over medium-low heat and lightly coat with cooking spray or a tiny bit of butter.",
        "Pour approximately 1/4 cup of batter per pancake onto the pan. Do not overcrowd — cook 2 at a time.",
        "Cook until bubbles form across the entire surface and the edges look set, about 2–3 minutes.",
        "Carefully flip each pancake and cook for another 1–2 minutes until golden brown.",
        "Transfer to a plate and repeat with remaining batter.",
        "Top with fresh berries, a drizzle of honey, or a spoonful of Greek yogurt and serve immediately."
    ],
    "prep_time": "10 mins",
    "protein": 40, "carbs": 55, "fat": 12, "calories": 450
},
{
    "id": 2,
    "type": "breakfast",
    "name": "Egg & Avocado Toast",
    "image": "https://plus.unsplash.com/premium_photo-1676106624038-81d1e17573db?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "ingredients": [
        "2 large eggs",
        "1 ripe avocado",
        "2 slices whole-grain bread",
        "Salt & pepper to taste",
        "Red chili flakes (optional)",
        "Lemon juice (a squeeze)"
    ],
    "instructions": [
        "Place bread slices in the toaster and toast to your desired level of crispness — golden brown works best.",
        "While the bread toasts, halve the avocado, remove the pit, and scoop the flesh into a small bowl.",
        "Add a squeeze of fresh lemon juice, a pinch of salt, and freshly cracked black pepper to the avocado.",
        "Mash with a fork until creamy but still slightly chunky for texture. Taste and adjust seasoning.",
        "Heat a non-stick skillet over medium heat and add a small knob of butter or a spray of cooking oil.",
        "Crack the eggs directly into the pan. For sunny-side up, cook undisturbed for 2–3 minutes. For over-easy, flip after 2 minutes and cook 30 seconds more.",
        "Season the eggs with a pinch of salt and pepper.",
        "Spread a generous layer of mashed avocado on each slice of toast.",
        "Place one egg on top of each toast. Finish with red chili flakes and an extra crack of pepper. Serve immediately."
    ],
    "prep_time": "10 mins",
    "protein": 25, "carbs": 30, "fat": 20, "calories": 400
},
{
    "id": 3,
    "type": "breakfast",
    "name": "Oatmeal Power Bowl",
    "image": "https://images.unsplash.com/photo-1517673400267-0251440c45dc",
    "ingredients": [
        "1 cup rolled oats",
        "1 cup milk (or oat milk)",
        "1 banana, sliced",
        "2 tbsp peanut butter",
        "1 tsp honey",
        "Pinch of salt"
    ],
    "instructions": [
        "Pour 1 cup of milk (or water) into a small saucepan and bring to a gentle simmer over medium heat.",
        "Stir in the rolled oats and a pinch of salt.",
        "Reduce heat to medium-low and cook, stirring occasionally, for 4–5 minutes until the oats absorb the liquid and reach a creamy, porridge-like consistency.",
        "If the oatmeal becomes too thick, stir in a splash more milk to loosen it up.",
        "Remove from heat and transfer to your serving bowl.",
        "Slice the banana and arrange the slices over the top of the oatmeal.",
        "Add a dollop of peanut butter in the center — it will melt slightly into the warm oats.",
        "Drizzle honey over everything for natural sweetness.",
        "Optional: sprinkle chia seeds, crushed walnuts, or a dash of cinnamon on top for extra nutrition and crunch."
    ],
    "prep_time": "5 mins",
    "protein": 20, "carbs": 60, "fat": 10, "calories": 420
},
{
    "id": 4,
    "type": "breakfast",
    "name": "Greek Yogurt Parfait",
    "image": "https://images.unsplash.com/photo-1488477181946-6428a0291777",
    "ingredients": [
        "1 cup Greek yogurt (plain, full-fat)",
        "1/3 cup granola",
        "1/2 cup mixed berries (blueberries, strawberries, raspberries)",
        "1 tbsp honey",
        "1 tsp chia seeds"
    ],
    "instructions": [
        "Choose a tall glass or wide bowl for a beautiful layered presentation.",
        "Spoon half of the Greek yogurt as the first layer at the bottom, spreading it evenly.",
        "Add a layer of granola over the yogurt — about 2 tablespoons — for crunch.",
        "Add a layer of mixed berries: blueberries, sliced strawberries, or raspberries work great.",
        "Repeat the layers: yogurt, granola, then berries.",
        "Drizzle honey generously over the final berry layer.",
        "Sprinkle chia seeds on top for added fiber and omega-3s.",
        "Serve immediately so the granola stays crunchy. If making ahead, store layers separately and assemble before eating."
    ],
    "prep_time": "3 mins",
    "protein": 30, "carbs": 40, "fat": 8, "calories": 350
},
{
    "id": 5,
    "type": "breakfast",
    "name": "Protein Smoothie",
    "image": "https://images.unsplash.com/photo-1553530666-ba11a7da3888",
    "ingredients": [
        "1 scoop protein powder (vanilla or chocolate)",
        "1 cup milk or almond milk",
        "1 banana (frozen for creaminess)",
        "1/2 cup ice cubes",
        "1 tbsp peanut butter (optional)"
    ],
    "instructions": [
        "Peel and freeze the banana at least 2 hours in advance for a thicker, creamier smoothie texture.",
        "Pour 1 cup of milk or almond milk into the blender first — adding liquid first protects the blade.",
        "Add the frozen banana, protein powder scoop, and peanut butter if using.",
        "Add the ice cubes last.",
        "Secure the blender lid and blend on high speed for 45–60 seconds until completely smooth with no chunks.",
        "Remove the lid and check the consistency — if too thick, add a splash more milk; if too thin, add a few more ice cubes.",
        "Taste and adjust sweetness — a drizzle of honey can help if your protein powder isn't sweet enough.",
        "Pour into a large glass and consume immediately for best taste. Optional: garnish with banana slices or a dusting of cinnamon."
    ],
    "prep_time": "2 mins",
    "protein": 35, "carbs": 45, "fat": 10, "calories": 400
},
{
    "id": 6,
    "type": "breakfast",
    "name": "Scrambled Eggs & Toast",
    "image": "https://media.istockphoto.com/id/1305159700/photo/scrambled-eggs-with-green-onion-on-wheat-rye-wholemeal-crispy-bread-homemade-healthy.webp?a=1&b=1&s=612x612&w=0&k=20&c=uroRXetadSPHGrVS2ZHVZl-KuD7DFXSLWo-VOjdgHmk=",
    "ingredients": [
        "3 large eggs",
        "2 slices whole-grain bread",
        "1 tbsp butter",
        "2 tbsp milk",
        "Salt & pepper to taste",
        "Fresh chives (optional)"
    ],
    "instructions": [
        "Crack 3 eggs into a bowl. Add 2 tablespoons of milk, a pinch of salt, and freshly cracked black pepper.",
        "Whisk vigorously with a fork until the yolks and whites are fully combined and slightly frothy — this incorporates air for fluffier eggs.",
        "Place bread in the toaster and toast to golden brown.",
        "Place a non-stick skillet over LOW heat — this is the key to creamy scrambled eggs. Add butter and let it melt slowly without browning.",
        "Pour in the egg mixture. Let it sit for 10–15 seconds undisturbed.",
        "Using a rubber spatula, gently push the eggs from the edges toward the center in slow, sweeping folds. Do not stir rapidly.",
        "Continue this process, pulling the pan off the heat momentarily if it gets too hot. The eggs should look glossy and slightly underdone when you remove from heat — residual heat finishes them.",
        "Remove from heat just before fully set — they should be soft and creamy, not dry.",
        "Plate the toast, pile the scrambled eggs on top, and garnish with freshly snipped chives. Serve at once."
    ],
    "prep_time": "7 mins",
    "protein": 20, "carbs": 25, "fat": 15, "calories": 350
},
{
    "id": 7,
    "type": "breakfast",
    "name": "Peanut Butter Banana Toast",
    "image": "https://plus.unsplash.com/premium_photo-1692912808105-bfb0081f0bd7?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8UGVhbnV0JTIwQnV0dGVyJTIwQmFuYW5hJTIwVG9hc3R8ZW58MHx8MHx8fDA%3D",
    "ingredients": [
        "2 slices whole-grain or sourdough bread",
        "2 tbsp natural peanut butter",
        "1 banana, sliced",
        "1 tsp honey",
        "Pinch of cinnamon"
    ],
    "instructions": [
        "Place the bread slices in the toaster. Toast to a deep golden brown — a crunchier toast holds up better under the toppings.",
        "While the bread toasts, peel the banana and slice it into even rounds, about 1/4 inch thick.",
        "Once the toast is ready, immediately spread 1 tablespoon of natural peanut butter on each slice while it's still warm — the warmth makes it easier to spread.",
        "Make sure the peanut butter covers edge to edge so every bite has flavor.",
        "Arrange the banana slices on top of the peanut butter in a single layer, slightly overlapping.",
        "Drizzle honey over the banana slices in a light zigzag pattern.",
        "Finish with a pinch of ground cinnamon over each slice.",
        "Optional: add a sprinkle of crushed walnuts or hemp seeds for extra healthy fats and crunch.",
        "Serve immediately and enjoy!"
    ],
    "prep_time": "5 mins",
    "protein": 15, "carbs": 40, "fat": 12, "calories": 350
},
{
    "id": 8,
    "type": "breakfast",
    "name": "Breakfast Burrito",
    "image": "https://images.unsplash.com/photo-1711488735428-27c6757beb5c?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8QnJlYWtmYXN0JTIwQnVycml0b3xlbnwwfHwwfHx8MA%3D%3D",
    "ingredients": [
        "2 large flour tortillas",
        "3 eggs, scrambled",
        "1/2 cup cooked chicken breast, shredded",
        "1/4 cup shredded cheddar cheese",
        "2 tbsp salsa",
        "Salt & pepper to taste"
    ],
    "instructions": [
        "If using raw chicken, season a chicken breast with salt, pepper, and a pinch of paprika. Cook in a skillet over medium-high heat for 6–7 minutes per side until cooked through. Let rest, then shred with two forks.",
        "Crack 3 eggs into a bowl, season with salt and pepper, and whisk until uniform.",
        "In the same skillet over medium-low heat, scramble the eggs gently using a rubber spatula, folding rather than stirring, until just barely set. Remove from heat immediately.",
        "Warm the flour tortillas: place each one directly over a gas burner for 10 seconds per side, or microwave for 20 seconds wrapped in a damp paper towel.",
        "Lay each warm tortilla flat. Down the center of each, layer: shredded chicken, scrambled eggs, and shredded cheddar cheese.",
        "Add a spoonful of salsa if desired at this stage (or serve on the side to keep the burrito from getting soggy).",
        "Fold in the sides of the tortilla, then roll it up tightly from the bottom like a burrito. Make sure the seam is on the bottom.",
        "Place the burritos seam-side down in a dry skillet over medium heat. Toast for 1–2 minutes per side until golden and lightly crisp.",
        "Slice in half diagonally and serve with extra salsa, hot sauce, or guacamole."
    ],
    "prep_time": "15 mins",
    "protein": 35, "carbs": 50, "fat": 18, "calories": 550
},

 # LUNCH 
{
    "id": 9,
    "type": "lunch",
    "name": "Chicken Rice Bowl",
    "image": "https://images.unsplash.com/photo-1771384552858-feb0574f958d?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8N3x8Q2hpY2tlbiUyMFJpY2UlMjBCb3dsfGVufDB8fDB8fHww",
    "ingredients": [
        "1 large chicken breast",
        "1 cup jasmine or brown rice",
        "1 cup broccoli florets",
        "1 tbsp olive oil",
        "Salt, pepper, garlic powder",
        "Soy sauce or teriyaki sauce"
    ],
    "instructions": [
        "Rinse the rice under cold water until the water runs clear. Cook according to package directions (typically 1 cup rice to 2 cups water, bring to boil, reduce to simmer for 18 minutes, then rest 5 minutes with lid on).",
        "Pat the chicken breast dry with paper towels. Rub with olive oil, then season generously on both sides with salt, pepper, and garlic powder.",
        "Preheat a grill pan or cast-iron skillet over medium-high heat until very hot — about 2 minutes.",
        "Place the chicken breast on the grill pan and press gently. Cook undisturbed for 5–6 minutes until grill marks appear and the chicken releases easily.",
        "Flip and cook for another 5–6 minutes until the internal temperature reaches 165°F (74°C).",
        "Remove chicken from heat, tent loosely with foil, and rest for 5 minutes before slicing.",
        "While the chicken rests, steam the broccoli: place florets in a microwave-safe bowl with 2 tablespoons of water, cover, and microwave for 3–4 minutes until tender-crisp. Season with a pinch of salt.",
        "Slice the rested chicken breast diagonally into even strips.",
        "Assemble the bowl: add a scoop of fluffy rice as the base, arrange broccoli on one side, and fan the chicken slices on top. Drizzle generously with soy sauce or teriyaki sauce and serve."
    ],
    "prep_time": "20 mins",
    "protein": 50, "carbs": 60, "fat": 15, "calories": 600
},
{
    "id": 10,
    "type": "lunch",
    "name": "Turkey Wrap",
    "image": "https://images.unsplash.com/photo-1585238342107-49a3cdace47f?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8VHVya2V5JTIwV3JhcHxlbnwwfHwwfHx8MA%3D%3D",
    "ingredients": [
        "1 large whole-wheat wrap/tortilla",
        "100g sliced turkey breast",
        "Romaine lettuce leaves",
        "Sliced tomato",
        "Sliced cucumber",
        "1 tbsp hummus or mustard"
    ],
    "instructions": [
        "Lay the whole-wheat wrap flat on a clean cutting board or work surface.",
        "Spread 1 tablespoon of hummus or mustard evenly across the center of the wrap, leaving a 2-inch border around the edges.",
        "Layer the romaine lettuce leaves first — they act as a moisture barrier to prevent the wrap from getting soggy.",
        "Layer the sliced turkey breast evenly over the lettuce.",
        "Add tomato slices and cucumber rounds on top of the turkey.",
        "Season lightly with salt, pepper, and any desired herbs (dried oregano or Italian seasoning works well).",
        "Fold in the left and right sides of the wrap by about an inch each.",
        "Starting from the bottom, roll the wrap away from you tightly, keeping the sides tucked in as you go.",
        "Slice the wrap diagonally in half using a sharp knife for a clean cut. Serve immediately, or wrap tightly in parchment paper for meal prep."
    ],
    "prep_time": "5 mins",
    "protein": 40, "carbs": 50, "fat": 12, "calories": 520
},
{
    "id": 11,
    "type": "lunch",
    "name": "Salmon Quinoa Bowl",
    "image": "https://images.unsplash.com/photo-1546069901-eacef0df6022",
    "ingredients": [
        "1 salmon fillet (150g)",
        "3/4 cup quinoa",
        "2 cups mixed greens",
        "1/2 avocado, sliced",
        "Lemon juice",
        "Olive oil, salt & pepper"
    ],
    "instructions": [
        "Rinse quinoa thoroughly under cold water using a fine-mesh strainer to remove bitterness. Combine with 1.5 cups of water in a saucepan, bring to a boil, then reduce to low heat, cover, and cook for 15 minutes until water is absorbed. Fluff with a fork and let cool slightly.",
        "Pat the salmon fillet completely dry. Season both sides with salt, pepper, and a drizzle of olive oil.",
        "Heat a skillet over medium-high heat until hot. Place the salmon skin-side up and cook for 3–4 minutes until a golden crust forms.",
        "Flip the salmon carefully and cook for another 3–4 minutes. The salmon is done when it flakes easily with a fork and the center is just barely opaque.",
        "Remove the salmon from heat and squeeze a little lemon juice over the top. Let it rest for 2 minutes.",
        "While salmon rests, halve the avocado, remove the pit, and slice it thinly.",
        "Build the bowl: add a base of mixed greens, then scoop the quinoa over half the greens.",
        "Break the salmon fillet into large chunks (or keep whole) and place on top.",
        "Fan the avocado slices alongside. Drizzle everything with fresh lemon juice and a light drizzle of olive oil. Season to taste and serve."
    ],
    "prep_time": "25 mins",
    "protein": 45, "carbs": 55, "fat": 18, "calories": 650
},
{
    "id": 12,
    "type": "lunch",
    "name": "Beef Burrito Bowl",
    "image": "https://media.istockphoto.com/id/2268466971/photo/mexican-beans-and-rice.webp?a=1&b=1&s=612x612&w=0&k=20&c=QJ74hr7zb7KZtwEZ0X9o_AlV9NiErSwFK2DjzbxlCoE=",
    "ingredients": [
        "150g lean ground beef",
        "1 cup cooked white rice",
        "1/2 cup black beans",
        "1/4 cup corn",
        "Salsa & sour cream",
        "Taco seasoning"
    ],
    "instructions": [
        "Cook the rice according to package directions. Keep warm.",
        "Heat a skillet over medium-high heat. Add ground beef and break it apart with a wooden spoon as it cooks.",
        "Cook the beef for 5–6 minutes, stirring occasionally, until fully browned and no pink remains. Drain any excess fat.",
        "Add taco seasoning and 2–3 tablespoons of water to the beef. Stir well to coat every piece.",
        "Let the seasoned beef cook for another 2 minutes until the liquid reduces and the beef is nicely coated and fragrant.",
        "Warm the black beans: drain and rinse canned black beans, then heat in a small saucepan with a pinch of cumin and salt for 3–4 minutes.",
        "Warm the corn in the same pan or microwave for 1 minute.",
        "Assemble the bowl: start with a base of fluffy white rice. Add seasoned beef on one side, black beans on another, and corn in the center.",
        "Top with a spoonful of fresh salsa, a dollop of sour cream, and optionally shredded cheese, jalapeños, or fresh cilantro. Serve hot."
    ],
    "prep_time": "20 mins",
    "protein": 50, "carbs": 65, "fat": 20, "calories": 700
},
{
    "id": 13,
    "type": "lunch",
    "name": "Grilled Chicken Salad",
    "image": "https://plus.unsplash.com/premium_photo-1664640733581-a9175477cd11?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8cmlsbGVkJTIwQ2hpY2tlbiUyMFNhbGFkfGVufDB8fDB8fHww",
    "ingredients": [
        "1 chicken breast",
        "2 cups romaine lettuce, chopped",
        "1 cup cherry tomatoes, halved",
        "1/2 cucumber, sliced",
        "Red onion, thinly sliced",
        "Olive oil & lemon dressing"
    ],
    "instructions": [
        "Season the chicken breast with olive oil, salt, pepper, garlic powder, and dried oregano. Let it marinate at room temperature for 10 minutes if time allows.",
        "Preheat a grill pan over medium-high heat. Grill the chicken for 5–6 minutes per side until cooked through (internal temp 165°F / 74°C) with clear grill marks.",
        "Remove the chicken and let it rest on a cutting board for 5 minutes — this keeps it juicy.",
        "While the chicken rests, prepare the salad base: wash and chop the romaine lettuce into bite-sized pieces and place in a large bowl.",
        "Add the halved cherry tomatoes, sliced cucumber, and thin rings of red onion to the bowl.",
        "Make a quick dressing: whisk together 2 tablespoons of olive oil, the juice of half a lemon, a pinch of salt, pepper, and 1/2 teaspoon of Dijon mustard.",
        "Drizzle the dressing over the salad and toss gently to coat every leaf.",
        "Slice the rested chicken breast diagonally into thin strips.",
        "Arrange the chicken slices over the dressed salad. Optionally top with shaved Parmesan, croutons, or a sprinkle of seeds. Serve immediately."
    ],
    "prep_time": "15 mins",
    "protein": 35, "carbs": 20, "fat": 12, "calories": 400
},
{
    "id": 14,
    "type": "lunch",
    "name": "Pasta Chicken Alfredo",
    "image": "https://images.unsplash.com/photo-1570549986390-6bd150ac3515?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8UGFzdGElMjBDaGlja2VuJTIwQWxmcmVkb3xlbnwwfHwwfHx8MA%3D%3D",
    "ingredients": [
        "200g fettuccine pasta",
        "1 chicken breast, sliced",
        "1/2 cup heavy cream",
        "1/4 cup Parmesan, grated",
        "2 cloves garlic, minced",
        "Butter, salt & pepper"
    ],
    "instructions": [
        "Bring a large pot of heavily salted water to a rolling boil. Add fettuccine and cook according to package directions until al dente (usually 10–12 minutes). Reserve 1/2 cup of pasta water before draining.",
        "While the pasta cooks, slice the chicken breast into thin strips. Season with salt, pepper, and garlic powder.",
        "Heat 1 tablespoon of butter in a large skillet over medium-high heat. Add chicken strips in a single layer and sear for 3–4 minutes per side until golden and cooked through. Remove and set aside.",
        "In the same skillet, reduce heat to medium. Add another tablespoon of butter and the minced garlic. Sauté for 60 seconds until fragrant — do not brown the garlic.",
        "Pour in the heavy cream and stir, scraping up any bits from the bottom. Let it simmer for 2–3 minutes until it begins to thicken slightly.",
        "Remove from heat and stir in the grated Parmesan until the sauce is smooth and glossy. Season with salt and pepper.",
        "Add the drained pasta to the sauce and toss to coat every strand. If the sauce is too thick, add a splash of reserved pasta water to loosen it.",
        "Return the cooked chicken strips to the pan and fold them through the pasta.",
        "Plate immediately, top with extra Parmesan and freshly cracked black pepper. A sprinkle of fresh parsley adds color."
    ],
    "prep_time": "20 mins",
    "protein": 45, "carbs": 70, "fat": 22, "calories": 750
},
{
    "id": 15,
    "type": "lunch",
    "name": "Tuna Sandwich",
    "image": "https://images.unsplash.com/photo-1558985250-27a406d64cb3?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8dHVuYSUyMHNhbmR3aWNofGVufDB8fDB8fHww",
    "ingredients": [
        "1 can tuna in water (drained)",
        "2 slices whole-grain bread",
        "1 tbsp mayonnaise",
        "1 tsp Dijon mustard",
        "Celery, finely chopped",
        "Salt, pepper & lemon juice"
    ],
    "instructions": [
        "Open and thoroughly drain the canned tuna. Use the back of the can lid to press out as much water as possible for a firmer filling.",
        "Transfer the tuna to a bowl and flake it with a fork until broken into small pieces.",
        "Add mayonnaise, Dijon mustard, and a squeeze of fresh lemon juice to the bowl.",
        "Stir in the finely chopped celery — this adds essential crunch. Season with salt and freshly cracked pepper.",
        "Mix everything together until well combined. Taste and adjust with more lemon juice, mayo, or seasoning as needed.",
        "Toast the bread slices to a golden brown for a sturdier, more flavorful sandwich base.",
        "Spread the tuna mixture generously over one slice of toast, going all the way to the edges.",
        "Add optional toppings: sliced tomato, lettuce, thinly sliced red onion, or cucumber.",
        "Close the sandwich with the second slice, press gently, and cut diagonally. Serve immediately."
    ],
    "prep_time": "5 mins",
    "protein": 35, "carbs": 40, "fat": 10, "calories": 450
},
{
    "id": 16,
    "type": "lunch",
    "name": "Chicken Stir Fry",
    "image": "https://images.unsplash.com/photo-1621515554656-3da68ba128b1?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8Q2hpY2tlbiUyMFN0aXIlMjBGcnl8ZW58MHx8MHx8fDA%3D",
    "ingredients": [
        "1 chicken breast, thinly sliced",
        "2 cups mixed vegetables (bell pepper, broccoli, snap peas, carrot)",
        "3 tbsp soy sauce",
        "1 tbsp sesame oil",
        "2 cloves garlic, minced",
        "1 tsp fresh ginger, grated"
    ],
    "instructions": [
        "Prepare all ingredients before you start cooking — stir fry moves fast! Slice the chicken breast into thin strips against the grain. Chop all vegetables into similar-sized bite-sized pieces.",
        "In a small bowl, mix together soy sauce, sesame oil, a teaspoon of cornstarch, and a pinch of sugar to make the stir fry sauce. Set aside.",
        "Heat a wok or large skillet over HIGH heat until it's smoking. This is critical — high heat gives you the 'wok hei' flavor.",
        "Add a tablespoon of vegetable oil and swirl to coat. Add the chicken strips in a single layer. Do not stir immediately — let them sear for 90 seconds to develop color.",
        "Stir fry the chicken for another 2 minutes until cooked through. Remove from the wok and set aside.",
        "Add another drizzle of oil. Add the minced garlic and grated ginger. Stir constantly for 30 seconds — they should sizzle and become fragrant.",
        "Add the harder vegetables first (carrots, broccoli) and toss for 2 minutes. Then add softer vegetables (bell pepper, snap peas) and toss for another 2 minutes.",
        "Return the cooked chicken to the wok. Pour the sauce over everything. Toss rapidly for 1–2 minutes until every piece is coated and the sauce slightly thickens.",
        "Remove from heat and drizzle with a tiny bit more sesame oil. Serve immediately over steamed white or brown rice, garnished with sesame seeds or sliced spring onions."
    ],
    "prep_time": "15 mins",
    "protein": 40, "carbs": 45, "fat": 12, "calories": 500
},


 # DINNER 
{
    "id": 17,
    "type": "dinner",
    "name": "Steak & Sweet Potato",
    "image": "https://plus.unsplash.com/premium_photo-1672199330043-d6d2690229e9?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8U3RlYWslMjAlMjYlMjBTd2VldCUyMFBvdGF0b3xlbnwwfHwwfHx8MA%3D%3D",
    "ingredients": [
        "1 ribeye or sirloin steak (200g)",
        "1 medium sweet potato",
        "1 tbsp olive oil",
        "Rosemary, thyme",
        "Salt & coarse black pepper",
        "Garlic butter"
    ],
    "instructions":[
        "Preheat your oven to 400°F (200°C). Scrub the sweet potato clean, pierce it all over with a fork, rub with a little olive oil and salt, and place directly on the oven rack. Bake for 40–45 minutes until fork-tender all the way through.",
        "While the potato bakes, take the steak out of the fridge 30 minutes before cooking to bring it to room temperature — this ensures even cooking.",
        "Pat the steak completely dry with paper towels (moisture is the enemy of a good sear). Season very generously on both sides with coarse salt and cracked black pepper.",
        "Heat a cast-iron skillet over HIGH heat for 3–4 minutes until it's ripping hot. Add 1 tablespoon of olive oil.",
        "Lay the steak in the pan away from you. For medium-rare on a 1-inch steak: sear for 3–4 minutes without touching. Flip ONCE and cook another 3–4 minutes.",
        "In the last minute, add a knob of butter, 2 garlic cloves (smashed), and a sprig of rosemary to the pan. Tilt the pan and continuously baste the steak with the foaming garlic butter using a spoon.",
        "Remove the steak to a cutting board and tent loosely with foil. REST for 5–10 minutes — this is non-negotiable for a juicy steak.",
        "Slice the baked sweet potato open and fluff the inside with a fork. Add a small knob of butter, a pinch of cinnamon and salt.",
        "Slice the steak against the grain. Plate alongside the sweet potato. Spoon any remaining garlic butter from the pan over the steak. Serve immediately."
    ],
    "prep_time": "40 mins",
    "protein": 55, "carbs": 70, "fat": 20, "calories": 700
},
{
    "id": 18,
    "type": "dinner",
    "name": "Grilled Salmon Plate",
    "image": "https://images.unsplash.com/photo-1676300185165-3f543c1fcb72?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8R3JpbGxlZCUyMFNhbG1vbiUyMFBsYXRlfGVufDB8fDB8fHww",
    "ingredients": [
        "2 salmon fillets (150g each)",
        "1 lemon",
        "2 cups asparagus or green beans",
        "Olive oil",
        "Garlic, fresh dill",
        "Salt & pepper"
    ],
    "instructions": [
        "Remove salmon from the fridge 15 minutes before cooking. Pat completely dry with paper towels — this is essential for a crispy skin.",
        "Drizzle both sides with olive oil and season generously with salt, pepper, and minced garlic. Lay a few sprigs of fresh dill on top.",
        "Prep the vegetables: trim the woody ends off asparagus or top-and-tail green beans. Toss with olive oil, salt, and pepper.",
        "Preheat your grill or grill pan over medium-high heat until very hot. Brush lightly with oil.",
        "Place the salmon fillets skin-side DOWN on the grill. Do not move them. Cook for 4–5 minutes until the skin is crispy and the sides are turning opaque halfway up.",
        "Carefully flip the salmon using a wide spatula. Cook for another 2–3 minutes. The salmon is perfect when it flakes easily but still has a slightly translucent center.",
        "While the salmon cooks, roast the vegetables: spread on a baking sheet, roast at 400°F for 12–15 minutes, or sauté in a pan for 5–6 minutes until tender and slightly charred.",
        "Remove salmon from the grill and let rest 2 minutes.",
        "Plate the salmon alongside the vegetables. Squeeze fresh lemon juice generously over the salmon and garnish with fresh dill. Serve immediately."
    ],
    "prep_time": "20 mins",
    "protein": 50, "carbs": 40, "fat": 18, "calories": 600
},
{
    "id": 19,
    "type": "dinner",
    "name": "Shrimp Stir Fry",
    "image": "https://images.unsplash.com/photo-1703876087121-50a1c0a00e4d?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8N3x8U2hyaW1wJTIwU3RpciUyMEZyeXxlbnwwfHwwfHx8MA%3D%3D",
    "ingredients": [
        "250g large shrimp, peeled & deveined",
        "2 cups mixed vegetables (bok choy, bell pepper, snap peas)",
        "3 tbsp soy sauce",
        "1 tbsp oyster sauce",
        "Garlic, ginger, sesame oil",
        "Cornstarch"
    ],
    "instructions": [
        "Pat the shrimp dry with paper towels and season lightly with salt and pepper. Toss with 1 teaspoon of cornstarch — this helps them get a better sear.",
        "Mix the sauce: combine soy sauce, oyster sauce, 1 teaspoon of sesame oil, 1 teaspoon of cornstarch, and 2 tablespoons of water in a small bowl. Set aside.",
        "Chop all vegetables into similar-sized pieces. Mince the garlic and grate the ginger.",
        "Heat a wok or large skillet over HIGH heat until smoking. Add 1 tablespoon of vegetable oil.",
        "Add the shrimp in a single layer. Cook undisturbed for 90 seconds until they curl and turn pink on one side. Flip each shrimp and cook 60 more seconds. Remove from the wok immediately — do not overcook.",
        "Add another splash of oil to the wok. Add garlic and ginger, stir for 30 seconds until fragrant.",
        "Add the harder vegetables first (bell pepper, snap peas) and stir fry for 2 minutes on high heat. Add bok choy last and cook for 1 minute.",
        "Pour the sauce over the vegetables and toss to coat. Let it bubble for 30 seconds until slightly thickened.",
        "Return the cooked shrimp to the wok and toss everything together for 30 seconds. Drizzle with sesame oil. Serve immediately over steamed rice, garnished with sesame seeds and sliced spring onions."
    ],
    "prep_time": "15 mins",
    "protein": 40, "carbs": 50, "fat": 12, "calories": 500
},
{
    "id": 20,
    "type": "dinner",
    "name": "Beef & Veggies",
    "image": "https://images.unsplash.com/photo-1723531055852-744d14ac00b4?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8QmVlZiUyMCUyNiUyMFZlZ2dpZXN8ZW58MHx8MHx8fDA%3D",
    "ingredients": [
        "200g lean beef strips",
        "2 cups mixed vegetables (zucchini, mushrooms, bell pepper)",
        "2 tbsp Worcestershire sauce",
        "1 onion, sliced",
        "2 garlic cloves",
        "Olive oil, salt & pepper"
    ],
    "instructions": [
        "Slice the beef into thin strips against the grain for tenderness. Season with salt and pepper and toss with 1 teaspoon of cornstarch to help brown.",
        "Prep all vegetables: slice the zucchini into half-moons, slice mushrooms, and cut bell pepper into strips. Slice the onion into thin wedges.",
        "Heat a large skillet or wok over HIGH heat. Add 1 tablespoon of olive oil.",
        "Add the beef strips in a single layer — do not overcrowd or they'll steam instead of sear. Sear for 2 minutes without moving, then toss for 1 more minute. Remove and set aside.",
        "Reduce heat to medium-high. Add another drizzle of oil. Add the onion and cook for 3 minutes until it softens and begins to caramelize.",
        "Add the garlic and cook for 30 seconds until fragrant.",
        "Add the mushrooms first — they need the most time. Cook for 3 minutes until golden. Then add bell pepper and zucchini. Stir fry for 3–4 minutes until just tender.",
        "Return the beef strips to the pan. Add Worcestershire sauce and stir everything together vigorously for 1–2 minutes so the sauce coats every piece.",
        "Taste and adjust seasoning with salt and pepper. Serve immediately over mashed sweet potato, rice, or steamed greens."
    ],
    "prep_time": "20 mins",
    "protein": 50, "carbs": 30, "fat": 18, "calories": 550
},

#  SNACKS 
{
    "id": 21,
    "type": "snack",
    "name": "Greek Yogurt Bowl",
    "image": "https://images.unsplash.com/photo-1530259152377-3a014e1092e0?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8R3JlZWslMjBZb2d1cnQlMjBCb3dsfGVufDB8fDB8fHww",
    "ingredients": [
        "1 cup Greek yogurt",
        "2 tbsp mixed nuts (almonds, walnuts)",
        "1 tsp honey",
        "Pinch of cinnamon"
    ],
    "instructions": [
        "Choose a thick, high-protein Greek yogurt — full-fat or 2% gives the best texture and richness.",
        "Spoon the yogurt into a bowl and smooth the top with the back of your spoon.",
        "Roughly chop or crush the mixed nuts for better distribution and easier eating.",
        "Scatter the nuts over the surface of the yogurt.",
        "Drizzle 1 teaspoon of honey over the nuts in a spiral pattern.",
        "Finish with a light pinch of ground cinnamon — this adds warmth and pairs perfectly with the honey.",
        "Optional additions: a few dark chocolate chips, seeds (flax or hemp), or fresh berries.",
        "Serve immediately. Do not let it sit too long or it may become watery."
    ],
    "prep_time": "2 mins",
    "protein": 30, "carbs": 20, "fat": 10, "calories": 350
},
{
    "id": 22,
    "type": "snack",
    "name": "Protein Shake",
    "image": "https://plus.unsplash.com/premium_photo-1726765808183-9c3d6a119000?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTd8fHByb3RlaW4lMjBzaGFrZXJ8ZW58MHx8MHx8fDA%3D",
    "ingredients": [
        "1 scoop protein powder",
        "1 cup cold milk or almond milk",
        "1/2 cup ice cubes",
        "Optional: 1 tbsp cocoa powder or 1/2 banana"
    ],
    "instructions": [
        "Pour the cold milk or almond milk into your blender or shaker bottle first to prevent powder from clumping.",
        "Add one level scoop of your chosen protein powder. Vanilla and chocolate are the most versatile flavors.",
        "If using a blender, add ice cubes and any optional additions (banana, cocoa powder, nut butter).",
        "If using a shaker bottle: add the protein powder to the liquid, seal tightly, and shake vigorously for 20–30 seconds.",
        "If using a blender: blend on high for 45–60 seconds until completely smooth and frothy.",
        "Pour into a chilled glass for best experience.",
        "Consume within 30 minutes of mixing for optimal protein utilization. Great as a post-workout snack."
    ],
    "prep_time": "1 min",
    "protein": 35, "carbs": 25, "fat": 12, "calories": 400
},
{
    "id": 23,
    "type": "snack",
    "name": "Tuna Salad",
    "image": "https://images.unsplash.com/photo-1604909052743-94e838986d24?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8dHVuYSUyMHNhbGFkfGVufDB8fDB8fHww",
    "ingredients": [
        "1 can tuna in water, drained",
        "1/4 cup cherry tomatoes, halved",
        "1/4 cucumber, diced",
        "1 tbsp olive oil",
        "Lemon juice",
        "Salt & pepper"
    ],
    "instructions": [
        "Drain the canned tuna completely and transfer to a mixing bowl.",
        "Flake the tuna with a fork until it's broken into small, even pieces.",
        "Halve the cherry tomatoes and dice the cucumber into small cubes. Add to the bowl.",
        "Drizzle 1 tablespoon of olive oil over the mixture.",
        "Squeeze fresh lemon juice over everything — about half a lemon.",
        "Season with salt and freshly cracked black pepper.",
        "Toss gently until everything is combined and evenly dressed.",
        "Taste and adjust with more lemon or seasoning.",
        "Serve with whole grain crackers, over lettuce leaves, or as a dip with vegetable sticks. Can be made ahead and refrigerated for up to 24 hours."
    ],
    "prep_time": "5 mins",
    "protein": 40, "carbs": 10, "fat": 8, "calories": 300
},
{
    "id": 24,
    "type": "snack",
    "name": "Cottage Cheese & Fruit",
    "image": "https://images.unsplash.com/photo-1631718051263-c567dca19362?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8Q290dGFnZSUyMENoZWVzZSUyMCUyNiUyMEZydWl0fGVufDB8fDB8fHww",
    "ingredients": [
        "1 cup cottage cheese",
        "1 apple, sliced",
        "1 tsp honey",
        "Pinch of cinnamon"
    ],
    "instructions": [
        "Choose a high-protein cottage cheese — small curd or large curd both work well.",
        "Spoon the cottage cheese into a bowl and smooth it out.",
        "Wash and core the apple, then slice into thin wedges or rings.",
        "Arrange the apple slices in a fan pattern around or alongside the cottage cheese.",
        "Drizzle honey over both the cottage cheese and apple slices.",
        "Sprinkle a pinch of ground cinnamon over the top.",
        "Optional: add a few walnuts, raisins, or a sprinkle of granola for extra texture.",
        "Serve immediately. This pairs especially well as a mid-afternoon or post-workout snack."
    ],
    "prep_time": "2 mins",
    "protein": 28, "carbs": 30, "fat": 5, "calories": 280
},
{
    "id": 25,
    "type": "snack",
    "name": "Peanut Butter Apple",
    "image": "https://plus.unsplash.com/premium_photo-1699150949538-60bdfd8dccb8?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8UGVhbnV0JTIwQnV0dGVyJTIwQXBwbGV8ZW58MHx8MHx8fDA%3D",
    "ingredients": [
        "1 large apple (Fuji, Honeycrisp, or Gala)",
        "3 tbsp natural peanut butter",
        "Optional: granola, raisins, honey"
    ],
    "instructions": [
        "Wash the apple thoroughly under cool running water.",
        "Cut the apple in half, then core each half using a spoon or corer.",
        "Slice each half into 6–8 even wedges for easy dipping.",
        "Optional: rub the cut surfaces with a tiny bit of lemon juice to prevent browning if making ahead.",
        "Spoon natural peanut butter into a small bowl for dipping. If the peanut butter is very thick, stir in a few drops of water to loosen it.",
        "For an extra treat: drizzle honey over the peanut butter and top with a pinch of granola or raisins.",
        "Arrange the apple slices around the dipping bowl on a plate.",
        "Dip, eat, and enjoy! This snack provides a great balance of fiber, natural sugars, and healthy fats."
    ],
    "prep_time": "3 mins",
    "protein": 15, "carbs": 35, "fat": 12, "calories": 300
},
{
    "id": 26,
    "type": "snack",
    "name": "Boiled Eggs",
    "image": "https://images.unsplash.com/photo-1482049016688-2d3e1b311543?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8Qm9pbGVkJTIwRWdnc3xlbnwwfHwwfHx8MA%3D%3D",
    "ingredients": [
        "2–4 large eggs",
        "Water",
        "Salt (for seasoning)",
        "Optional: hot sauce or everything bagel seasoning"
    ],
    "instructions": [
        "Take the eggs out of the fridge 10 minutes before boiling to reduce the risk of cracking.",
        "Fill a saucepan with enough water to cover the eggs by at least 1 inch. Bring to a full rolling boil over high heat.",
        "Using a spoon, gently lower the eggs into the boiling water one by one. Reduce heat to a gentle boil (medium).",
        "Set a timer based on your preferred doneness: 6 minutes for a jammy/soft yolk, 8 minutes for a custardy medium yolk, 10–12 minutes for a fully hard-boiled yolk.",
        "While eggs cook, prepare an ice bath: fill a large bowl with cold water and plenty of ice cubes.",
        "When the timer goes off, immediately transfer the eggs to the ice bath using a slotted spoon. Let them sit for at least 5 minutes — this stops cooking and makes peeling much easier.",
        "To peel: tap each egg gently all over on the counter to crack the shell, then peel under a thin stream of running water for the easiest removal.",
        "Slice in half, sprinkle with salt and pepper, and optionally add a few drops of hot sauce or a pinch of everything bagel seasoning.",
        "Eat immediately or store unpeeled in the fridge for up to 5 days for a ready-to-eat high-protein snack."
    ],
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


#GET ALL MEALS
@router.get("/")
def get_meals(db: SessionDep):
    seed_meals(db)
    return db.exec(select(Meal)).all()


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
 

