import pandas as pd
from api_key import API_KEY
from googleapiclient.discovery import build
import nltk 
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from wordcloud import WordCloud
import matplotlib.pyplot as plt

my_api_key = API_KEY()
nltk.download('stopwords')
nltk.download('words')
nltk.download('vader_lexicon')
youtube = build("youtube", "v3", developerKey = my_api_key)
stop_words = stopwords.words("english")

comments = []

def extract_comment(url, pages):

    if int(pages) > 2500:
        raise Exception("The number of pages to extract can't exceed 2500 due to quota limit.") 
    
    if "&" in url:
        video_id = url[(url.index("v=") + 2):url.index("&")]
    else:
        video_id = url[(url.index("v=") + 2):]

    request = youtube.commentThreads().list(
        part = "snippet",
        videoId = video_id,
        maxResults = 100
    )
    
    response = request.execute()
    
    n = 0
    
    while n < int(pages):
        try:
            request = youtube.commentThreads().list(
                part = "snippet",
                videoId = video_id,
                maxResults = 100,
                pageToken = response["nextPageToken"]
            )
            response = request.execute()
            
            for item in response["items"]:
                comment = item["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
                comments.append(comment)
            n += 1
        except:
            request = youtube.commentThreads().list(
                part = "snippet",
                videoId = video_id,
                maxResults = 100,
            )
            response = request.execute()
            
            for item in response["items"]:
                comment = item["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
                comments.append(comment)
            n += 1
        
    return comments


comment_list = extract_comment(input("Enter the url of video: "), input("Enter the number of pages(100 comments per page) to extract: "))

df = pd.DataFrame(comment_list, columns = ["Comments"])

df["Comments"] = df["Comments"].apply(lambda comment: " ".join(word.title() for word in comment.split() if word not in stop_words))

df["Comments"] = df[df["Comments"] != ""]

df = df.dropna()

word_cloud = WordCloud(collocations = False, max_words = 30, background_color = "white")

word_cloud.generate("".join(df["Comments"]))

plt.imshow(word_cloud, interpolation = "bilinear")
plt.axis("off")
plt.show()


analyzer = SentimentIntensityAnalyzer()

df["Sentiment scores"] = df["Comments"].apply(lambda comment: analyzer.polarity_scores(comment))

df["Compound Scores"] = df["Sentiment scores"].apply(lambda sentiment_score: sentiment_score["compound"])

def identify_sentiment_of_comment(compound_score):
    if compound_score >= 0.2:
        return "positive"
    elif compound_score <= -0.2:
        return "negative"
    else:
        return "neutral"

df["Sentiments"] = df["Compound Scores"].apply(identify_sentiment_of_comment)

print("Average compound score:", df["Compound Scores"].mean())

sentiment_count_df = df["Sentiments"].value_counts().sort_index(ascending = False)

plt.bar(sentiment_count_df.index, sentiment_count_df.values, 0.4)
plt.title("Number of Comments by Sentiment")
plt.show()

