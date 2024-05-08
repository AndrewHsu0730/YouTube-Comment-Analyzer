from flask import Flask, render_template, request
import os
import pandas as pd
from analyzer import extract_comment, translate_comment, process_comment, generate_word_cloud, calculate_score, identify_sentiment, generate_bar_chart

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/", methods = ["POST"])
def read_url():
    url = request.form["url"]
    comment_list = extract_comment(url, 1) # Extract comments
    df = pd.DataFrame(comment_list, columns = ["Comments"])
    df["Comments"] = df["Comments"].apply(translate_comment) # Translate comments
    df = process_comment(df, "Comments") # Process comments
    word_cloud = generate_word_cloud(df["Comments"]) # Generate word cloud
    word_cloud.savefig(os.path.join("static", "images", "word_cloud.png")) # Save the word cloud
    df = calculate_score(df, "Comments")
    df["Sentiments"] = df["Compound Scores"].apply(identify_sentiment)
    score_statement = f"Average compound score: {df["Compound Scores"].mean()}"
    sentiment_count_df = df["Sentiments"].value_counts().sort_index(ascending = False)
    bar_chart = generate_bar_chart(sentiment_count_df) # Generate bar chart
    bar_chart.savefig(os.path.join("static", "images", "bar_chart.png")) # Save the bar chart
    return render_template("dashboard.html")

@app.route("/login")
def login():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug = True, host = "localhost", port = 8008)