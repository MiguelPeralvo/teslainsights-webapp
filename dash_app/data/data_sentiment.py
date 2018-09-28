import pandas as pd
import sqlite3
import numpy as np
import traceback
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
from requests import Request
import datetime as dt


def query_tesla_sentiment(url, params):

    try:
        url = Request('GET', f'{url}', params=params).prepare().url
        df = pd.read_json(url)
        # TODO: Calculate volatility
        df['volatility'] = np.random.uniform(0, 5, df.shape[0])
    except:
        logger.warning(f'Problem when accessing url {url}: {traceback.format_exc()}')
        df = pd.DataFrame(columns=['sentiment_absolute', 'volatility'])

    return df

