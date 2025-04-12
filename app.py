from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import openai

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from the environment variables
api_key = os.getenv("OPENAI_API_KEY")

# Check if API key is set, and raise an error if not
if not api_key:
    raise ValueError("❌ OPENAI_API_KEY is missing. Make sure it's in your .env file.")

# Set OpenAI API key
openai.api_key = api_key

app = Flask(__name__)

# Function to build the story prompt
def build_prompt(genre, character, setting, tone):
    return (
        f"Write a {tone} short story in the {genre} genre, set in a {setting}. "
        f"The main character is named {character}. "
        f"Start with a clear introduction. Midway through, introduce a surprising but logically coherent plot twist. "
        f"Ensure the twist fits the tone and genre. End the story with an emotionally satisfying resolution."
    )

# Function to generate story using OpenAI API
def generate_story(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # You can also use "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "You are a masterful storyteller who writes engaging and twist-filled stories."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,
            max_tokens=900
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error generating story: {e}"

# Home route to handle form submission and display the generated story
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        genre = request.form["genre"]
        character = request.form["character"]
        setting = request.form["setting"]
        tone = request.form["tone"]

        prompt = build_prompt(genre, character, setting, tone)
        story = generate_story(prompt)

        return render_template("index.html", story=story, genre=genre, character=character, setting=setting, tone=tone)

    return render_template("index.html", story=None)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)