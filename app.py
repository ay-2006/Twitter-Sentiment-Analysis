from flask import Flask, render_template, request
import tweepy
import re
from textblob import TextBlob

app = Flask(__name__)

# Twitter API setup
bearer_token = 'AAAAAAAAAAAAAAAAAAAAACvXwwEAAAAAWNH3E6Wm0QHDAfk%2FxoSDB0kflkM%3D9IDNQ1p9VeidPyP3cvMCUjDzPvNnumPNEMbiyc7N0WJ7lQbZVG'
client = tweepy.Client(bearer_token=bearer_token)

# Function to fetch tweets using Twitter API v2
def fetch_tweets_v2(query, count=10):
    try:
        tweets = client.search_recent_tweets(query=query, max_results=count, tweet_fields=["created_at"])
        tweet_list = []
        for tweet in tweets.data:
            tweet_list.append(tweet.text)
        return tweet_list
    except Exception as e:
        print(f"Error fetching tweets: {e}")
        return []

# Function to preprocess tweet text
def preprocess_text(text):
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'@\w+|#\w+', '', text)
    text = re.sub(r'[^A-Za-z\s]', '', text)
    text = text.lower()
    return text

# Function to analyze sentiment
def analyze_sentiment(tweet):
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        return "Positive"
    elif analysis.sentiment.polarity < 0:
        return "Negative"
    else:
        return "Neutral"

# Route for the homepage
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form.get("query")
        tweets = fetch_tweets_v2(query, count=10)
        results = []
        
        for tweet in tweets:
            preprocessed_tweet = preprocess_text(tweet)
            sentiment = analyze_sentiment(preprocessed_tweet)
            results.append({
                "original": tweet,
                "preprocessed": preprocessed_tweet,
                "sentiment": sentiment
            })
        
        return render_template("index.html", results=results, query=query)
    
    return render_template("index.html", results=None)

if __name__ == "__main__":
    app.run(debug=True)
