from io import BytesIO

import numpy as np
import pandas as pd
from app.core.config import settings


class DataService:
    def __init__(self):
        self.df = pd.read_csv(settings.DATA_FILE_PATH)
        self.df = self.df.dropna()

    def get_numeric_columns(self):
        return list(self.df.select_dtypes(include=['int64', 'float64']).columns)

    def get_categorical_columns(self):
        return list(self.df.select_dtypes(include=['object', 'category']).columns)

    def get_filtered_data(self, filters=None):
        if filters is None:
            return self.df

        filtered_df = self.df.copy()
        for column, filter_range in filters.items():
            if column in self.get_numeric_columns():
                min_val, max_val = filter_range
                filtered_df = filtered_df[(filtered_df[column] >= min_val) & (filtered_df[column] <= max_val)]
            elif column in self.get_categorical_columns():
                if len(filter_range) == 0:
                    continue
                filtered_df = filtered_df[filtered_df[column].isin(filter_range)]

        return filtered_df

    def get_column_ranges(self):
        ranges = {}

        for col in self.get_numeric_columns():
            ranges[col] = [self.df[col].min(), self.df[col].max()]

        ranges = {
            key: [int(value[0]), int(value[1])] if np.issubdtype(value[0], np.integer)
            else [float(value[0]), float(value[1])]
            for key, value in ranges.items()
        }

        for col in self.get_categorical_columns():
            ranges[col] = self.df[col].unique().tolist()

        return ranges

    def load_new_dataframe(self, content):
        self.df = pd.read_csv(BytesIO(content))
        self.df = self.df.dropna()


data_service = DataService()
