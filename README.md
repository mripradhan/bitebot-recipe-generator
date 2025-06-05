# BiteBot 🍳  
**Your Personalized Recipe Generator**  

BiteBot is a Streamlit-based application designed to help you cook delicious meals with the ingredients, equipment, and dietary restrictions you have. Powered by Groq's API, BiteBot creates step-by-step recipes customized to your needs — now with image-based ingredient detection and enhanced customization!  

## ✨ Features

- 📸 **Upload fridge images** to detect ingredients automatically (with option to edit afterward)
- 🥗 **Generate unique recipe variations** based on your available ingredients
- ⏱️ **Customize by cooking time** (quick, moderate, or leisurely meals)
- 🌎 **Select cuisine style** (Italian, Mexican, Chinese, etc.)
- 🥦 **Nutritional analysis** displayed for main ingredients and final dish (via API Ninjas)
- 🛠️ **Advanced customization** for dietary preferences and cooking tools
- 🎨 **Charming pastel UI** with responsive design

## 🛠️ Technologies Used

- **Python** with **Streamlit** for the web interface
- **Groq API** (using LLaMA 3 70B) for AI recipe generation
- **API Ninjas** for nutrition data
- **Roboflow** or **custom image model** for ingredient detection from uploaded fridge images
- **Dotenv** for environment variable management

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Groq API key (free tier available)
- API Ninjas key (optional, for nutrition data)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/bitebot.git
   cd bitebot
   ````

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file and add your API keys:

   ```env
   GROQ_API_KEY=your_groq_api_key_here
   NINJAS_API_KEY=your_ninjas_api_key_here  # Optional
   ```

### Running the App

```bash
streamlit run app.py
```

The app will launch in your default browser at `http://localhost:8501`.

## 🌟 Tips for Best Results

1. **Upload a clear image of your fridge contents** to auto-detect ingredients.
2. **Review and edit the detected list** before recipe generation.
3. **List as many ingredients as possible** for more accurate results.
4. **Be specific with equipment** – Mention tools like air fryers or blenders.
5. **Try different cuisines** to explore new flavors.
6. **Use the nutrition panel** for meal planning and dietary awareness.

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a pull request

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Enjoy BiteBot, and eat well! 🥗
