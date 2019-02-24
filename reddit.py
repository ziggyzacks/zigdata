import os
import pickle
import pandas as pd

import praw
import nltk

nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

from sklearn.feature_extraction.text import CountVectorizer

reddit = praw.Reddit(client_id=os.environ.get('REDDIT_CLIENT_ID'),
                     client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
                     user_agent=os.environ.get('REDDIT_USER_AGENT'))

headlines = set()
for submission in reddit.subreddit('politics').new(limit=None):
    headlines.add(submission.title)

sia = SIA()
results = []

for line in headlines:
    pol_score = sia.polarity_scores(line)
    pol_score['headline'] = line
    results.append(pol_score)

df = pd.DataFrame.from_records(results)
print(df.head(10))
df.to_parquet('headlines.parquet')