# User Guide for API Endpoints

This documentation provides an overview of the API endpoints available in the NutriNube application.

## Authentication Routes

1. Login
   - Endpoint: `/login`
   - Method: `GET`, `POST`
   - Description: Authenticates a user and starts a session.

---

2. Register
   - Endpoint: `/register`
   - Method: `POST`
   - Description: Registers a new user.

---

3. Logout
   - Endpoint: `/logout`
   - Method: `POST`
   - Description: Logs out the current user by destroying the session.

---

4. Home
   - Endpoint: `/`
   - Method: `GET`
   - Description: Renders the home dashboard or forwards users to `/login`.

---

## Protected Routes (requires authentication)

5. Dashboard
   - Endpoint: `/dashboard`
   - Method: `GET`
   - Description: Renders the user dashboard page. User must be logged in.

---

6. Goals
   - Endpoint: `/goals`
   - Method: `GET`
   - Description: Renders the page for user goals management. Requires authentication.

---

7. Foods
   - Endpoint: `/foods`
   - Method: `GET`
   - Description: Renders the foods page where a user can manage their food logs. Requires authentication.

---

8. Activities
   - Endpoint: `/activities`
   - Method: `GET`
   - Description: Renders the activities page. Requires authentication.

---

9. Summary
   - Endpoint: `/summary`
   - Method: `GET`
   - Description: Renders the summary page for tracking progress. Requires authentication.

---

## API Endpoints for Data Management

10. Update Goal
    - Endpoint: `/api/update-goal`
    - Method: `POST`
    - Description: Updates user fitness goals.

---

11. Add Food
    - Endpoint: `/api/food`
    - Method: `POST`
    - Description: Adds a new food log entry for the authenticated user.

---

12. Delete Food
    - Endpoint: `/api/food`
    - Method: `DELETE`
    - Description: Deletes a food log entry by providing the food item ID.

---

13. Add Fitness
    - Endpoint: `/api/fitness`
    - Method: `POST`
    - Description: Adds a new fitness log entry.

---

14. Delete Fitness
    - Endpoint: `/api/fitness`
    - Method: `DELETE`
    - Description: Deletes a fitness log entry by providing the fitness item ID.

---

15. Daily Summary
    - Endpoint: `/daily-summary`
    - Method: `GET`
    - Description: Retrieves a daily summary of the user's food and fitness logs.

---
