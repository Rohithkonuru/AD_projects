from flask import Flask, render_template, request
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os
import re

app = Flask(__name__)

# Ensure the "static" directory exists
if not os.path.exists("static"):
    os.makedirs("static")

def extract_ingredients(text):
    """
    Extracts ingredients from text using regex.
    Returns a structured list of tuples (Ingredient, Quantity, Unit).
    """
    ingredient_list = []
    pattern = r"(\d*\s*\d*\/?\d*)\s*([a-zA-Z]+)?\s*(.+)"
    
    for line in text.split(","):
        line = line.strip()
        match = re.match(pattern, line)
        if match:
            quantity = match.group(1).strip() if match.group(1) else "N/A"
            unit = match.group(2).strip() if match.group(2) else "N/A"
            ingredient = match.group(3).strip()
            ingredient_list.append((ingredient, quantity, unit))
    
    return ingredient_list

def generate_visualizations(ingredients):
    """
    Generates a word cloud and a pie chart from the extracted ingredients.
    """
    ingredient_names = [ing[0] for ing in ingredients]
    ingredient_quantities = []

    # Convert valid numeric values; if not a number, default to 1
    for ing in ingredients:
        try:
            qty = float(ing[1])
        except ValueError:
            qty = 1
        ingredient_quantities.append(qty)

    # Generate Word Cloud
    wordcloud_text = " ".join(ingredient_names)
    wordcloud = WordCloud(width=500, height=300, background_color="white").generate(wordcloud_text)
    wordcloud.to_file("static/ingredient_wordcloud.png")

    # Generate Pie Chart
    plt.figure(figsize=(6, 6))
    plt.pie(ingredient_quantities, labels=ingredient_names, autopct='%1.1f%%', colors=plt.cm.Paired.colors)
    plt.title("Ingredient Distribution for Selected Recipe")
    plt.savefig("static/ingredient_pie_chart.png")
    plt.close()

@app.route("/", methods=["GET", "POST"])
def index():
    ingredients = []
    generated = False
    url = ""

    if request.method == "POST":
        url = request.form["recipe_url"]
        raw_ingredients = "2 salmon fillets, 1 tbsp olive oil, 1 tsp lemon zest, 1 tbsp lemon juice, 1 tsp black pepper, 1 tsp salt, 1 garlic clove minced"

        # Extract ingredients in structured format
        ingredients = extract_ingredients(raw_ingredients)

        # Generate visualizations
        generate_visualizations(ingredients)
        generated = True

    return render_template("index.html", url=url, ingredients=ingredients, generated=generated)

if __name__ == "__main__":
    app.run(debug=True)
