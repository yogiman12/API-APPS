# import modules
from fastapi import FastAPI , Query  # import API app & validation rules.
from pydantic import BaseModel # make class for return output 
# configure Cross-Origin Resource Sharing (CORS) for the application to enable app in the directory to interacts with API
from fastapi.middleware.cors import CORSMiddleware


class BMIOutput(BaseModel):
    bmi: float
    message : str

app = FastAPI()

app.add_middleware(
    
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"]
    
)

@app.get('/') # make home route API 
def hi ():
    return {"message":"hi im ahmed"}

@app.get('/bmi')  # BMI route API 
def calc_bmi(weight: float = Query(..., gt=0.01, lt=500, description="Weight in KG"), 
             height: float = Query(..., gt=0.01, lt=4, description="Height in M")):
    """
    Calculate BMI based on weight and height.

    Args:
        weight (float, required): Weight in kilograms. 
        height (float, required): Height in meters.

    Returns:
        float: bmi result
        str: Message indicating the BMI category.
    Example:
        http://127.0.0.1:8000/bmi?weight=80&height=1.7
    Output:
        {
            "bmi": 34.602076124567475,
            "message": "BMI = 34.60, very fat, go to doctor"
        }
    """
    bmi = weight / (height ** 2)
    
    if bmi < 18:
        message = f"too skinny"
    elif 18 <= bmi < 25:
        message = f"perfect weight"
    elif 25 <= bmi < 30:
        message = f"overweight"
    else:
        message = f"very fat, go to doctor"
    
    return BMIOutput(bmi=bmi, message=message)
        
