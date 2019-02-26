import os
import sys
import pandas as pd
import praw
import nltk
import s3fs
import time
from datetime import datetime
from time import sleep
import logging
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s')
logger = logging.getLogger("reddit")
logger.setLevel(logging.INFO)

try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

CLIENT_ID = os.environ.get('REDDIT_CLIENT_ID')
CLIENT_SECRET = os.environ.get('REDDIT_CLIENT_SECRET')
USER_AGENT = os.environ.get('REDDIT_USER_AGENT')
NAP_TIME = int(os.environ.get('REDDIT_EXTRACTOR_NAPTIME', 900))
SUBREDDITS = pd.read_html('http://redditmetrics.com/top')[0].Reddit.str.replace('/r/', '').unique().tolist()


class RedditHeadlineExtractor:

    def __init__(self, client_id, client_secret, user_agent):
        self.reddit = praw.Reddit(client_id=client_id,
                                  client_secret=client_secret,
                                  user_agent=user_agent)
        self.sia = SIA()
        self.fs = s3fs.S3FileSystem()

    @classmethod
    def from_environment(cls):
        return cls(CLIENT_ID, CLIENT_SECRET, USER_AGENT)

    def fetch_headlines_from_s3(self, pattern='s3://zigdata.org/reddit-headlines/*'):
        headline_files = self.fs.glob(pattern)
        if len(headline_files) > 0:
            dfs = []
            for f in headline_files:
                logger.info(f'Loading: {f}')
                dfs.append(pd.read_parquet(f))
            headlines = pd.concat(dfs)
            logger.info(f"Found {len(headlines)} headlines in {len(headline_files)} records")
        else:
            logger.info('No headlines files found in S3.')
            headlines = None
        return headlines

    def gather_headlines(self, subreddits=None):
        if subreddits is None:
            subreddits = SUBREDDITS

        rows = []
        with ThreadPoolExecutor(cpu_count() * 2) as pool:
            for hls in pool.map(self._gather_headlines, subreddits):
                rows.extend(hls)
        return rows

    def _gather_headlines(self, subreddit):
        new_headlines = set()
        records = []

        logger.info(f"Fetching new headlines from {subreddit}")
        for submission in self.reddit.subreddit(subreddit).new(limit=None):
            title = submission.title
            if title not in new_headlines:
                new_headlines.add(title)
                record = {
                    "title": title,
                    "ups": submission.ups,
                    "subreddit": subreddit,
                    "created_epoch": submission.created_utc,
                    "ncomments": submission.num_comments,
                    "extracted_epoch": time.time()
                }
                records.append(record)
        logger.info(f"Found {len(new_headlines)} new headlines in the {subreddit} subreddit")
        return records

    def build_df_from_headlines(self, headlines):
        results = []
        logger.info('Calculating sentiment scores')
        for record in headlines:
            pol_score = self.sia.polarity_scores(record['title'])
            results.append({**record, **pol_score})
        df = pd.DataFrame.from_records(results)
        df['timestamp'] = pd.to_datetime(df.created_epoch, unit='s')
        return df


if __name__ == "__main__":
    extractor = RedditHeadlineExtractor.from_environment()
    headlines = extractor.gather_headlines()
    df = extractor.build_df_from_headlines(headlines)
    logger.info('Persiting to s3')
    df.to_parquet(f's3://zigdata.org/reddit-headlines/{datetime.now().strftime("%Y-%m-%d_%H%M%S")}.parquet.gzip',
                  compression='gzip')
    logger.info(f'Sleeping for {NAP_TIME // 60} minutes')
    # 15 minutes
    sleep(NAP_TIME)
    sys.exit(0)
