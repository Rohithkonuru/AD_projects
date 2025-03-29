import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud

# Load dataset
dataset_filename = "recipe_dataset.csv"
df = pd.read_csv(dataset_filename)

# Combine all ingredient lists
all_ingredients = []
for ingredients in df["Ingredients"]:
    all_ingredients.extend(ingredients.split("; "))

# Function to plot the top 10 most used ingredients
def plot_top_ingredients():
    ingredient_counts = Counter(all_ingredients)
    top_ingredients = ingredient_counts.most_common(10)  # Get top 10 ingredients

    ingredients, counts = zip(*top_ingredients)

    plt.figure(figsize=(10, 5))
    plt.barh(ingredients, counts, color="skyblue")
    plt.xlabel("Frequency")
    plt.ylabel("Ingredients")
    plt.title("Top 10 Most Used Ingredients in Recipes")
    plt.gca().invert_yaxis()
    plt.savefig("top_ingredients.png")  # Save figure
    plt.show()

# Function to plot recipe category distribution
def plot_recipe_distribution():
    categories = {
        "Pasta": ["Spaghetti", "Pasta"],
        "Soup": ["Soup"],
        "Salad": ["Salad"],
        "Dessert": ["Cookies", "Cake", "Smoothie"],
        "Meat": ["Chicken", "Beef", "Shrimp", "Salmon"],
        "Vegetarian": ["Vegetable", "Avocado"]
    }

    category_counts = {category: 0 for category in categories}

    for recipe in df["Recipe Name"]:
        for category, keywords in categories.items():
            if any(keyword in recipe for keyword in keywords):
                category_counts[category] += 1

    category_counts = {k: v for k, v in category_counts.items() if v > 0}

    plt.figure(figsize=(8, 8))
    plt.pie(category_counts.values(), labels=category_counts.keys(), autopct="%1.1f%%", 
            colors=["#ff9999","#66b3ff","#99ff99","#ffcc99","#c2c2f0","#ffb3e6"])
    plt.title("Recipe Category Distribution")
    plt.savefig("recipe_distribution.png")  # Save figure
    plt.show()

# Function to create a word cloud of ingredients
def plot_word_cloud():
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(" ".join(all_ingredients))

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("Most Common Ingredients in Recipes")
    plt.savefig("wordcloud.png")  # Save figure
    plt.show()

# Function to plot a histogram of ingredient counts per recipe
def plot_ingredient_distribution():
    ingredient_counts_per_recipe = df["Ingredients"].apply(lambda x: len(x.split("; ")))

    plt.figure(figsize=(8, 5))
    plt.hist(ingredient_counts_per_recipe, bins=10, color="purple", edgecolor="black", alpha=0.7)
    plt.xlabel("Number of Ingredients")
    plt.ylabel("Number of Recipes")
    plt.title("Distribution of Ingredients per Recipe")
    plt.savefig("ingredient_distribution.png")  # Save figure
    plt.show()

if __name__ == "__main__":
    print("Generating visualizations...")

    plot_top_ingredients()
    plot_recipe_distribution()
    plot_word_cloud()
    plot_ingredient_distribution()

    print("Visualizations saved as images in the project folder.")
