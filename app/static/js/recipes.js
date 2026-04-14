const API_BASE = "/api/meals";

// Load all meals
async function loadMeals() {
    const res = await fetch(API_BASE);
    const meals = await res.json();
    renderMeals(meals);
}

// Filter meals
async function filterMeals(type) {
    const res = await fetch(`${API_BASE}/type/${type}`);
    const meals = await res.json();
    renderMeals(meals);
}

// Render meals to UI
function renderMeals(meals) {
    const container = document.getElementById("meals-container");
    container.innerHTML = "";

    meals.forEach(meal => {
        container.innerHTML += `
        <div class="card" style="width:250px; padding:10px;">
            
            <img src="${meal.image}" style="width:100%; height:150px; object-fit:cover;">
            
            <h5>${meal.name}</h5>
            <p>${meal.calories} kcal</p>

            <button onclick="addToTracker(${meal.id})" class="btn btn-success">
                Add to Tracker
            </button>

        </div>
        `;
    });
}

async function addToTracker(mealId) {
    await fetch(`/api/tracker/add/${mealId}`, {
        method: "POST"
    });

    // UX feedback
    M.toast({ html: "Added to tracker!" });

    // OPTIONAL: redirect
    // window.location.href = "/api/tracker/trackcalories";
}

// View single meal (expand or alert for now)
async function viewMeal(id) {
    const res = await fetch(`${API_BASE}/${id}`);
    const meal = await res.json();

    alert(`
${meal.name}

Ingredients:
${meal.ingredients.join(", ")}

Instructions:
${meal.instructions}
    `);
}

// Load on page start
document.addEventListener("DOMContentLoaded", loadMeals);