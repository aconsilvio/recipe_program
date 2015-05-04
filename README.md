Rapid Recipes: Recipe Finder Program
Created by Annabel Consilvio, Anisha Nakagawa, and Maggie Jakus
--------------------------------------------------------------------
TO RUN:
--------------------------------------------------------------------

	-open http://rapid-recipes.herokuapp.com/ in any browser

	---or---

	-Make sure that the file structure of program on computer matches file structure on github
		(https://github.com/aconsilvio/recipe_program).
	-Run flask_recipes.py as a python file in terminal.
	-Copy the IP address (http://0.0.0.0:8081/) printed in the terminal.  It should look something like this:
		 * Running on http://0.0.0.0:8081/ (Press CTRL+C to quit)
 		 * Restarting with stat
--------------------------------------------------------------------
Design Decisions and Issues
--------------------------------------------------------------------

	- Currently, this program is able to search for recipes & correctly generate a page
		with images and text that correspond to the inputs of the user.  This only works
		for one user at a time because of our use of global variables.  In future iterations,
		we would like to change this, but the time limit of this project did not allow us
		to do so.  Currently, if multiple people try to use the program at once, the pantry
		of that user (the part that gets saved each time you run the program) could 
		accidentally get replaced by another person's pantry.  Additionally, the max total
		cook time variable may also get replaced by the other user's input.
	- Besides the problem with multiple users, we made a design decsion regarding how we
		searched for recipes that we would eventually like to change.  Yummly's
		API search function will only search for very specific items.  For example, searching
		for 'milk' returns results that does not include "whole milk", "fat free milk", "skim
		milk", etc.  In order to make our app more fucntional, we decided to search for the
		word milk in every ingredient rather than just matching ingreditents.  This works 
		pretty well for things like milk, but does present some problems for things like
		'butter' and 'oil', where our program will now return recipes including 'butter', 
		'peanut butter', 'almond butter', and 'olive oil', 'vegetable oil', 'corn oil',
		'mustard oil', etc.  Although this increases the general functionality of the app,
		it is not the best practice and we would like to fix this.
--------------------------------------------------------------------
Class Structure
--------------------------------------------------------------------

	- The class structure is contained in the recipe_program.py file. The main user class contrains a fridge and pantry, which are lists of ingredients used to search for recipes. The pantry class is saved for the specific user.

--------------------------------------------------------------------
Yummly API
--------------------------------------------------------------------

	- This API works by searching for recipes based on an ingredient; however, it gives you 
		any recipe that include this ingredient.  Because our program is designed to search
		for essentially the opposite of this, we needed to develop the following algorithm in
		order to search efficiently. 
--------------------------------------------------------------------
Algorithms
--------------------------------------------------------------------

	- The algorithm in recipe_program.py works by using the Yummly API to search for any recipes
		that have the specified ingredient in them.  The program then runs through each ingredient
		and compiles a list of recipes that have not been filtered and have many more ingredients 
		than those in your fridge and pantry.  Next, each ingredient in each recipe is cross checked
		with the list of available ingredients.  If there is an ingredient in the recipe that is not 
		in the available ingredients, the program immediately moves on to the next recipe.  If the
		recipe includes only available ingredients, it is added to a new list of recipes that are 
		suitable to show in the website.
--------------------------------------------------------------------
Heroku
--------------------------------------------------------------------
	- Heroku is the server that hosts the web application. It runs the flask file at the url rapid-recipes.herokuapp.com

--------------------------------------------------------------------
Flask
--------------------------------------------------------------------
	- Flask is an add on to Python that allows you to build a web-app with a python back-end.
		It integrates python files and html files with javascript.  You will need this to run
		the program.
--------------------------------------------------------------------
MongoDB
--------------------------------------------------------------------
	- Used as the database for storing existing users and pantries, as well as for memoizing the recipes for common ingredients. Uses MongoLab to host the database on a server.
