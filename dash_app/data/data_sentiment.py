import pandas as pd
from datetime import datetime, timedelta
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
        df = generate_data(params)
        # url = Request('GET', f'{url}', params=params).prepare().url
        # # We revert the dataframe for the visualisation.
        # df = pd.read_json(url).iloc[::-1]
        # # TODO: Calculate volatility
        df['volatility'] = df['sentiment_absolute'].rolling(20).std()
        df['volatility'] = df['volatility'].bfill()
        # # df['volatility'] = np.random.uniform(0, 5, df.shape[0])
    except:
        logger.warning(f'Problem when accessing url {url}: {traceback.format_exc()}')
        df = pd.DataFrame(
            columns=[
                'sentiment_type', 'sentiment_seconds_back', 'bin', 'created_at_epoch_ms',
                'sentiment_absolute', 'sentiment_normalized',' min_created_at_epoch_ms',
                'max_created_at_epoch_ms', 'volatility'
            ]
        )

    return df


def generate_data(params):
    map_files = {
        ('teslamonitor', 400): 'social_teslamonitor_downsample_400_15726.csv',
        ('teslamonitor', 1200): 'social_teslamonitor_downsample_1200_5663.csv',
        ('teslamonitor', 21600): 'social_teslamonitor_downsample_21600_324.csv',
        ('social_external_ensemble', 21600): 'social_external_ensemble_downsample_21600_324.csv',
        ('news_external_ensemble', 21600): 'news_external_ensemble_downsample_21600_324.csv',
    }

    data_path = '{}/{}'.format('/tmp/data', map_files[(
        params['sentiment_type'], params['downsample_freq'])
    ])

    logger.info('Reading data from {}'.format(data_path))

    df = pd.read_csv(data_path, header=0).iloc[::-1]
    epoch_x_days = int(161 * 24 * 60 * 60) * 1000

    # We move the historical data x days into the future
    df = df.assign(
        created_at_epoch_ms=df['created_at_epoch_ms']+epoch_x_days,
        min_created_at_epoch_ms=df['min_created_at_epoch_ms'] + epoch_x_days,
        max_created_at_epoch_ms=df['max_created_at_epoch_ms'] + epoch_x_days
    )

    now = datetime.utcnow() - datetime(1970, 1, 1)
    epoch_now = int((now.days * 24 * 60 * 60 + (now.seconds // 10) * 10)) * 1000

    logger.info('Selecting data older than {}'.format(epoch_now))
    # df = df.loc[df['created_at_epoch_ms'] <= epoch_now]
    return df[:params['limit']]