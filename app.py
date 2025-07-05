from flask import Flask, render_template, request, send_file, redirect, url_for
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
import io

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# ---------- Load and process dataset ----------
df = pd.read_csv("enriched_13k_recipes.csv")
df['Ingredients_Text'] = df['Cleaned_Ingredients'].apply(eval).apply(lambda x: ' '.join(x))
df['Mood_Tags'] = df['Mood_Tags'].apply(eval)
df['Health_Goal_Tags'] = df['Health_Goal_Tags'].apply(eval)
df['Ingredients'] = df['Ingredients'].apply(eval)

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df['Ingredients_Text'])

# ---------- Recommendation Function ----------
def recommend_recipes(user_ingredients, mood=None, goal=None):
    user_query = ' '.join(user_ingredients)
    user_vec = vectorizer.transform([user_query])
    similarities = cosine_similarity(user_vec, tfidf_matrix).flatten()

    df_copy = df.copy()
    df_copy['similarity'] = similarities

    if mood and mood != "No Preference":
        df_copy = df_copy[df_copy['Mood_Tags'].apply(lambda tags: mood in tags)]
    if goal and goal != "No Preference":
        df_copy = df_copy[df_copy['Health_Goal_Tags'].apply(lambda goals: goal in goals)]

    df_sorted = df_copy.sort_values(by='similarity', ascending=False)

    results = []
    for _, row in df_sorted.iterrows():
        results.append({
            'Title': row['Title'],
            'Mood_Tags': row['Mood_Tags'],
            'Health_Goal_Tags': row['Health_Goal_Tags'],
            'Ingredients': row['Ingredients'],
            'Instructions': row['Instructions'],
            'similarity': row['similarity']
        })

    return results

# ---------- Routes ----------
@app.route('/',methods=['GET'])
def intro():
    return render_template('intro.html')

@app.route('/home', methods=['GET', 'POST'])
def index():
    moods = ['No Preference', 'Tired', 'Happy', 'Festive', 'Comforting', 'Adventurous']
    goals = ['No Preference', 'Weight Loss', 'High Protein', 'Quick Meal', 'Balanced Diet', 'Vegan']
    ingredients = sorted(set(i for sublist in df['Cleaned_Ingredients'].apply(eval) for i in sublist))

    results_to_show = []

    if request.method == 'POST':
        selected_ingredients = request.form.getlist('ingredients')
        typed_ingredients = request.form.get('typed_ingredients', '')
        mood = request.form.get('mood')
        goal = request.form.get('goal')

        if typed_ingredients:
            selected_ingredients += [i.strip() for i in typed_ingredients.split(',') if i.strip()]

        if selected_ingredients or mood != "No Preference" or goal != "No Preference":
            results_to_show = recommend_recipes(selected_ingredients or [""], mood, goal)[:5]

    return render_template('index.html',
                           moods=moods,
                           goals=goals,
                           ingredients=ingredients,
                           results=results_to_show)

@app.route('/download', methods=['GET'])
def download():
    mood = request.args.get('mood')
    goal = request.args.get('goal')
    typed_ingredients = request.args.get('typed_ingredients', '')
    user_ingredients = [i.strip() for i in typed_ingredients.split(',') if i.strip()]
    results = recommend_recipes(user_ingredients or [""], mood, goal)[:5]

    df_export = pd.DataFrame(results)
    output = io.StringIO()
    df_export.to_csv(output, index=False)
    output.seek(0)

    return send_file(io.BytesIO(output.getvalue().encode()),
                     mimetype='text/csv',
                     as_attachment=True,
                     download_name='recipes.csv')

@app.route('/download/pdf', methods=['GET'])
def download_pdf():
    mood = request.args.get('mood')
    goal = request.args.get('goal')
    typed_ingredients = request.args.get('typed_ingredients', '')
    user_ingredients = [i.strip() for i in typed_ingredients.split(',') if i.strip()]
    results = recommend_recipes(user_ingredients or [""], mood, goal)[:5]

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    flow = []

    for r in results:
        flow.append(Paragraph(f"<b>{r['Title']}</b>", styles['Title']))
        tags = ', '.join(r['Mood_Tags'] + r['Health_Goal_Tags'])
        flow.append(Paragraph(f"<b>Tags:</b> {tags}", styles['Normal']))
        flow.append(Paragraph("<b>Ingredients:</b>", styles['Normal']))
        flow.extend([Paragraph(f"- {ing}", styles['Normal']) for ing in r['Ingredients']])
        flow.append(Paragraph("<b>Instructions:</b>", styles['Normal']))
        steps = r['Instructions'].replace('\n', '. ').split('.')
        flow.extend([Paragraph(f"{i+1}. {s.strip()}", styles['Normal']) for i, s in enumerate(steps) if s.strip()])
        flow.append(Spacer(1, 20))

    doc.build(flow)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="recipes.pdf", mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
