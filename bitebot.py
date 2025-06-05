import streamlit as st
from groq import Groq
from inference_sdk import InferenceHTTPClient
from PIL import Image
import tempfile
import requests

# Custom CSS
st.markdown(
    """
    <style>
    .highlight-box ul {
        margin-top: 0;
        margin-bottom: 0;
        padding-left: 20px;
    }
    .highlight-box li {
        margin-top: 2px;
        margin-bottom: 2px;
        line-height: 1.4;
    }
    .stApp {
        background-color: #fdf7f9;
        color: #4d4d4d;
    }
    .main-title {
        font-family: "Comic Sans MS", cursive, sans-serif;
        color: #ff6b81;
    }
    .subtitle {
        font-family: "Calibri", cursive, sans-serif;
        color: rgb(255, 152, 167);
    }
    .sidebar-title {
        color: #f0932b;
        font-weight: bold;
    }
    .highlight-box {
        background-color: #ffe5ef;
        padding: 10px;
        border-radius: 10px;
        border: 1px solid #f39c12;
    }
    label {
        color: #000000 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

class RecipeGenerator:
    def __init__(self, api_key=None):
        if api_key:
            self.client = Groq(api_key=api_key)
        else:
            env_key = "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"
            self.client = Groq(api_key=env_key)

    def generate_recipe(self, ingredients, equipment, dietary_restrictions, cuisine=None, time_limit=None):
        if not self.client:
            st.error("⚠️ Groq client not initialized.")
            return None

        try:
            with st.spinner("🍳 Cooking up your personalized recipe..."):
                user_prompt = (
                    f"Ingredients: {ingredients}\n"
                    f"Equipment: {equipment}\n"
                    f"Dietary Restrictions: {dietary_restrictions}\n"
                )
                if cuisine and cuisine != "Any":
                    user_prompt += f"Cuisine Preference: {cuisine}\n"
                if time_limit and time_limit != "Any":
                    user_prompt += f"Time Constraint: {time_limit}\n"

                chat_completion = self.client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": """You are a professional chef specializing in personalized recipe generation.
                            Create a recipe considering:
                            - Provided ingredients
                            - Available kitchen equipment
                            - Dietary restrictions
                            - Optional cuisine preference
                            - Optional time constraint
                            Include a title, short description, ingredients with measurements, step-by-step instructions, and estimated cooking time."""
                        },
                        {
                            "role": "user",
                            "content": user_prompt
                        }
                    ],
                    model="llama3-70b-8192",
                    max_tokens=700,
                    temperature=0.7
                )
            return chat_completion.choices[0].message.content
        except Exception as e:
            st.error(f"❌ Error: {e}")
            return None

class NutritionAnalyzer:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_nutrition(self, ingredients):
        if not self.api_key:
            st.warning("⚠️ API Ninjas API Key required for nutrition analysis.")
            return []

        nutrition_data = []
        for ingredient in ingredients.split(",")[:5]:
            try:
                response = requests.get(
                    "https://api.api-ninjas.com/v1/nutrition",
                    headers={"X-Api-Key": self.api_key},
                    params={"query": ingredient.strip()}
                )
                if response.status_code == 200:
                    nutrition_data.extend(response.json())
                else:
                    st.warning(f"⚠️ Could not fetch nutrition for {ingredient.strip()}")
            except Exception as e:
                st.error(f"❌ Error fetching nutrition: {e}")
        return nutrition_data

def detect_ingredients_with_roboflow(image_file):
    roboflow_api_key = "VBrbofv1SzJmOhfTp1ZS"

    try:
        client = InferenceHTTPClient(
            api_url="https://detect.roboflow.com",
            api_key=roboflow_api_key
        )

        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
            image = Image.open(image_file).convert("RGB")
            image.save(tmp_file.name)

            result = client.infer(
                tmp_file.name,
                model_id="ingredient-detection-5uzov/5"
            )

        predictions = result.get("predictions", [])
        ingredients = list({pred["class"] for pred in predictions})
        return ingredients

    except Exception as e:
        st.error(f"🛑 Roboflow error: {e}")
        return []

def main():
    st.markdown("<h1 class='main-title'>🥗 Welcome to BiteBot! Your personalized recipe generator.</h1>", unsafe_allow_html=True)
    st.write("✨ Enter your ingredients, equipment, and preferences, and BiteBot will cook up the perfect recipe!")

    nutrition_api_key = "a6viV8ixM0pzeCrx47jWrw==pBdll5JaBghNMV0r"
    nutrition_analyzer = NutritionAnalyzer(api_key=nutrition_api_key)
    recipe_generator = RecipeGenerator(api_key=None)

    with st.sidebar:
        st.markdown("<h2 class='sidebar-title'>⚙️ Configuration</h2>", unsafe_allow_html=True)
        st.markdown("---")
        st.info("**Steps to Use:**\n\n1️⃣ Upload or list ingredients.\n\n2️⃣ Fill out other preferences.\n\n3️⃣ Click **Generate Recipe**!\n\n🍽️ Bon Appétit!")

    st.markdown("<h2 class='subtitle'>📷 Upload an Image of Ingredients</h2>", unsafe_allow_html=True)
    uploaded_image = st.file_uploader("Upload a kitchen image (jpg/png)", type=["jpg", "jpeg", "png"])
    autofill_ingredients = ""

    if uploaded_image:
        st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
        with st.spinner("🧠 Detecting ingredients using Roboflow..."):
            detected_ingredients = detect_ingredients_with_roboflow(uploaded_image)
        if detected_ingredients:
            autofill_ingredients = ", ".join(detected_ingredients)
            st.markdown(
                f"""
                <div style="background-color: #d4edda; padding: 10px; border-radius: 8px;
                            border-left: 6px solid #28a745; color: #155724; font-weight: 500;">
                    ✅ <strong>Detected:</strong> {autofill_ingredients}
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("<h2 class='subtitle'>🥞 Available Ingredients</h2>", unsafe_allow_html=True)
    ingredients = st.text_area("List your ingredients (comma-separated)", value=autofill_ingredients)

    st.markdown("<h2 class='subtitle'>🥘 Available Equipment</h2>", unsafe_allow_html=True)
    equipment = st.text_area("List your kitchen equipment (comma-separated)", placeholder="E.g., oven, blender, stove")

    st.markdown("<h2 class='subtitle'>🍓 Dietary Restrictions</h2>", unsafe_allow_html=True)
    dietary_restrictions = st.text_input("Enter any dietary restrictions", placeholder="E.g., vegan, nut-free")

    st.markdown("<h2 class='subtitle'>🌍 Preferred Cuisine</h2>", unsafe_allow_html=True)
    cuisine_type = st.selectbox(
        "Choose a cuisine",
        ["Any", "Italian", "Indian", "Mexican", "Chinese", "Japanese", "French", "Mediterranean", "Thai", "American"]
    )

    st.markdown("<h2 class='subtitle'>⏱️ Time Constraint</h2>", unsafe_allow_html=True)
    time_constraint = st.selectbox(
        "Select maximum cooking time",
        ["Any", "15 minutes", "30 minutes", "45 minutes", "1 hour", "Over 1 hour"]
    )

    col1, col2 = st.columns([2, 1])
    with col1:
        generate_button = st.button("✨ Generate Recipe")
    with col2:
        st.write("")
        st.write("✩₊˚.⋆☾⋆⁺₊✧")

    if generate_button:
        if not ingredients.strip():
            st.warning("⚠️ Please enter your ingredients.")
            return
        if not equipment.strip():
            st.warning("⚠️ Please enter your equipment.")
            return

        recipe = recipe_generator.generate_recipe(
            ingredients, equipment, dietary_restrictions,
            cuisine=cuisine_type, time_limit=time_constraint
        )

        if recipe:
            st.markdown("<h2 class='subtitle'>📜 Your Recipe</h2>", unsafe_allow_html=True)
            st.markdown(f"<div class='highlight-box'>{recipe}</div>", unsafe_allow_html=True)

            st.markdown("<h2 class='subtitle'>🧪 Estimated Nutritional Information</h2>", unsafe_allow_html=True)
            with st.spinner("🥦 Analyzing nutritional content..."):
                nutrition_data = nutrition_analyzer.get_nutrition(ingredients)

            if nutrition_data:
                for item in nutrition_data:
                    st.markdown(
                        f"""
                        <div class='recipe-column'>
                            <strong>{item.get('name', 'Ingredient')}</strong><br>
                            Calories: {item.get('calories', 'N/A')} kcal<br>
                            Protein: {item.get('protein_g', 'N/A')} g<br>
                            Fat: {item.get('fat_total_g', 'N/A')} g<br>
                            Carbs: {item.get('carbohydrates_total_g', 'N/A')} g<br>
                            Sugar: {item.get('sugar_g', 'N/A')} g
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.info("No nutritional data found.")

if __name__ == "__main__":
    main()
