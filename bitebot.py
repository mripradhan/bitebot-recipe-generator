import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv
import pyperclip

# Load environment variables from .env file
load_dotenv()

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
        border-radius: 10px;S
        border: 1px solid #f39c12;
    }
    label {
        color: #000000 !important; /* Make ALL labels black */
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

    def generate_recipe(self, ingredients, equipment, dietary_restrictions):
        """
        Generate a recipe using Groq API.
        """
        if not self.client:
            st.error("⚠️ Groq client not initialized.")
            return None

        try:
            with st.spinner("🍳 Cooking up your personalized recipe..."):
                chat_completion = self.client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": """You are a professional chef specializing in creating personalized recipes. 
                            Create a recipe based on the following:
                            1. Available ingredients
                            2. Available equipment
                            3. Dietary restrictions
                            The recipe should include a title, a short description, step-by-step instructions including ingredient measurements, and approximate cooking time."""
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

def main():
    # Main UI
    st.markdown("<h1 class='main-title'>🥗 Welcome to BiteBot! Your personalized recipe generator.</h1>", unsafe_allow_html=True)
    st.write("✨ All you have to do is enter your available ingedients, available equipment, and dietary restrictions. We'll tell you exactly what to cook and how to do it, so you can enjoy a meal made with love (and what you have on hand)!")

    # Sidebar Configuration
    with st.sidebar:
        st.markdown("<h2 class='sidebar-title'>⚙️ Configuration</h2>", unsafe_allow_html=True)
        api_key = st.text_input("🔐 Groq API Key (optional)", type="password")
        st.markdown("---")
        st.info("**Steps to Use:**\n\n1️⃣ Enter ingredients, equipment, and restrictions.\n\n2️⃣ Click **Generate Recipe**.\n\n3️⃣ Copy or enjoy your new recipe! 😋")
    
    # Create a RecipeGenerator instance
    recipe_generator = RecipeGenerator(api_key=api_key)

    # Main Form Section
    st.markdown("<h2 class='subtitle'>🥞 Available Ingredients</h2>", unsafe_allow_html=True)
    ingredients = st.text_area("List your ingredients (comma-separated)", placeholder="E.g., egg, tomatoes, olive oil")

    st.markdown("<h2 class='subtitle'>🥘 Available Equipment</h2>", unsafe_allow_html=True)
    equipment = st.text_area("List your kitchen equipment (comma-separated)", placeholder="E.g., oven, frying pan, mixer")

    st.markdown("<h2 class='subtitle'>🍓 Dietary Restrictions</h2>", unsafe_allow_html=True)
    dietary_restrictions = st.text_input("Enter any dietary restrictions", placeholder="E.g., vegetarian, gluten-free")

    # Generate Button
    col1, col2 = st.columns([2, 1])
    with col1:
        generate_button = st.button("✨ Generate Recipe", help="Click to create your personalized recipe.")
    with col2:
        st.write("")  # Spacer
        st.write("✩₊˚.⋆☾⋆⁺₊✧✩₊˚.⋆☾⋆⁺₊✧")

    # Generate and Display Recipe
    if generate_button:
        if not ingredients.strip():
            st.warning("⚠️ Please enter your ingredients.")
            return
        if not equipment.strip():
            st.warning("⚠️ Please enter your equipment.")
            return
        
        recipe = recipe_generator.generate_recipe(ingredients, equipment, dietary_restrictions)
        if recipe:
            st.markdown("## 📜 Your Recipe")
            st.markdown(f"<div class='highlight-box'>{recipe}</div>", unsafe_allow_html=True)
            # if st.button("📋 Copy to Clipboard"):
            #     pyperclip.copy(recipe)
            #     st.success("✅ Recipe copied to clipboard!")

if __name__ == "__main__":
    main()