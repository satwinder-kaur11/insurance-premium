from fastapi import FastAPI
from fastapi.responses import JSONResponse
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
    
    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight/(self.height**2)
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi>30:
            return 'high risk'
        elif self.smokeror or self.bmi>27:
            return 'medium risk'
        else:
            return 'low risk'
    @computed_field
    @property
    def age_group(self)-> int:
        if self.age < 25:
            return 'young'
        elif self.age < 45:
            return 'adult'
        elif self.age <  60:
            return 'middle-aged'
        else:
            return 'senior'

app.post('/predict')
def predict_premium(data:UserInput):
    input_df=pd.DataFrame([{
        'bmi':data.bmi ,
        'age_group': data.age_group,
        'city' :data.city,
        'income_lpa': data.income_lpa,
        'occupation':data.occupation
    }])
    prediction=model.predict(input_df)[0]
    return JSONResponse(status_code=200,content={'predicted_category':prediction})