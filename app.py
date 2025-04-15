# craft_app.py (Craft Idea Generator)
import streamlit as st
import requests
import random
import textwrap

# Hugging Face API Details
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-3B-Instruct"
HEADERS = {"Authorization": "Bearer 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"} # Replace with your actual API key

def query_llama(prompt):
  """Send a prompt to Hugging Face API and return the response."""
  try:
    response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})
    response.raise_for_status()
    return response.json()[0]['generated_text']
  except requests.exceptions.RequestException as e:
    return f"Error: {e}"

def generate_random_theme():
  themes = ["nature", "holidays", "space", "animals", "fantasy", "abstract", "food", "travel", "technology", "seasons", "underwater", "mythical creatures", "steampunk", "retro", "geometric"]
  return random.choice(themes)

def generate_random_material():
  materials = ["paper", "glue", "fabric", "wood", "clay", "yarn", "beads", "plastic", "metal", "leaves", "shells", "buttons", "wire", "felt", "cardboard"]
  return random.choice(materials)

def generate_random_difficulty():
  difficulties = ["Easy", "Medium", "Hard"]
  return random.choice(difficulties)

# Streamlit UI
st.title("💡 Craft Idea Generator 🎨")
st.write("Unleash your creativity with unique craft ideas!")

use_random = st.checkbox("Use Random Values?")

if use_random:
  materials = st.text_input("Materials:", value=generate_random_material())
  theme = st.text_input("Theme:", value=generate_random_theme())
else:
  materials = st.text_input("Materials:")
  theme = st.text_input("Theme:")

# Difficulty level as radio buttons for better UI
difficulty = st.radio("Difficulty Level:", ["Easy", "Medium", "Hard"], horizontal=True)

if st.button("Generate Craft Idea"):
  if materials and theme:
    prompt = f"Create a {difficulty.lower()} craft idea using {materials}. The theme is {theme}. Provide detailed steps, variations, and estimated time."
    with st.spinner("Generating..."):
      craft_idea = query_llama(prompt)

    st.success("Craft Idea:")
    st.write(craft_idea)

    # Additional Features
    st.subheader("Related Ideas:")
    related_prompt = f"Suggest 3 related craft ideas to '{craft_idea}'"
    related_ideas = query_llama(related_prompt)
    st.write(related_ideas)

    st.subheader("Material Alternatives:")
    alternatives_prompt = f"What are some alternative materials for '{materials}' in this craft?"
    material_alternatives = query_llama(alternatives_prompt)
    st.write(material_alternatives)

    st.subheader("Theme Variations:")
    theme_variations_prompt = f"Suggest some variations on the '{theme}' theme for this craft."
    theme_variations = query_llama(theme_variations_prompt)
    st.write(theme_variations)

  else:
    st.warning("Please enter materials and theme!")

# Custom CSS
st.markdown(
  """
    <style>
    body {
      background-color: #f0f8ff; /* Light blue background */
    }
    .stTextInput > div > div > input, .stTextArea > div > textarea {
      border: 2px solid #6495ED; /* Cornflower blue border */
      border-radius: 5px;
      padding: 10px;
      width: 100%;
      box-shadow: 2px 2px 5px #888888;
    }
    .stButton > button {
      background-color: #6495ED;
      color: white;
      padding: 15px 32px;
      text-align: center;
      text-decoration: none;
      display: inline-block;
      font-size: 16px;
      border-radius: 8px;
      width: 100%;
      box-shadow: 2px 2px 5px #888888;
    }
    .stRadio > label, .stSelectbox > label {
      font-size: 18px;
      color: #333;
    }
    .stSpinner > div > div {
      border-color: #6495ED;
    }
    .stSuccess, st.warning {
      padding: 20px;
      border-radius: 10px;
    }

    /* Remove the blue highlight on selected radio buttons */
    .stRadio > label > div > div:has(input:checked) {
      background-color: transparent; /* Remove background color */
    }
    /* Style radio buttons */
    .stRadio > label > div > div {
        border: 1px solid #ccc; /* Add a light border */
        border-radius: 5px; /* Add rounded corners */
        padding: 8px 12px; /* Add padding for better appearance */
        margin-right: 10px; /* Add spacing between buttons */
        display: inline-flex;
        align-items: center;
    }

    .stRadio > label > div > div:has(input:checked){
        border: 2px solid #6495ED;
    }

    </style>
  """,
  unsafe_allow_html=True,
)
