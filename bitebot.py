import streamlit as st
from groq import Groq
import os
import requests
from dotenv import load_dotenv
import pyperclip

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
NINJAS_API_KEY = os.getenv("NINJAS_API_KEY")

# Custom CSS for a cute pastel theme
st.markdown(
    """
    <style>
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
        color:rgb(255, 152, 167);
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
        color: #000000 !important; /* Make ALL labels black */
    }
    .recipe-column {
        padding: 15px;
        border-radius: 10px;
        background-color: #fff5f7;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

class RecipeGenerator:
    def __init__(self, api_key=None):
        """
        Initialize Groq client with API key handling.
        """
        if api_key:
            self.client = Groq(api_key=api_key)
        else:
            env_key = os.getenv('GROQ_API_KEY')
            if not env_key and hasattr(st.secrets, 'GROQ_API_KEY'):
                env_key = st.secrets.GROQ_API_KEY
            if not env_key:
                st.warning("🔐 Groq API Key not found. Please enter your API key below.")
                env_key = st.text_input("Enter your Groq API Key", type="password", help="You can find this in your Groq account.")
            if env_key:
                self.client = Groq(api_key=env_key)
            else:
                st.error("❌ API key required. Cannot initialize Groq client.")
                self.client = None

    def generate_recipe(self, ingredients, equipment, dietary_restrictions, cooking_time, difficulty, cuisine):
        """
        Generate a recipe using Groq API.
        """
        if not self.client:
            st.error("⚠️ Groq client not initialized.")
            return None

        try:
            with st.spinner(f"🍳 Cooking up your {cuisine} recipe ({difficulty} difficulty, {cooking_time} mins)..."):
                chat_completion = self.client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": f"""You are a professional chef specializing in {cuisine} cuisine. 
                            Create a recipe with these requirements:
                            - Cooking time: {cooking_time} minutes
                            - Difficulty level: {difficulty}
                            - Dietary restrictions: {dietary_restrictions}
                            The recipe should include:
                            1. A creative title
                            2. Preparation time and servings
                            3. Detailed ingredient list with measurements
                            4. Clear step-by-step instructions
                            5. Serving suggestions"""
                        },
                        {
                            "role": "user",
                            "content": f"Ingredients: {ingredients}\nEquipment: {equipment}\nDietary Restrictions: {dietary_restrictions}"
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
        if not api_key:
            st.warning("⚠️ API Ninjas API Key required for nutrition analysis.")
        self.api_key = api_key

    def get_nutrition(self, ingredients):
        if not self.api_key:
            return None
        nutrition_data = []
        for ingredient in ingredients.split(",")[:5]:  # Limit to first 5 ingredients
            try:
                response = requests.get(
                    "https://api.api-ninjas.com/v1/nutrition",
                    headers={"X-Api-Key": self.api_key},
                    params={"query": ingredient.strip()}
                )
                if response.status_code == 200:
                    nutrition_data.extend(response.json())
                else:
                    st.warning(f"⚠️ Unable to fetch nutrition for {ingredient}")
            except Exception as e:
                st.error(f"❌ API Request Failed: {e}")
        return nutrition_data

def main():
    # Main UI
    st.markdown("<h1 class='main-title'>🥗 Welcome to BiteBot! Your personalized recipe generator.</h1>", unsafe_allow_html=True)
    st.write("✨ All you have to do is enter your available ingredients, equipment, and preferences. We'll create delicious recipes tailored just for you!")

    # Sidebar Configuration
    with st.sidebar:
        st.markdown("<h2 class='sidebar-title'>⚙️ Configuration</h2>", unsafe_allow_html=True)
        api_key = st.text_input("🔐 Groq API Key (optional)", type="password", value=GROQ_API_KEY or "")
        st.markdown("---")
        st.info("**Steps to Use:**\n\n1️⃣ Enter ingredients, equipment, and preferences\n\n2️⃣ Click **Generate Recipe**\n\n3️⃣ Enjoy your new recipes! 😋")
    
    # Create instances
    recipe_generator = RecipeGenerator(api_key=api_key)
    nutrition_analyzer = NutritionAnalyzer(api_key=NINJAS_API_KEY)

    # Main Form Section
    st.markdown("<h2 class='subtitle'>🥞 Available Ingredients</h2>", unsafe_allow_html=True)
    ingredients = st.text_area("List your ingredients (comma-separated)", placeholder="E.g., egg, tomatoes, olive oil")

    st.markdown("<h2 class='subtitle'>🥘 Available Equipment</h2>", unsafe_allow_html=True)
    equipment = st.text_area("List your kitchen equipment (comma-separated)", placeholder="E.g., oven, frying pan, mixer")

    st.markdown("<h2 class='subtitle'>🍓 Dietary Preferences</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        dietary_restrictions = st.text_input("Dietary Restrictions", placeholder="E.g., vegetarian")
    with col2:
        cuisine = st.selectbox("Cuisine", ["Italian", "Indian", "Chinese", "Mexican", "French", "Japanese", "Mediterranean", "American"], index=0)
    with col3:
        cooking_time = st.selectbox("Time", ["10-20 mins", "20-40 mins", "40+ mins"], index=1)
    
    time_map = {"10-20 mins": 15, "20-40 mins": 30, "40+ mins": 60}
    difficulty_map = {"10-20 mins": "Easy", "20-40 mins": "Medium", "40+ mins": "Hard"}

    # Generate Button
    if st.button("✨ Generate Recipes", type="primary", help="Click to create your personalized recipes."):
        if not ingredients.strip():
            st.warning("⚠️ Please enter your ingredients.")
            return
        
        # Generate two recipe variations
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='recipe-column'>", unsafe_allow_html=True)
            recipe1 = recipe_generator.generate_recipe(
                ingredients, equipment, dietary_restrictions, 
                time_map[cooking_time], difficulty_map[cooking_time], cuisine
            )
            if recipe1:
                st.markdown(f"## 🍽️ Recipe 1")
                st.markdown(f"<div class='highlight-box'>{recipe1}</div>", unsafe_allow_html=True)
                if st.button("📋 Copy Recipe 1", key="copy1"):
                    pyperclip.copy(recipe1)
                    st.success("✅ Copied!")
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='recipe-column'>", unsafe_allow_html=True)
            recipe2 = recipe_generator.generate_recipe(
                ingredients, equipment, dietary_restrictions, 
                time_map[cooking_time], difficulty_map[cooking_time], cuisine
            )
            if recipe2:
                st.markdown(f"## 🍽️ Recipe 2")
                st.markdown(f"<div class='highlight-box'>{recipe2}</div>", unsafe_allow_html=True)
                if st.button("📋 Copy Recipe 2", key="copy2"):
                    pyperclip.copy(recipe2)
                    st.success("✅ Copied!")
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Nutrition Analysis
        if NINJAS_API_KEY:
            with st.expander("🥦 Nutritional Breakdown (for main ingredients)"):
                nutrition_data = nutrition_analyzer.get_nutrition(ingredients)
                if nutrition_data:
                    for item in nutrition_data:
                        st.write(f"""
                        **🍏 {item['name'].title()}**  
                        Calories: {item['calories']} kcal  
                        Protein: {item['protein_g']}g  
                        Fat: {item['fat_total_g']}g  
                        Carbs: {item['carbohydrates_total_g']}g  
                        Fiber: {item['fiber_g']}g
                        """)
                else:
                    st.warning("Could not fetch nutrition data for these ingredients")

if __name__ == "__main__":
    main()
