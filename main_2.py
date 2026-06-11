from fastapi import FastAPI,HTTPException,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,EmailStr,computed_field
from typing import Annotated,Any,Literal,Optional
from colorama import Fore,Style,init
init(autoreset=True)
import json

app = FastAPI()


class date(BaseModel):
    year : int
    month : int
    date : int

class patient(BaseModel):
    id:Annotated[int,Field(...,description='enter patient id',examples=[1,2])]
    name:Annotated[str,Field(...,description='enter patient name')]
    age: Annotated[int,Field(...,gt=0,lt=120,description='enter patient age')]
    gender : Literal['Male','Female','Other']
    weight : Annotated[float,Field(...,description='enter your weight')]
    height : Annotated[float,Field(...,description='enter your height')]
    diagnosis: Optional[Annotated[str,Field(...,description='enter diagnosis if you have any do it before come here',examples=['Diabetes','Asthma','Hypertension','Heart Disease','Thyroid'])]] = None
    admission_date: Optional[date] = None

    @computed_field
    @property
    def bmi(self) -> float:
        height_m = self.height / 100
        return round(self.weight / (height_m ** 2), 2)


def load_data(): #helper func that load a our json data
    with open('info.json') as j:
        data = json.load(j)
        return data
print(type(date))
print(date)

def update_file(data):
    with open('info.json','w') as f:
        json.dump(data,f)
    # return  data

@app.get('/')
def welcome()->str:
    return f'{Fore.LIGHTMAGENTA_EX} 🕊️ welcome in our hospital 👿'

@app.get('/info')
def info()->str:
    return (f'our hospital is founder in 1930' 
            f'\n our hospital is very good at service and very quick service and affordable 🦣')

@app.get('/patients')
def view_data():
    data = load_data()
    return {'patient':data}

@app.post('/update')
def insert_data(patient: patient):
    data = load_data()

    if any(p['id'] == patient.id for p in data):
        raise HTTPException(
            status_code=400,
            detail='Patient already exists'
        )

    data.append(patient.model_dump())

    update_file(data)

    return JSONResponse(
        status_code=201,
        content={'message': 'Appointment booked'}
    )