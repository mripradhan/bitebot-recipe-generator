import os
import tempfile
from flask import Flask, request, jsonify, send_from_directory
from groq import Groq
from dotenv import load_dotenv
import requests as http_requests

from PIL import Image
import base64
import requests as http_requests

load_dotenv()

app = Flask(__name__, static_folder="static", static_url_path="")

# ── API Clients ──────────────────────────────────────────────────────────────

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
NUTRITION_API_KEY = os.getenv("NUTRITION_API_KEY", "")
ROBOFLOW_API_KEY = os.getenv("ROBOFLOW_API_KEY", "")

# ── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/api/generate", methods=["POST"])
def generate_recipe():
    data = request.get_json(force=True)
    ingredients = data.get("ingredients", "")
    equipment = data.get("equipment", "")
    dietary = data.get("dietary_restrictions", "")
    cuisine = data.get("cuisine", "Any")
    time_limit = data.get("time_limit", "Any")

    user_prompt = (
        f"Ingredients: {ingredients}\n"
        f"Equipment: {equipment}\n"
        f"Dietary Restrictions: {dietary}\n"
    )
    if cuisine and cuisine != "Any":
        user_prompt += f"Cuisine Preference: {cuisine}\n"
    if time_limit and time_limit != "Any":
        user_prompt += f"Time Constraint: {time_limit}\n"

    try:
        completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional chef specializing in personalized recipe generation. "
                        "Create a recipe considering the provided ingredients, available kitchen equipment, "
                        "dietary restrictions, optional cuisine preference, and optional time constraint. "
                        "Include a title, short description, ingredients with measurements, "
                        "step-by-step instructions, and estimated cooking time. "
                        "Format your response in clean Markdown."
                    ),
                },
                {"role": "user", "content": user_prompt},
            ],
            model="llama-3.3-70b-versatile",
            max_tokens=700,
            temperature=0.7,
        )
        recipe = completion.choices[0].message.content
        return jsonify({"recipe": recipe})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.route("/api/nutrition", methods=["POST"])
def get_nutrition():
    if not NUTRITION_API_KEY:
        return jsonify({"error": "Nutrition API key not configured"}), 500

    data = request.get_json(force=True)
    ingredients = data.get("ingredients", "")

    results = []
    for ingredient in ingredients.split(",")[:5]:
        ingredient = ingredient.strip()
        if not ingredient:
            continue
        try:
            resp = http_requests.get(
                "https://api.api-ninjas.com/v1/nutrition",
                headers={"X-Api-Key": NUTRITION_API_KEY},
                params={"query": ingredient},
            )
            if resp.status_code == 200:
                results.extend(resp.json())
        except Exception:
            pass

    return jsonify({"nutrition": results})


@app.route("/api/detect", methods=["POST"])
def detect_ingredients():
    if not ROBOFLOW_API_KEY:
        return jsonify({"error": "Roboflow API key not configured"}), 500

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image_file = request.files["image"]

    try:
        # Save temp file, we could also just convert to base64 directly
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            image = Image.open(image_file).convert("RGB")
            image.save(tmp.name)
            
            with open(tmp.name, "rb") as bf:
                encoded_image = base64.b64encode(bf.read()).decode("ascii")

        # Call Roboflow HTTP API
        # Model: ingredient-detection-5uzov/5
        upload_url = "".join([
            "https://detect.roboflow.com/ingredient-detection-5uzov/5",
            f"?api_key={ROBOFLOW_API_KEY}",
            "&name=image.jpg"
        ])
        
        response = http_requests.post(
            upload_url,
            data=encoded_image,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if response.status_code != 200:
            return jsonify({"error": f"Roboflow API error: {response.text}"}), 500
            
        result = response.json()
        predictions = result.get("predictions", [])
        ingredients = list({pred["class"] for pred in predictions})
        
        # Clean up temp file
        os.remove(tmp.name)
        
        return jsonify({"ingredients": ingredients})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
