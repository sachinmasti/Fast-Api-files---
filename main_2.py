from fastapi import FastAPI,HTTPException,Query
from fastapi.responses import JSONResponse
from plotly.graph_objs.indicator.gauge import step
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
    diagnosis: Optional[Annotated[str,Field(description='enter diagnosis if you have any do it before come here',examples=['Diabetes','Asthma','Hypertension','Heart Disease','Thyroid'])]] = None
    admission_date: Optional[date] = None

    @computed_field
    @property
    def bmi(self) -> float:
        height_m = self.height / 100
        return round(self.weight / (height_m ** 2), 2)


class updatepatient(BaseModel):
        name: str | None = None
        age: int | None = None
        gender: Literal['Male', 'Female', 'Other'] | None = None
        weight: float | None = None
        height: float | None = None
        diagnosis: str | None = None
        admission_date: date | None = None

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
def insert_data(patient : patient):
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

@app.put('/edit/{patient_id}')
def edit(patient_id: int, patient_edit: updatepatient):

    data = load_data()

    existing_patient = next(
        (p for p in data if p['id'] == patient_id),
        None
    )

    if existing_patient is None:
        raise HTTPException(
            status_code=404,
            detail='patient not found'
        )

    updated_data = patient_edit.model_dump(exclude_unset=True)

    for key, value in updated_data.items():
        existing_patient[key] = value

    patient_obj = patient(**existing_patient)

    existing_patient.update(
        patient_obj.model_dump()
    )

    update_file(data)

    return JSONResponse(
        status_code=200,
        content={'message': 'patient info updated'}
    )
@app.delete('/delete/{patient_id}')
def patient_delete(patient_id: int):

    data = load_data()

    if not any(p['id'] == patient_id for p in data):
        raise HTTPException(
            status_code=404,
            detail='patient not found'
        )

    data = [p for p in data if p['id'] != patient_id]

    update_file(data)

    return JSONResponse(
        status_code=200,
        content={'message': 'patient deleted'}
    )



























# @app.put('/edit/{patient_id}')
# def edite(patient_id:int,patient_edit:updatepatient):
#     data = load_data()
#
#     if patient_id not in patient.id:
#         raise HTTPException(status_code=404,detail='patient not found')
#
#     existing_patient = data[patient_id]
#     updated_patent = patient_edit.model_dump(exclude_unset=True)
#     # data[patient_id] = updated_patent
#
#     for key,value in existing_patient.item():
#         existing_patient[key] = value
#
#     existing_patient['id'] = data[patient_id]
#
#     patient_Pydantic_obj = patient(**existing_patient)
#     # -> pydantic object -> dict
#     existing_patient_info = patient_Pydantic_obj.model_dump(exclude='id')
#
#     # add this dict to data
#     data[patient_id] = existing_patient_info
#
#     return JSONResponse(status_code=200,content={'massge':'patient info updated'})





















