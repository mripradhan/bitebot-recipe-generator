# BiteBot 🍳  
**Your Personalized Recipe Generator**  

BiteBot is a Streamlit-based application designed to help you cook delicious meals with the ingredients, equipment, and dietary restrictions you have. Powered by Groq's API, BiteBot creates step-by-step recipes customized to your needs in just a few clicks!  

## ✨ Features

- 🥗 **Generate two unique recipe variations** from your ingredients
- ⏱️ **Customize by cooking time** (quick, moderate, or leisurely meals)
- 🌎 **Select cuisine style** (Italian, Mexican, Japanese, etc.)
- 🥦 **Nutritional analysis** of main ingredients (via API Ninjas)
- 🎨 **Charming pastel UI** with responsive design

## 🛠️ Technologies Used

- **Python** with **Streamlit** for the web interface
- **Groq API** (using LLaMA 3 70B) for AI recipe generation
- **API Ninjas** for nutrition data
- **Dotenv** for environment variable management
- **Pyperclip** for copy-to-clipboard functionality

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
   ```

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

1. **List as many ingredients as possible** - More ingredients = more creative recipes!
2. **Be specific with equipment** - Mention if you have special tools like air fryers or blenders
3. **Try different cuisines** - Discover new flavor combinations
4. **Use the nutrition analysis** - Great for meal planning and dietary tracking

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a pull request
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Enjoy BiteBot, and happy cooking! 🥗
