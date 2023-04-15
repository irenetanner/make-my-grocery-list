'''
Create a shopping list for the week based on user-input meals.
'''
import os
import csv
import random
import reminders

def main():

    root_dir = os.getcwd()
    list_maker = GroceryListMaker(root_dir)
    list_maker.print_menu()
    
    meal_names = list_maker.get_meal_names_from_user()
    ingredients = list_maker.pull_ingredients(meal_names)
    list_maker.print_meals_for_the_week(ingredients)
    
    list_maker.make_grocery_list()

class GroceryListMaker:
    def __init__(self, root_dir):
        '''
        Load a dictionary that maps ingredients to its class.
        Create a dictionary of recipe names.
        '''
        self.root_dir = root_dir
        self.recipe_dir = os.path.join(self.root_dir, 'Recipes')
        self.ingredient_class_dict = self._get_ingredient_classes()
        #print(list(set(self.ingredient_class_dict.values())))
        self.sorted_classes = {
            'Fresh produce': 1,
            'Meat': 2,
            'Baking': 3,
            'Canned': 4,
            'Jar': 5,
            'Boxed or bagged item': 6,
            'Condiment': 7,
            'International': 8,
            'Bread': 9,
            'Frozen': 10,
            'Dairy': 11,
            'Side': 12
        }
        self.grocery_list = []
        self.recipe_dict = {}
        for i, recipe in enumerate(os.listdir(self.recipe_dir)):
            self.recipe_dict[i+1] = recipe.replace('.csv', '')

    def print_menu(self):
        '''Iterate through all recipes and print with corresonding number.'''
        print('-------------------')
        print('| Dinner Options: |')
        print('-------------------')
        for i, recipe in self.recipe_dict.items():
            print(f"[{i:02d}] {recipe}")

    def get_meal_names_from_user(self):
        '''Return a list of recipe names chosen from the menu.'''
        man_or_ran = input("\nDo you want to choose [m]anually or [r]andomly?\n")

        if man_or_ran == 'm':
            meal_nums = input(
                "Enter the number corresponding to which meals you want to make this week, separated by commas. Eg: 2,5,14,7\n")
            meal_nums = [int(x) for x in meal_nums.split(',')]
            meal_names = []
            for meal_num in meal_nums:
                meal_names.append(self.recipe_dict[meal_num])

        elif man_or_ran == 'r':
            num_meals = int(input("How many meals do you want this week?\n"))
            meal_names = random.sample(
                list(self.recipe_dict.values()), num_meals)
        
        else:
            self.get_meal_names_from_user()
        
        return meal_names
                
    def print_meals_for_the_week(self, all_ingredients):
        reminder = get_reminder(title='Meals for the Week')
        print("You've chosen:")
        
        for meal_name in all_ingredients.keys():
            print(meal_name)
            ingredients = all_ingredients[meal_name]
            meal_to_add = reminders.Reminder(reminder)
            meal_to_add.title = meal_name
            meal_to_add.notes = self._make_note(ingredients)
            meal_to_add.save()
            
            sorted_meal_ingredients = self._sort_ingredients(ingredients)
            
            for ingredient in sorted_meal_ingredients:
                print(f'   - {ingredient.quant} {ingredient.ingred}')
                
            self.grocery_list.extend(sorted_meal_ingredients)

    def pull_ingredients(self, meal_names):
        # df = pd.read_csv(os.path.join(self.recipe_dir, option))
        # ingredients = df["Ingredients"]
        all_ingredients = {}
        for meal_name in meal_names:
            recipe_file = os.path.join(self.recipe_dir, meal_name + '.csv')
            with open(recipe_file, 'r') as file:
                reader = csv.reader(file)
                ingredients = {}
                for row in reader:
                    ingredient = row[0]
                    quantity = row[1]
                    if ingredient == 'Ingredients':
                        continue
                    ingredients[ingredient] = quantity
                all_ingredients[meal_name] = ingredients
        return all_ingredients

    def add_to_reminder(self, list_to_add, title):
        reminder = get_reminder(title=title)
        for ingredient in list_to_add:
            ingred_to_add = reminders.Reminder(reminder)
            ingred_to_add.title = f'{ingredient.quant} {ingredient.ingred}'
            ingred_to_add.save()

    def make_grocery_list(self):
        sorted_grocery_list = sorted(self.grocery_list, key=lambda x: x.loc)
            
        self.add_to_reminder(sorted_grocery_list, title='Grocery List')
        
    def _make_note(self, ingredients):
        note = ''
        for ingred, quant in ingredients.items():
            note += f'{quant} {ingred}\n'
        return note

    def _get_ingredient_classes(self):
        ingredient_classes = {}
        with open('Master Ingredient List.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                ingredient = row[0]
                cls = row[1]
                ingredient_classes[ingredient] = cls
        return ingredient_classes

    def _sort_ingredients(self, ingredients):
        # classify ingredients
        ingred_obj_list = []
        for ingred, quant in ingredients.items():
            cls = self.ingredient_class_dict[ingred]
            loc = self.sorted_classes[cls]
            ingred_obj = Ingredient(ingred, cls, loc, quant)
            ingred_obj_list.append(ingred_obj)
        sorted_ingreds = sorted(ingred_obj_list, key=lambda x: x.loc)
        return sorted_ingreds
        
def create_reminder(title):
    '''Create and return a new reminder list.'''
    reminder = reminders.Calendar()
    reminder.title = title
    reminder.save()
    return reminder


def get_reminder(title):
    '''Check if the specified reminder list exists or create a new one.'''
    cals = reminders.get_all_calendars()
    cal = [cal for cal in cals if cal.title == title]
    cal = create_reminder(title) if cal == [] else cal[0]
    return cal




class Ingredient:
    def __init__(self, ingred, cls, loc, quant):
        self.ingred = ingred
        self.quant = quant
        self.cls = cls
        self.loc = loc
    
    def __repr__(self):
        return repr(f'{self.quant} {self.ingred}')

if __name__ == '__main__':
    main()

