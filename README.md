# PromptCraft AI — Universal AI Prompt Studio

> **"One Idea. Any Prompt."**  
> *Turn your imagination into powerful, structured prompts for images, videos, websites, code and more.*

A lightweight, futuristic full-stack web application designed for the college course **IPE (Introduction to Prompt Engineering)**. PromptCraft AI helps students, developers, and creators convert raw, unstructured concepts into precision-engineered prompts optimized for modern AI models like ChatGPT, Midjourney, Claude, Cursor, v0, and Sora.

---

## 💡 Important Notice: How PromptCraft AI Works

PromptCraft AI is a **universal prompt generator and quality evaluator**. It uses Python templates and prompt engineering heuristics to craft well-structured prompt instructions.

- **What it does:** Generates high-clarity, context-rich, formatted prompt specifications ready to copy and paste into third-party AI tools.
- **What it does NOT do:** It does *not* directly generate final graphic images, render video files, or compile full standalone web servers.
- **Zero Cost / Zero Keys:** Requires **no paid APIs, no OpenAI/Anthropic API keys, and no database**.

---

## ✨ Key Features

1. **Universal Prompt Generation Across 7 Categories:**
   - 🖼️ **Image Generation:** Midjourney v6 / DALL-E 3 / SDXL parameter syntax, camera lens framing, lighting setups, color palettes, and negative prompts.
   - 🎬 **Video Generation:** Sora / Runway Gen-3 Alpha temporal pacing, camera movements, atmospheric lighting, and audio Foley cues.
   - 🌐 **Website Creation:** Claude 3.5 / v0.dev / Cursor page architecture, design system tokens, responsive grid requirements, and WCAG accessibility standards.
   - 💻 **Coding & Software:** Architecture planning, clean code guidelines, edge case handling, and unit test suites.
   - 📚 **Study & Learning:** Feynman technique, intuitive mental models, first principles, common pitfalls, and active recall quizzes.
   - ✍️ **Writing & Presentation:** High-impact narrative hooks, slide-by-slide deck breakdowns, tone directives, and calls-to-action.
   - ⚙️ **Custom Meta-Prompt:** Universal Role-Task-Context-Constraints meta-framework for custom tasks.

2. **6 Output Styles:**
   - 🔮 **Futuristic:** Sleek cyberpunk/solarpunk aesthetics, neon violet/cyan accents, and visionary forward-looking tone.
   - 🎬 **Cinematic:** Dramatic 35mm anamorphic film quality, volumetric lighting, and deep storytelling depth.
   - 🍃 **Minimal:** Clean negative space, Swiss international typography, and zero-fluff conciseness.
   - 💼 **Professional:** Enterprise rigor, balanced authoritative tone, and trustworthy structure.
   - ⚡ **Technical:** Blueprint precision, formal contracts, and deterministic edge-case coverage.
   - 🎨 **Creative:** Expressive avant-garde flair, unexpected metaphors, and vivid sensory language.

3. **Prompt Quality Check (0 – 100):**
   - Heuristic evaluation based on the **4 Pillars of Prompt Engineering**:
     - **Clarity (25 pts):** Direct intent and action verbs.
     - **Context (25 pts):** Persona, background setting, and target audience framing.
     - **Specificity (25 pts):** Concrete constraints, technical terms, and aesthetic descriptors.
     - **Output Format (25 pts):** Markdown structure, bullet points, parameters, and tables.
   - Provides up to 3 actionable suggestions to improve your prompt.
   - Includes a clear transparency disclaimer (heuristic educational estimate, not an AI guarantee).

4. **6 Instant Clickable Examples:**
   - Cinematic futuristic city image
   - Coffee shop promo video
   - Futuristic portfolio website
   - Python loops explained for beginners
   - Study notes summarized into revision points
   - College presentation on artificial intelligence

5. **Premium Futuristic UI/UX:**
   - Deep midnight background (`#070814`) with dark charcoal surfaces.
   - Glowing violet (`#8b5cf6`) and electric cyan (`#06b6d4`) accents.
   - Glassmorphic panels with `backdrop-filter: blur(24px)`.
   - 1-click clipboard copy with visual confirmation and animated toasts.
   - Real-time character counters and responsive mobile navigation.

---

## 📁 Project Structure

```
new ipe website/
│
├── app.py                  # Python Flask backend (routes, prompt generators, quality evaluator)
├── requirements.txt        # Python package dependencies (Flask, gunicorn)
├── .gitignore              # Git ignore rules for Python environments
├── README.md               # Complete documentation, setup, deployment & presentation guide
│
├── templates/
│   └── index.html          # Semantic HTML5 single-page application
│
└── static/
    ├── style.css           # Premium futuristic dark theme, neon glows, glassmorphism & responsive CSS
    └── script.js           # Vanilla JS (DOM handling, AJAX fetch, clipboard copy, examples)
```

---

## 🚀 How to Run Locally (Windows PowerShell)

Follow these exact steps in your Windows terminal:

### Step 1: Open PowerShell and navigate to the project directory
```powershell
cd "c:\Users\SUJAL\OneDrive\Desktop\new ipe website"
```

### Step 2: (Optional but Recommended) Create a virtual environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
*(If PowerShell throws an execution policy warning for activating the virtual environment, run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*

### Step 3: Install required dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Run the Flask application
```powershell
python app.py
```
*(Note: If `python` points to Microsoft Store alias on your system, run `python3.14 app.py` or `py app.py`)*

### Step 5: Open in Google Chrome
Open your web browser and go to:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🌐 Free Cloud Deployment Guide

### Why GitHub Pages Alone Cannot Run This Application:
> **Important Note for College Students:**  
> GitHub Pages is a static file hosting service. It only serves static HTML, CSS, and client-side JavaScript. It **cannot run a Python Flask backend** or execute Python code on a server. To run PromptCraft AI online for free, use a Python-compatible cloud host such as **Render** or **PythonAnywhere**.

---

### Option A: Free Deployment on Render (Recommended)

Render offers a free tier for Python web services:

1. **Push your code to a GitHub repository:**
   ```powershell
   git init
   git add .
   git commit -m "Initial commit of PromptCraft AI"
   git branch -M main
   git remote add origin https://github.com/<your-username>/promptcraft-ai.git
   git push -u origin main
   ```
2. Go to **[https://render.com](https://render.com)** and sign in with GitHub.
3. Click **New +** → **Web Service**.
4. Select your `promptcraft-ai` repository.
5. Configure the settings:
   - **Name:** `promptcraft-ai`
   - **Region:** Any close region (e.g., Singapore, Frankfurt, Oregon)
   - **Branch:** `main`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Instance Type:** `Free`
6. Click **Deploy Web Service**. Within 2-3 minutes, Render will provide a live public HTTPS URL (e.g., `https://promptcraft-ai.onrender.com`).

---

### Option B: Free Deployment on PythonAnywhere

1. Sign up for a free beginner account at **[https://www.pythonanywhere.com](https://www.pythonanywhere.com)**.
2. Go to the **Files** tab and upload `app.py`, `requirements.txt`, the `templates/` folder, and the `static/` folder (or clone from GitHub using a Bash console).
3. Go to the **Web** tab, click **Add a new web app**, choose **Flask**, and select **Python 3.10+**.
4. Point the source directory to your project folder and reload the web app.

---

## 🎓 IPE College Assignment Presentation Pitch

When presenting PromptCraft AI to your college professor or classmates, use this concise 60-second explanation:

> *"Respected Professor and peers, our project is **PromptCraft AI — Your Universal AI Prompt Studio**, created for our **Introduction to Prompt Engineering (IPE)** subject.*
>
> *Today, billions of people use generative AI tools like ChatGPT, Midjourney, and Claude, but most users receive mediocre or distorted results because their initial prompts lack structure, context, and clear constraints.*
>
> *PromptCraft AI bridges this gap. It takes a student or developer's simple one-line idea and instantly transforms it across 7 distinct categories — images, videos, websites, code, study notes, slide presentations, or custom tasks — into an engineered prompt using the **4 Pillars of Prompt Engineering: Clarity, Context, Constraints, and Output Format**.*
>
> *Additionally, we built a transparent **Quality Rubric Engine** in Python that scores prompt effectiveness out of 100 and provides actionable tips for improvement. The entire application runs on lightweight Python Flask, requires zero expensive API keys, and features an accessible, futuristic glassmorphic UI.*
>
> *Thank you, and we'd be thrilled to demonstrate a live prompt generation!"*

---

## 📜 License

Created for academic purposes under the **Introduction to Prompt Engineering (IPE)** curriculum. Open source and free to extend.
