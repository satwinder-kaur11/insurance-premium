from fastapi import FastAPI
from pydantic import BaseModel,Field,computed_field
from typing import List,Literal,Annotated
import pickle
import numpy as np
import pandas as pd

# import the ml model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

app=FastAPI()
# pydantic model to validate incoming data
class UserInput(BaseModel):
    age : Annotated[int,Field(...,gt=0,lt=120,description='Age of the User')]
    weight : Annotated[float,Field(...,gt=0,description='weight of the user')]
    height : Annotated[float,Field(...,gt=0,lt=2.5,description='height of the user')]
    income_lpa : Annotated[float,Field(...,gt=0,description='annual salary of the user in lpa')]
    smoker : Annotated[bool,Field(...,description='Is a user smoker')]
    city : Annotated[str,Field(...,description='city of the user')]
    occupation : Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'],Field(...)]