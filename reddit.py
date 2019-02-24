import praw
import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import pickle

reddit = praw.Reddit(client_id=os.environ.get('REDDIT_CLIENT_ID'),
                     client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
                     user_agent=os.environ.get('REDDIT_USER_AGENT'))

headlines = set()
for submission in reddit.subreddit('politics').new(limit=None):
    headlines.add(submission.title)
    print(len(headlines))


sia = SIA()
results = []

for line in headlines:
    pol_score = sia.polarity_scores(line)
    pol_score['headline'] = line
    results.append(pol_score)

df = pd.DataFrame.from_records(results)
df.to_parquet('headlines.parquet')

vectorizer = CountVectorizer()
vectorizer.fit_transform(df.headline.values)

with open('vectorizer.pkl') as f:
    pickle.dumps(vectorizer)

