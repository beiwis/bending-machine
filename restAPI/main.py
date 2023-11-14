from fastapi import FastAPI
from typing import Union
from bending_machine import machine

machine = machine() #we create a new machine object 
app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/get_mode")
async def get_mode():
    return {machine.mode}

@app.get("/get_state")
async def get_state():
    return {machine.state}

@app.get("/get_curr_measure/{measure_id}")
#TODO: map each id to a measure, I was thinking, encoder, strain and force.
async def get_current_measures(id: int = 0):
    if id == 0:
        return {machine.measurements}
    elif id <= 3: 
        return{machine.measurements[id-1]}
    
@app.get("/get_prev_measure/{measure_id}")
async def get_previous_measures(id: int = 0, type: int = 0, date: str = ''):#TODO: map the int values to its meaning 
    """Returns the measures from the last test, can be filtered by sensor, type of test, and date (DDMMYYYY_HHMMSS format).
    In the occurance that no csv files match the specified criteria, it will return the closest by date, matching the specified type (if any).
    In the event that there are no csv files at all, it will return an Error"""