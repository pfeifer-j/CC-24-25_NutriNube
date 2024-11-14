//app/static/app.js
let calorieGoal = 0;
let proteinGoal = 0;
let fatGoal = 0;
let carbsGoal = 0;
let totalCaloriesConsumed = 0;
let totalCaloriesBurned = 0;
let selectedDate = localStorage.getItem('selectedDate') || new Date().toISOString().split('T')[0];

const foodData = {
    date: selectedDate,  
    calories: parseInt($('#calories_consumed').val(), 10),
    protein: parseInt($('#protein_consumed').val(), 10),
    fat: parseInt($('#fat_consumed').val(), 10),
    carbs: parseInt($('#carbs_consumed').val(), 10)
};

const fitnessData = {
    date: selectedDate, 
    exercise: $('#exercise').val(),
    kcal_burned: parseInt($('#kcal_burned').val(), 10)
};


$(document).ready(function() {
    if (typeof jQuery !== 'undefined') {
        console.log('jQuery is loaded');
    }

    // Set the date picker to the stored date or default to today
    $('#date-picker').val(selectedDate);

    // Display the stored or default date
    $('#selected-date').text(new Date(selectedDate).toLocaleDateString());

    // Fetch data for the selected date
    fetchUserData();

    $('#date-picker').on('change', function() {
        selectedDate = $(this).val();
        localStorage.setItem('selectedDate', selectedDate);
        $('#selected-date').text(new Date(selectedDate).toLocaleDateString());
        fetchUserData();
    });

    // Submit handler for login form
    $('#login-form').on('submit', function(e) {
        e.preventDefault();
        const username = $('#login-username').val();
        const password = $('#login-password').val();

        $.ajax({
            type: 'POST',
            url: '/login',
            data: {
                username: username,
                password: password
            },
            success: function(response) {
                // Handle successful login (e.g., redirect to the homepage)
                window.location.href = '/'; 
            },
            error: function(xhr) {
                // Handle error: Display the error message
                const response = xhr.responseJSON;
                showToast(response.error || 'Login failed. Please try again.');
            }
        });
    });

    // Submit handler for register form
    $('#register-form').on('submit', function(e) {
        e.preventDefault();
        const username = $('#register-username').val();
        const password = $('#register-password').val();
    
        $.ajax({
            type: 'POST',
            url: '/register',
            data: { username: username, password: password },
            success: function(response) {
                showToast(response.message);
                $('#register-username').val('');
                $('#register-password').val('');
            },
            error: function(xhr) {
                const response = xhr.responseJSON;
                showToast(response.error || 'Failed to register. Please try again.');
            }
        });
    });

    $('#logout-form').on('submit', function(e) {
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/logout',
            success: function(response) {
                showToast(response.message);
                window.location.href = '/login';
            },
            error: function(xhr) {
                showToast('Failed to logout. Please try again.');
            }
        });
    });

    function fetchUserData() {
        $.ajax({
            type: 'GET',
            url: '/daily-summary',
            data: { date: selectedDate },
            success: function(response) {
                calorieGoal = response.calories_goal;
                proteinGoal = response.protein_goal;
                fatGoal = response.fat_goal;
                carbsGoal = response.carbs_goal;
                totalCaloriesConsumed = response.total_calories_consumed;
                totalCaloriesBurned = response.total_calories_burned;

                const totalProteinConsumed = response.total_protein;
                const totalFatConsumed = response.total_fat;
                const totalCarbsConsumed = response.total_carbs;

                // Clear and populate food data
                const foodList = $('#food-list tbody').empty();
                response.food_log.forEach(function(item) {
                    foodList.append(`
                        <tr data-id="${item.id}">
                            <td>${item.food}</td>
                            <td>${item.calories}</td>
                            <td>${item.protein}</td>
                            <td>${item.fat}</td>
                            <td>${item.carbs}</td>
                            <td>
                                <button class="delete-food">Delete</button>
                            </td>
                        </tr>
                    `);
                });

                // Clear and populate fitness data
                const fitnessList = $('#fitness-list tbody').empty();
                response.fitness_log.forEach(function(item) {
                    fitnessList.append(`
                        <tr data-id="${item.id}">
                            <td>${item.exercise}</td>
                            <td>${item.kcal_burned}</td>
                            <td>
                                <button class="delete-fitness">Delete</button>
                            </td>
                        </tr>
                    `);
                });

                // Register click handlers
                $('.delete-food').click(deleteFood);
                $('.delete-fitness').click(deleteFitness);

                updateDisplay(totalProteinConsumed, totalFatConsumed, totalCarbsConsumed);
            },
            error: function(xhr) {
                showToast('Failed to load user data. Please try again.');
            }
        });
    }

    document.addEventListener("DOMContentLoaded", function() {
        // Fetch the current values displayed on the page
        const calorieGoalText = document.getElementById('calories-goal-text').textContent;
        const proteinGoalText = document.getElementById('protein-goal-text').textContent;
        const fatGoalText = document.getElementById('fat-goal-text').textContent;
        const carbsGoalText = document.getElementById('carbs-goal-text').textContent;
    
        // Set the input fields' value attribute to match the current goals
        document.getElementById('calorie_goal').value = calorieGoalText;
        document.getElementById('protein_goal').value = proteinGoalText;
        document.getElementById('fat_goal').value = fatGoalText;
        document.getElementById('carbs_goal').value = carbsGoalText;
    });

    // Submit handler for goal form
    $('#goal-form').on('submit', function(e) {
        e.preventDefault();
        const newCalorieGoal = parseInt($('#calorie_goal').val(), 10);
        const newProteinGoal = parseInt($('#protein_goal').val(), 10);
        const newFatGoal = parseInt($('#fat_goal').val(), 10);
        const newCarbsGoal = parseInt($('#carbs_goal').val(), 10);

        if (isNaN(newCalorieGoal) || newCalorieGoal <= 0 || isNaN(newProteinGoal) || newProteinGoal <= 0 ||
            isNaN(newFatGoal) || newFatGoal <= 0 || isNaN(newCarbsGoal) || newCarbsGoal <= 0) {
            showToast("Please enter valid goals for all fields.");
            return;
        }

        $.ajax({
            type: 'POST',
            url: '/api/update-goal',
            data: JSON.stringify({ 
                calorie_goal: newCalorieGoal,
                protein_goal: newProteinGoal,
                fat_goal: newFatGoal,
                carbs_goal: newCarbsGoal
            }),
            contentType: 'application/json',
            success: function(response) {
                showToast(response.message);
                fetchUserData();
                clearGoalInput();
            },
            error: function(xhr) {
                showToast('Failed to update goals. Please try again.');
            }
        });
    });

    $('#food-form').on('submit', function(e) {
        e.preventDefault();
        const originalIndex = $(this).data('originalIndex');
        let food_name = $('#food').val();
        
        const foodData = {
            food: food_name,
            calories: parseInt($('#calories_consumed').val(), 10),
            protein: parseInt($('#protein_consumed').val(), 10),
            fat: parseInt($('#fat_consumed').val(), 10),
            carbs: parseInt($('#carbs_consumed').val(), 10),
            date: selectedDate
        };
    
        // Validate input
        if (isNaN(foodData.calories) || isNaN(foodData.protein) || isNaN(foodData.fat) || isNaN(foodData.carbs)) {
            showToast("Please enter valid numbers for calories and macronutrients.");
            return;
        }
    
        let method = 'POST';
        let url = '/api/food';
    
        if (originalIndex !== undefined) {
            method = 'PUT';
            url = '/api/food/update';
            foodData.original_index = originalIndex;
        }
        
        $.ajax({
            type: method,
            url: url,
            data: JSON.stringify(foodData),
            contentType: 'application/json',
            success: function(response) {
                showToast(method === 'PUT' ? 'Food updated successfully.' : 'Food added successfully.');
                fetchUserData();
                clearFoodInputs();
                $('#food-form').removeData('originalIndex');
            },
            error: function(xhr) {
                showToast('Failed to process food item. Please try again.');
            }
        });
    });

    $('#fitness-form').on('submit', function(e) {
        e.preventDefault();
        const originalIndex = $(this).data('originalIndex');
        
        const fitnessData = {
            exercise: $('#exercise').val(),
            kcal_burned: parseInt($('#kcal_burned').val(), 10),
            date: selectedDate
        };
    
        // Validate input
        if (isNaN(fitnessData.kcal_burned)) {
            showToast("Please enter a valid number for calories burned.");
            return;
        }
    
        let method = 'POST';
        let url = '/api/fitness';
    
        if (originalIndex !== undefined) {
            method = 'PUT';
            url = '/api/fitness/update';
            fitnessData.original_index = originalIndex;
        }
    
        $.ajax({
            type: method,
            url: url,
            data: JSON.stringify(fitnessData),
            contentType: 'application/json',
            success: function(response) {
                showToast(method === 'PUT' ? 'Exercise updated successfully.' : 'Exercise added successfully.');
                fetchUserData();
                clearFitnessInputs();
                $('#fitness-form').removeData('originalIndex');
            },
            error: function(xhr) {
                showToast('Failed to process exercise. Please try again.');
            }
        });
    });

    function deleteFood() {
        const row = $(this).closest('tr');
        const foodId = row.data('id');
        
        $.ajax({
            type: 'DELETE',
            url: '/api/food',
            data: JSON.stringify({ food_id: foodId }),
            contentType: 'application/json',
            success: function(response) {
                showToast('Food deleted successfully.');
                fetchUserData();
            },
            error: function(xhr) {
                showToast('Failed to delete food item. Please try again.');
            }
        });
    }
    
    function deleteFitness() {
        const row = $(this).closest('tr');
        const fitnessId = row.data('id');

        $.ajax({
            type: 'DELETE',
            url: '/api/fitness',
            data: JSON.stringify({ fitness_id: fitnessId }),
            contentType: 'application/json',
            success: function(response) {
                showToast('Exercise deleted successfully.');
                fetchUserData();
            },
            error: function(xhr) {
                showToast('Failed to delete exercise. Please try again.');
            }
        });
    }

    // Clear goal input
    function clearGoalInput() {
        $('#calorie_goal').val('');
        $('#protein_goal').val('');
        $('#fat_goal').val('');
        $('#carbs_goal').val('');
    }

    // Clear food inputs
    function clearFoodInputs() {
        $('#food').val('');  
        $('#calories_consumed').val('');  
        $('#protein_consumed').val('');  
        $('#fat_consumed').val('');  
        $('#carbs_consumed').val('');  
    }

    // Clear fitness inputs
    function clearFitnessInputs() {
        $('#exercise').val('');  
        $('#kcal_burned').val('');  
    }

    // Update display
    function updateDisplay(totalProtein, totalFat, totalCarbs) {
        $('#calories-goal-text').text(calorieGoal);
        $('#protein-goal-text').text(proteinGoal);
        $('#fat-goal-text').text(fatGoal);
        $('#carbs-goal-text').text(carbsGoal);
        $('#total-calories-consumed').text(totalCaloriesConsumed);
        $('#total-protein-consumed').text(totalProtein);
        $('#total-fat-consumed').text(totalFat);
        $('#total-carbs-consumed').text(totalCarbs);
        $('#total-calories-burned').text(totalCaloriesBurned);
        $('#net-calories').text(totalCaloriesConsumed - totalCaloriesBurned);
        $('#calories-remaining').text(calorieGoal - (totalCaloriesConsumed - totalCaloriesBurned));
    }

    // Show toast message
    function showToast(message) {
        const toast = $('<div class="toast"></div>').text(message);
        $('#toast-container').append(toast);
        toast.addClass('show');

        setTimeout(() => {
            toast.removeClass('show');
            setTimeout(() => {
                toast.remove(); 
            }, 500);
        }, 3000);
    }
});