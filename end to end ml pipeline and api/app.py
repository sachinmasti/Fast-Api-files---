from fastapi import FastAPI
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import joblib
import pandas as pd

app = FastAPI()

class base(BaseModel):
    '''creating a data validation using Pydantic'''
    pclass: Annotated[int, Field(..., gt=0, le=3, description='enter a passenger class')]
    sex: Annotated[str, Field(..., description='enter a passenger gender')]
    age: Annotated[int, Field(..., gt=0, description='enter a passenger age')]
    fare: Annotated[int | float, Field(..., description='enter a fare amount passenger paid')]
    sibsp: Annotated[int, Field(..., description='enter a passenger siblings details')]
    parch: Annotated[int, Field(..., description='enter a passenger parents details')]
    embark_town: Literal['Southampton', 'Cherbourg', 'Queenstown']

    @computed_field()
    @property
    def adult_male(self)->bool:
        return self.sex == 'male' and 20 <= self.age < 30


def model_load():
    '''loading a joblib file for prediction'''
    with open('titanic_model_path.pkl', 'rb') as f:
        model = joblib.load(f)
    return model


model = model_load()


@app.post('/details')
def func(info: base):
    '''getting a input from user and predict passenger is survived and not survived'''
    data = info.model_dump()
    input_df = pd.DataFrame([data])

    pred = model.predict(input_df)[0]

    return {
        'prediction': int(pred),
        'result': 'survived' if pred == 1 else 'not survived'
            }
