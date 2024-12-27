from flask import Flask, render_template, request, jsonify
import requests
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Download NLTK data for sentiment analysis
nltk.download('vader_lexicon')

# Initialize SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

app = Flask(__name__)

def fetch_quote():
    """Fetch a random motivational quote from ZenQuotes API."""
    url = "https://zenquotes.io/api/random"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            quote = data[0]['q']
            author = data[0]['a']
            return f"\"{quote}\" - {author}"
        else:
            return "Sorry, I couldn't fetch a quote right now. Please try again later."
    except Exception as e:
        return f"An error occurred: {e}"

def analyze_sentiment(text):
    """Analyze sentiment of the given text."""
    sentiment_scores = sia.polarity_scores(text)
    compound_score = sentiment_scores['compound']

    if compound_score >= 0.05:
        return 'Positive'
    elif compound_score <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

@app.route('/')
def home():
    """Render the homepage."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat requests."""
    user_input = request.form.get('user_input', '').strip()

    # Exit command
    if user_input.lower() == 'exit':
        return jsonify(response="Take care and stay motivated! Goodbye! 🌈")

    # Analyze sentiment
    sentiment = analyze_sentiment(user_input)

    # Generate response based on sentiment
    if sentiment == 'Positive':
        response = f"I'm glad you're feeling positive! 🌟 Here's a motivational quote to keep you inspired: {fetch_quote()}"
    elif sentiment == 'Negative':
        response = f"I'm sorry to hear that you're feeling down. 😔 Remember, tough times never last, but tough people do! Here's something to uplift you: {fetch_quote()}"
    else:
        response = f"Thank you for sharing your thoughts. Here's a quote to keep you going: {fetch_quote()}"

    return jsonify(response=response)

if __name__ == '__main__':
    app.run(debug=True)
