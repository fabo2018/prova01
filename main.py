from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI is running!"}
from pydantic import BaseModel

# Modello per i dati che FastAPI riceverà
class DataModel(BaseModel):
    shapes: list
    analysis: dict

# Endpoint POST per ricevere dati
@app.post("/data")
async def receive_data(data: DataModel):
    # Puoi stampare i dati nel terminale per verifica
    print(data)
    return {"message": "Data received successfully!", "received_data": data}
