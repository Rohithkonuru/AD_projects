import pandas as pd

# Load the dataset
dataset_filename = "recipe_dataset.csv"

def get_ingredients(recipe_url):
    """Retrieve ingredients from the dataset based on the given recipe URL."""
    try:
        # Load the dataset
        df = pd.read_csv(dataset_filename)

        # Search for the URL
        recipe = df[df["Recipe URL"] == recipe_url]

        if recipe.empty:
            return "Recipe not found in the dataset."

        # Extract the ingredients list
        ingredients = recipe["Ingredients"].values[0].split("; ")

        return ingredients

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    # Get URL input from the user
    url = input("Enter the recipe URL: ")
    
    # Fetch ingredients
    ingredients_list = get_ingredients(url)

    # Display results
    if isinstance(ingredients_list, list):
        print("\nIngredients:")
        for ingredient in ingredients_list:
            print(f"- {ingredient}")
    else:
        print(ingredients_list)
