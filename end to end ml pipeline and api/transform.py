from calendar import error

import pandas as pd

def feature_engineering(df):
    df = df.copy()

    df['family'] = df['sibsp'] + df['parch']
    df['is_alone'] = (df['family'] == 0).astype(int)

    df['age_category'] = pd.cut(
        df['age'],
        bins=[0, 19, 29, 39, 49, 59, 69, 80],
        labels=[
            'teenager',
            'adult',
            'middle',
            'old_middle',
            'old',
            'more_old',
            'pure_old'
        ]
    )

    df.drop(
        columns=[
            'sibsp',
            'parch',
            'embarked',
            'class',
            'who',
            'deck',
            'alive',
            'alone'
        ],
        inplace=True,
        errors='ignore'
    )

    return df