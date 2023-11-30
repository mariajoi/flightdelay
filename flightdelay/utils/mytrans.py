import numpy as np
import pandas as pd
from sklearn.base import TransformerMixin, BaseEstimator

class MyTrans(TransformerMixin, BaseEstimator):
    def __init__(self):
        pass

    def fit(self, X):
        self.grouped_TimeBlk = {
            'morning': ['0600-0659', '0700-0759', '0800-0859', '0900-0959', '1000-1059', '1100-1159'],
            'daytime': ['1200-1259', '1300-1359', '1400-1459', '1500-1559', '1600-1659', '1700-1759'],
            'night': ['1800-1859', '1900-1959', '2000-2059', '2100-2159', '2200-2259', '2300-2359', '0001-0559']
            }
        return self

    def transform(self, X):
        X['Month_sin'] = np.sin(2 * np.pi * X['Month'] / 12)
        X['Month_cos'] = np.cos(2 * np.pi * X['Month'] / 12)
        X['DayOfWeek_sin'] = np.sin(2 * np.pi * X['DayOfWeek'] / 7)
        X['DayOfWeek_cos'] = np.cos(2 * np.pi * X['DayOfWeek'] / 7)

        X['groups_DepTimeBlk'] = X['DepTimeBlk'].apply(lambda x: next((key for key, values in self.grouped_TimeBlk.items() if x in values), None))
        X['groups_ArrTimeBlk'] = X['ArrTimeBlk'].apply(lambda x: next((key for key, values in self.grouped_TimeBlk.items() if x in values), None))

        X = X.drop(columns = ['DepTimeBlk', 'ArrTimeBlk', 'Month', 'DayOfWeek'])

        return X
