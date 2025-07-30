# MediaSanitizer — Armenian News Credibility Checker

MediaSanitizer is an AI-powered tool that checks the credibility of Armenian (and English) news articles. It helps journalists, fact-checkers, and ordinary readers detect bias, red flags, and estimate trustworthiness in media.


---

## 🚀 Features

- **Analyze News Credibility:** Paste a link or full article text to check for bias, red flags, and a credibility score.
    
- **AI-Based Analysis:** Uses advanced language models (OpenAI GPT-3.5-turbo or GPT-4) for deep natural language analysis.
    
- **Source Cross-Check:** Compares articles against trusted Armenian news outlets.
    
- **Heuristic Analysis:** Reports on emotional language, subjectivity, and writing style.
    
- **Clear Visual Report:** Green/Yellow/Red trust signal, red flags, summary, and more.

---

## 💡 How It Works

1. **Paste a news article link** or the full article text.
    
2. **The backend fetches and analyzes** the article using NLP and AI.
    
3. **A clear report is shown** with a trust indicator, explanations, and detected issues.
    

---

## 📦 Tech Stack

- **Frontend:** HTML, CSS, vanilla JS (no frameworks)
    
- **Backend:** Python (Flask)
    
- **AI API:** OpenAI GPT-3.5-turbo (or GPT-4, customizable)
    
- **Scraping:** Selenium for dynamic web scraping
    
- **Database:** SQLite (stores analysis results)
    

---

### 1. Clone the repository
```bash
git clone https://github.com/p055e55eD/mediasanitizer.git
cd mediasanitizer
```

### 2. Set up Python & install dependencies

> **Python 3.8+ recommended.**

If you use PyCharm, just open the project and set the interpreter.

Otherwise, in terminal:
```bash
python -m venv venv venv\Scripts\activate    # On Windows # Or: source venv/bin/activate   # On Mac/Linux  pip install -r requirements.txt
```

### 3. Download WebDriver for Selenium

- **Chrome:** Download ChromeDriver matching your Chrome version.
    
- **Edge:** Download msedgedriver.
    
- Place the driver `.exe` somewhere in your PATH, or specify its path in your `scraper.py`.
    

### 4. Set up API Keys

- **OpenAI API Key** required!
    
- Create a file called `.env` in the `backend/` directory:
    
    `OPENAI_API_KEY=sk-...`
    
    (Get your key from [https://platform.openai.com/](https://platform.openai.com/))
    

### 5. Run the Backend

`cd backend python app.py`

> By default, the backend runs at `http://localhost:5000`

### 6. Run the Frontend

No build tools needed! Just open `frontend/index.html` in your browser.

- For best results, use **Chrome** or **Edge** (Selenium/driver must match browser).
    
- If CORS issues, try running a simple static server:
    
    `cd frontend python -m http.server 8080 # Then open http://localhost:8080 in browser`
    

---

## 📝 Usage Notes

- **Supports both Armenian and English articles.**
    
- **Text or URL:** You can paste an article’s URL or full text.
    
- **Results are cached in SQLite** — repeated analysis is instant.
    

---

## ⚡️ Troubleshooting

- **Selenium errors:** Ensure your browser and WebDriver versions match.
    
- **OpenAI quota errors:** Check your billing at [https://platform.openai.com/account/usage](https://platform.openai.com/account/usage).
    
- **CORS errors:** If frontend and backend run on different ports, use Flask-CORS (already included).
