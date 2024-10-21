from fastapi import FastAPI
import uvicorn
import pandas as pd
import joblib

app = FastAPI(debug=True, title="API subscripción", version="0.1",summary="API para predecir si el cliente subscribirá un deposito")

@app.get("/")
async def root():
    return {"message": "Predicción de suscripción a deposito"}

@app.post("/predict")
async def predict(data: dict): # se recibe un diccionario
    model = joblib.load("../Datos/bank_mkt_pipeline.pkl") # se carga el modelo 
    df = pd.DataFrame(data)
    prediction = model.predict(df)
    prob = model.predict_proba(df)

    if prediction[0] == 'yes':
        return {"prediction": "Si va a subscribir a un deposito",
                "probabilidad": prob}              
    else:
        return {"prediction": "No va a subscribir a un deposito",
                "probabilidad": prob}
