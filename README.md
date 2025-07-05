
# 🥗 Smart Recipe Recommender

**Smart Recipe Recommender** is a personalized cooking assistant that suggests recipes based on your **mood**, **health goals**, and **available ingredients**. Whether you're feeling festive, tired, or looking for a high-protein meal, this smart app finds just the right dish for you!

---

## 🌟 Key Features

- 🎭 **Mood-Based Suggestions** — Choose a mood like *Happy*, *Tired*, or *Festive* to get emotionally relevant dishes.
- 🥦 **Health Goals Support** — Filter recipes based on goals like *Weight Loss*, *Quick Meal*, *Vegan*, and more.
- 🍅 **Ingredient Matching** — Enter available ingredients and get recipes that closely match what you have.
- 🌓 **Dark & Light Mode** — Beautiful mood-responsive themes with toggle support.
- 🎬 **Intro Animation** — Eye-catching animated welcome screen with a clean "Get Started" flow.
- 📄 **Export Recipes** — Download recipe recommendations in **PDF** or **CSV** format.
- ⚡ **Fast & Minimal UI** — Smooth transitions, collapsible sections, modern fonts, and responsive design.
- 🧠 **Lightweight ML** — Uses TF-IDF vectorization and cosine similarity for intelligent matching.

---

## 🛠️ Built With

- **Python (Flask)** — Backend web framework
- **HTML + CSS + JS** — Responsive and animated frontend
- **Pandas** — Data handling
- **Scikit-learn** — Ingredient similarity (TF-IDF + Cosine)
- **ReportLab** — PDF generation
- **Jinja2** — Templating for dynamic content

---

## 🚀 Getting Started

1. **Clone the Repository**
   ```bash
   git clone https://github.com/NavyaSri-0701/SmartRecipeRecommender.git
   cd SmartRecipeRecommender
````

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the App**

   ```bash
   python app.py
   ```

4. Open your browser and go to:
   `http://localhost:5000`

---

## 🌐 Deployment

The app is ready to be deployed on platforms like:

* [Render](https://render.com/)
* [Replit](https://replit.com/)
* [Heroku](https://www.heroku.com/)
* [Vercel (via Flask adapters)](https://vercel.com/)

> Be sure to include your dataset file (`enriched_13k_recipes.csv`) and all templates/static files in your deployment.

---

## 📁 Project Structure

```
SmartRecipeRecommender/
├── templates/
│   ├── intro.html         # Animated welcome screen
│   └── index.html         # Main recipe search page
├── static/
│   └── salad.png          # (Optional) Browser tab logo
├── enriched_13k_recipes.csv
├── app.py                 # Flask application
├── requirements.txt
└── README.md
```

---

## 📘 Dataset
This project uses the 13k-recipes.csv dataset published by @josephrmartinez, containing over 13,000 diverse recipes.

✨ Enhancements Added:

Cleaned and tokenized ingredients

Annotated recipes with Mood Tags: Tired, Happy, Comforting, Festive, Adventurous

Tagged recipes with Health Goals: Weight Loss, High Protein, Balanced Diet, Quick Meal, Vegan

This enriched dataset powers the intelligent filtering and recommendation features in the app.


## 📄 License

This project is licensed under the **MIT License**.
Feel free to use, share, and improve it!



