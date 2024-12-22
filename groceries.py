from flask import Flask, request, render_template, url_for
import sqlite3

app = Flask(__name__)

# creating all databases
db = sqlite3.connect('groceries.db') # connect to database
cursor = db.cursor()

create_recipe = '''CREATE TABLE IF NOT EXISTS "Recipe" (
	"ID"	INTEGER,
	"DishName"	TEXT,
	PRIMARY KEY("ID" AUTOINCREMENT))'''
create_one_recipe = '''CREATE TABLE IF NOT EXISTS "OneRecipe" (
	"ID"	INTEGER,
	"Ingredients"	TEXT,
	"Weight"	TEXT,
	"RecipeID"	INTEGER,
	PRIMARY KEY("ID" AUTOINCREMENT),
	FOREIGN KEY("recipeID") REFERENCES "Recipe"("ID"))'''
create_weekly_planner = '''CREATE TABLE IF NOT EXISTS "WeeklyPlanner" (
	"Day"	TEXT UNIQUE,
	"RecipeID"	INTEGER,
	"Quantity"  INTEGER,
	FOREIGN KEY("recipeID") REFERENCES "Recipe"("ID"))'''
create_groceries = '''CREATE TABLE IF NOT EXISTS "Groceries" (
	"Item"	TEXT,
	"Weight"    TEXT)'''
create_list = [create_recipe, create_one_recipe, create_weekly_planner, create_groceries]

for create in create_list:
    db.execute(create)

db.commit() # saves the database
db.close() # closes the database


# adding to database
def add_recipe(name, ingredients):
    '''this function takes in the name of the recipe and a dictionary containing ingredients as keys and weight as values
        and adds the key-value pairs into database'''
    db = sqlite3.connect('groceries.db') # connect to database
    cursor = db.cursor()

    # insert name of recipe
    db.execute('INSERT INTO Recipe(DishName) VALUES(?)', (name,))

    # insert ingredients of recipe
    recipeID = cursor.execute('SELECT ID FROM Recipe WHERE Recipe.DishName = ?', (name,)).fetchone()[0] # get recipe ID 
    for ingredient in ingredients:
        insert = '''INSERT INTO OneRecipe(Ingredients, Weight, RecipeID)
                    VALUES(?,?,?)'''
        print(ingredient, ingredients[ingredient], recipeID)
        db.execute(insert, (ingredient, ingredients[ingredient], recipeID))

    db.commit() # saves the database
    db.close() # closes the database
        

# viewing the recipe from database
def view_recipe():
    db = sqlite3.connect('groceries.db') # connect to database
    cursor = db.cursor()

    # retrieve all recipes from Recipe table
    recipe_list = cursor.execute('SELECT DishName FROM Recipe').fetchall()

    db.commit() # saves the database
    db.close() # closes the database
    
    # returns a list of recipes
    return recipe_list


# viewing ingredients in recipe
def view_one_recipe():
    db = sqlite3.connect('groceries.db') # connect to database
    cursor = db.cursor()

    # retrieve all ingredients and weights required from OneRecipe table 
    ingredients_list = cursor.execute('SELECT Ingredients, Weight FROM OneRecipe').fetchall()
    db.commit() # saves database 
    db.close() # closes the database
    
    # returns a list of ingredients
    return ingredients_list


# add weekly planner to save into database
def add_weekly_planner(plans):
    '''this function takes in a list where the keys are names of the day and the values
        are a list containing the dish name and servings of each dish for the day to be consummed'''
    db = sqlite3.connect('groceries.db') # connect to database

    # adds the days into database
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for day in days:
        db.execute('''INSERT OR IGNORE INTO WeeklyPlanner(Day) VALUES(?)''', (day,))

    # adds data into WeeklyPlanner
    for day in plans:
        recipeID = db.execute('SELECT ID FROM Recipe WHERE DishName = ?', (plans[day][0],)).fetchone()[0]
        query = '''INSERT OR REPLACE INTO WeeklyPlanner(Day, RecipeID, Quantity) VALUES(?,?,?)'''
        db.execute(query, (day, recipeID, plans[day][1]))

    db.commit() # saves the database
    db.close() # closes the database
    

# view the making of weekly planner
def view_weekly_planner():
    db = sqlite3.connect('groceries.db') # connect to database
    cursor = db.cursor()
    query = '''SELECT WeeklyPlanner.Day, Recipe.DishName, WeeklyPlanner.Quantity
                FROM WeeklyPlanner, Recipe
                WHERE Recipe.ID = WeeklyPlanner.RecipeID'''
    weekly_planner = cursor.execute(query).fetchall()
    db.commit() # saves the database
    db.close() # closes the database

    # returns the list weekly_planner
    return weekly_planner

# adding the groceries together...
def adding_groceries(data):
    '''this function takes in an unknown data type and returns a dictionary'''
    grocery_list = {}
    # loop through data

    # check if data exists
    pass

# add groceries
def add_groceries(grocery_list):
    db = sqlite3.connect('groceries.db')

    # removes all data in table
    db.execute('TRUNCATE TABLE Groceries')

    # insert data into Groceries 
    query = '''INSERT INTO''' ### INCOMPLETE
    for ingredient in grocery_list:  
        db.execute(query, (ingredient, grocery_list[ingredient]))
    db.commit() # saves the database
    db.close() # closes the database 

# view groceries
def view_groceries():
    db = sqlite3.connect('groceries.db') # connect to database
    query = '''SELECT * FROM Groceries'''
    groceries = db.execute(query).fetchall()
    db.commit() # saves the database
    db.close() # closes the database
    return groceries



# home page of webapp
# has three buttons: weekly meal planner, profile, groceries
@app.route("/")
def home():
    # buttons is on html file
    return render_template("Home.html")


# weekly meal planner
# has three buttons: create new recipe, saved recipes (save in db browser), "save" (redirects to groceries page)
# displays a page that allows user to input (form)... what
@app.route("/weeklymealplanner")
def weekly_meal_planner():
    return render_template("mealplanwkly.html")



# create new recipe
# name: a field that stores name of dish
# cross: goes back to weeklymealplanner
# save: goes back to weeklymealplanner + save to database 
# insredients, quantity: how...
@app.route("/create", methods=["POST", "GET"])
def create():
    if request.method == 'POST': # user clicked on save recipe button
        # insert code to save the recipe into database
        pass
        '''
        recipe_name = request.form['name']
        ingredients = request.form['ingredients']
        quantity = request.form['quantity']
        print(ingredients)
        print(quantity)
        '''
        
        return weekly_meal_planner()
        
    
    return render_template("CreateRecipe.html")


# saved recipes
# views all existing saved recipe (they are buttons to redirect to recipe)
@app.route("/viewsavedrecipes", methods=["GET", "POST"])
def view_all():
    return render_template("Recipe.html", recipe_list=view_recipe())

# viewing of ONE recipe
# displaying purposes
# has three buttons: edit, delete (redirects back to saved recipes), back (redirects to saved recipes) 
@app.route("/viewonerecipe")
def view_one():
    return render_template("Recipesaved1.html", view_all=view_all(), view_ingredients=view_one_recipe())


# groceries page
@app.route("/groceries")
def groceries():
    # use a for loop, dictionary to calculate the total amount of groceries the user needs to buy 


    return render_template("GroceryPlannerDisplay.html")



if __name__ == "__main__":
    app.run()
