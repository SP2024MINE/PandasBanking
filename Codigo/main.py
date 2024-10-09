from fastapi import FastAPI
import uvicorn
import pandas as pd
import joblib

app = FastAPI(debug=True, title="API Prediccion de subscripcion", version="0.1",summary="API para predecir si el cliente subscribira un deposito")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/predict")
async def predict(data: dict): # se recibe un diccionario
    model = joblib.load("../Datos/mi_primer_pipeline.pkl") # se carga el modelo 
    df = pd.DataFrame(data)
    prediction = model.predict(df)
    if prediction[0] == 0:
        return {"prediction": "Si va a subscribir a un deposito"}
    else:
        return {"prediction": "No va a subscribir a un deposito"}
