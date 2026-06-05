from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import StreamingResponse
import json
import io
import pandas as pd
import matplotlib.pyplot as plt
import mplcyberpunk as cp

app = FastAPI()


def load_data():
    """load a data from json file"""
    with open('info.json', 'r') as f:
        data = json.load(f)
    return data


@app.get('/')
def message():
    return {'message': 'sachin masti'}

@app.get('/about')
def about():
    return {'about section': 'hi bro hows going'}


@app.get('/view_patients')
def view_patients():
    data = load_data()
    return {'patients': data}

@app.get('/patients_info/{patient_id}')
def patients_info(patient_id: int = Path(..., description='enter a patient id of view a particular patient', example=1)):
    data = load_data()
    try:
        return {'patients_info': data[patient_id - 1]}
    except IndexError:
        raise HTTPException(status_code=404, detail='patient not found')


@app.get('/sort')
def sort_data(
    sort_by: str = Query(..., description='Sort data on basis of age'),
    order: str = Query(..., description='Sort in asc or desc order')
):
    valid_fields = ['age']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Choose a valid field. Valid fields: {valid_fields}')

    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Enter a valid order: asc or desc')

    data = load_data()

    sort_order = True if order == 'desc' else False

    sorted_data = sorted(data, key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data


def load_df():
    df = pd.read_json('info.json')
    return df


def bar_plot(df):
    plt.style.use('cyberpunk')
    fig, ax = plt.subplots(figsize=(10, 6))

    colors = ['#FF6B9D' if g == 'Female' else '#4FC3F7' for g in df['gender']]
    bar = ax.bar(x=df['name'], height=df['age'], color=colors)

    ax.set_title('Patient Age by Gender', fontsize=14, fontweight='bold')
    ax.set_ylabel('Age')
    ax.set_xlabel('Patient Name')
    ax.tick_params(axis='x', rotation=45)
    cp.add_bar_gradient(bars=bar)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf


@app.get('/plot')
def get_plot():
    df = load_df()
    buf = bar_plot(df)
    return StreamingResponse(buf, media_type='image/png')
