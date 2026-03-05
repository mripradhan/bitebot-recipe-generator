# BiteBot 🍳
**Your Personalized Recipe Generator**

BiteBot is a web application designed to help you cook delicious meals with the ingredients, equipment, and dietary restrictions you have. Powered by Groq's API and the latest Meta Llama 3.3 models, BiteBot creates step-by-step recipes customized to your needs — featuring a uniquely designed, clean, and vibrant egg-yolk orange UI.

## ✨ Features

- 📸 **Upload fridge images** to detect ingredients automatically (powered by Roboflow)
- 🥗 **Generate unique recipe variations** based on your available ingredients
- ⏱️ **Customize by cooking time** (quick, moderate, or leisurely meals)
- 🌎 **Select cuisine style** (Italian, Mexican, Chinese, etc.)
- 🥦 **Nutritional analysis** displayed for main ingredients (via API Ninjas)
- 🛠️ **Advanced customization** for dietary preferences and cooking tools
- 🎨 **Egg-Yolk Orange UI** — A striking, clean, and interactive frontend design utilizing glassmorphism, micro-animations, and minimal ASCII iconography.

## 🛠️ Technologies Used

- **Backend**: Python with **Flask** serving static files and API endpoints
- **Frontend**: Custom Vanilla **HTML, CSS, and JavaScript**
- **AI Core**: **Groq API** (using LLaMA 3.3 70B Versatile) for rapid recipe generation
- **Nutrition**: **API Ninjas** for nutritional data retrieval
- **Vision**: **Roboflow** Inference SDK for ingredient detection from images (Optional)
- **Environment**: **python-dotenv** for API key management

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Groq API key (free tier available)
- API Ninjas key (optional, for nutrition data)
- Roboflow API key (optional, for image detection. Minimum Python < 3.14 required)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/bitebot.git
   cd bitebot
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file and add your API keys:

   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ROBOFLOW_API_KEY=your_roboflow_key_here  # Optional
   NUTRITION_API_KEY=your_ninjas_api_key_here  # Optional
   ```

### Running the App

1. Start the Flask server:
   ```bash
   python app.py
   ```

2. The app will launch locally on port 5000. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## 🌟 Tips for Best Results

1. **Snap & Detect:** Drop an image of your ingredients into the upload zone to auto-detect them.
2. **Review:** Check and edit the detected list before pressing generate to ensure accuracy.
3. **Be specific with equipment** – Mention tools like air fryers, food processors, or Dutch ovens.
4. **Try different cuisines** to explore new flavors using the same base ingredients.

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements.

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

built with 🍊 by **bitebot**
