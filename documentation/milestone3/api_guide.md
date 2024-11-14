# User Guide for NutriNube API Endpoints

This documentation provides a detailed overview of the API endpoints available in the NutriNube application. Each section describes the endpoint, the required parameters, and example requests and responses.

## Authentication Routes

1. Login
- Endpoint: `/login`
- Method: `GET`, `POST`
- Description: Authenticates a user and starts a session.
  
#Request Example (POST)
http
POST /login
Content-Type: application/x-www-form-urlencoded

username=johndoe&password=secretpassword


#Response Example
- Success (200):
json
{
  "message": "Successful login"
}

- Failure (401):
json
{
  "error": "Invalid username or password"
}


---

2. Register
- Endpoint: `/register`
- Method: `POST`
- Description: Registers a new user.

#Request Example
http
POST /register
Content-Type: application/x-www-form-urlencoded

username=johndoe&password=secretpassword


#Response Example
- Success (201):
json
{
  "message": "User registered successfully!"
}

- Failure (400):
json
{
  "error": "Username and password must be provided."
}


---

3. Logout
- Endpoint: `/logout`
- Method: `POST`
- Description: Logs out the current user by destroying the session.

#Request Example
http
POST /logout


#Response Example
- Success (200):
json
{
  "message": "Logged out successfully"
}


---

## Protected Routes (requires authentication)

4. Home
- Endpoint: `/`
- Method: `GET`
- Description: Renders the home dashboard. Requires user to be logged in.

#Response Example
- Success (200): Renders the dashboard page.

---

5. Dashboard
- Endpoint: `/dashboard`
- Method: `GET`
- Description: Renders the user dashboard page. User must be logged in.

#Response Example
- Success (200): Renders the dashboard page.

---

6. Goals
- Endpoint: `/goals`
- Method: `GET`
- Description: Renders the page for user goals management. Requires authentication.

#Response Example
- Success (200): Renders the goals management page.

---

7. Foods
- Endpoint: `/foods`
- Method: `GET`
- Description: Renders the foods page where a user can manage their food logs. Requires authentication.

#Response Example
- Success (200): Renders the foods management page.

---

8. Activities
- Endpoint: `/activities`
- Method: `GET`
- Description: Renders the activities page. Requires authentication.

#Response Example
- Success (200): Renders the activities management page.

---

9. Summary
- Endpoint: `/summary`
- Method: `GET`
- Description: Renders the summary page for tracking progress. Requires authentication.

#Response Example
- Success (200): Renders the summary page.

---

## API Endpoints for Data Management

10. Update Goal
- Endpoint: `/api/update-goal`
- Method: `POST`
- Description: Updates user fitness goals.

#Request Example
http
POST /api/update-goal
Content-Type: application/json

{
  "calorie_goal": 2200,
  "protein_goal": 160,
  "fat_goal": 80,
  "carbs_goal": 300
}


#Response Example
- Success (200):
json
{
  "message": "Goals updated successfully!"
}


---

11. Add Food
- Endpoint: `/api/food`
- Method: `POST`
- Description: Adds a new food log entry for the authenticated user.

#Request Example
http
POST /api/food
Content-Type: application/json

{
  "date": "2023-10-01",
  "food": "Oatmeal",
  "calories": 150,
  "protein": 5,
  "fat": 3,
  "carbs": 27
}


#Response Example
- Success (201):
json
{
  "message": "Food added successfully!"
}

- Failure (400):
json
{
  "error": "Food name, calories, protein, fat, and carbs are required"
}


---

12. Delete Food
- Endpoint: `/api/food`
- Method: `DELETE`
- Description: Deletes a food log entry by providing the food item ID.

#Request Example
http
DELETE /api/food
Content-Type: application/json

{
  "food_id": 5
}


#Response Example
- Success (200):
json
{
  "message": "Food deleted successfully!"
}

- Failure (404):
json
{
  "error": "Food item not found!"
}


---

13. Add Fitness
- Endpoint: `/api/fitness`
- Method: `POST`
- Description: Adds a new fitness log entry.

#Request Example
http
POST /api/fitness
Content-Type: application/json

{
  "date": "2023-10-01",
  "exercise": "Running",
  "kcal_burned": 300
}


#Response Example
- Success (201):
json
{
  "message": "Exercise added successfully!"
}

- Failure (400):
json
{
  "error": "Exercise and kcal burned are required"
}


---

14. Delete Fitness
- Endpoint: `/api/fitness`
- Method: `DELETE`
- Description: Deletes a fitness log entry by providing the fitness item ID.

#Request Example
http
DELETE /api/fitness
Content-Type: application/json

{
  "fitness_id": 5
}


#Response Example
- Success (200):
json
{
  "message": "Exercise deleted successfully!"
}

- Failure (404):
json
{
  "error": "Exercise not found!"
}


---

15. Daily Summary
- Endpoint: `/daily-summary`
- Method: `GET`
- Description: Retrieves a daily summary of the user's food and fitness logs.

#Request Example
http
GET /daily-summary?date=2023-10-01


#Response Example
- Success (200):
json
{
  "calories_goal": 2000,
  "protein_goal": 150,
  "fat_goal": 70,
  "carbs_goal": 250,
  "total_calories_consumed": 1800,
  "total_calories_burned": 500,
  "net_calories": 1300,
  "total_protein": 100,
  "total_fat": 40,
  "total_carbs": 200,
  "food_log": [...],
  "fitness_log": [...]
}


- Failure (404):
json
{
  "error": "User not found"
}


---

## Conclusion

This API provides users with the ability to manage their dietary and fitness habits efficiently. Each endpoint is designed to handle specific functions, ensuring that users can log their food intake, exercise, and set goals, all while maintaining a secure environment. For further modifications or enhancements, please review each route's functionality for potential improvements or feature expansions.