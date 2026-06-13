import pandas as pd
import numpy as np
from warnings import filterwarnings

from colorama import Fore,Style,init
import time
init(autoreset=True)

import joblib
from transform import feature_engineering

filterwarnings('ignore',category=UserWarning,module='matplotlib')
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder,MinMaxScaler
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix
from sklearn.compose import ColumnTransformer
from sklearn.compose import make_column_selector
from sklearn.metrics import classification_report
from xgboost import XGBClassifier



#
# def feature_engineering(df)->int:
#     df = df.copy()
#
#     df['family'] = df['sibsp'] + df['parch']
#     df['is_alone'] = (df['family'] ==0).astype(int)
#
#     df['age_category'] = pd.cut(df['age'], bins=[0, 19, 29, 39, 49, 59, 69, 120],
#                                 labels=[ 'teenager','adult','middle','old_middle','old','more_old','pure_old'])
#     df.drop(columns=['sibsp','parch','embarked','class','who','deck','alive','alone'],inplace=True)
#
#     return df

# df = feature_engineering(df)

def data_split():
    ''' splitting a data for training and testing purpose '''
    df = sns.load_dataset('titanic')
    x_train,x_test,y_train,y_test = train_test_split(df.drop(columns='survived'),
                                                     df['survived'],
                                                     shuffle=True,
                                                     stratify=df['survived'],
                                                     test_size=0.2,
                                                     random_state=42)
    return x_train,x_test,y_train,y_test


def model_pipe():
    ''' build a sklearn pipeline for automate ml workflow and avoid data leakage '''
    feature_trans = Pipeline(steps=[
        ('custom_trans',FunctionTransformer(feature_engineering,validate=False))
    ])

    cate_pipe = Pipeline(steps=[
        ('impute',SimpleImputer(strategy='most_frequent')),
        ('ohe',OneHotEncoder(drop='first',handle_unknown='ignore'))
    ])

    num_pipe = Pipeline(steps=[
        ('impute',SimpleImputer(strategy='mean',add_indicator=True)),
        ('scale',MinMaxScaler())
    ])

    processor = ColumnTransformer(transformers=[
        ('categorical',cate_pipe,make_column_selector(dtype_include=['str','object','category'])),
        ('numerical',num_pipe,make_column_selector(dtype_include=['float','int']))
    ],remainder='passthrough')

    main_pipe = Pipeline(steps=[
        ('feature_en',feature_trans),
        ('process',processor),
        ('model',XGBClassifier(max_leaves=5,
                               max_depth=4,
                               n_estimators=200,
                               random_state=42))
    ])
    return main_pipe

def model_train(model_path='titanic_model_path.pkl'):
    '''training a model and saving it using joblib'''

    x_train,x_test,y_train,y_test = data_split()
    print(f'{Fore.GREEN} data split for train and test purpose')

    time.sleep(4)

    pipeline = model_pipe()
    print(f'{Fore.GREEN} model  pipline is loading')

    time.sleep(4)

    pipeline.fit(x_train,y_train)
    print(f'{Fore.LIGHTMAGENTA_EX} model is trained🌿')

    time.sleep(4)

    y_pred = pipeline.predict(x_test)
    acc = classification_report(y_test,y_pred)
    cn = confusion_matrix(y_test,y_pred)

    print(f'{Fore.LIGHTCYAN_EX} classification report is \n {acc}')
    print(f'{Fore.LIGHTCYAN_EX} confusion matrix is \n {cn}')

    joblib.dump(pipeline,model_path)
    print(f'{Fore.GREEN} model is saved and ready for predictions 👿')



if __name__ =='__main__':
    model_train()


















