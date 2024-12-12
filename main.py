from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI is running!"}

# Modello per i dati che FastAPI riceverà
class DataModel(BaseModel):
    shapes: list  # Lista di forme o figure rilevate
    analysis: dict  # Dizionario con i dati analizzati

# Endpoint POST per ricevere dati
@app.post("/data")
async def receive_data(data: DataModel):
    print(f"Dati ricevuti: {data}")  # Stampa i dati nei log
    # Puoi aggiungere ulteriori elaborazioni qui, se necessario
    return {"message": "Data received successfully!", "received_data": data.dict()}
