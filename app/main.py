from fastapi import FastAPI
from pydantic import BaseModel
import json
from pathlib import Path
from app.recommender import recommend_query
from app.dataloader_2 import load_existing_data  # Import the scrape function
from app.dataloader_2 import load_data_and_update_index

app = FastAPI()
DATA_PATH = Path("data/shl_assessments.json")

class QueryRequest(BaseModel):
    query: str

@app.get("/")
def root():
    return {"message": "SHL Recommender API is running 🚀"}

@app.get("/recommend")
def get_all_assessments():
    if DATA_PATH.exists():
        with open(DATA_PATH, "r") as f:
            data = json.load(f)
        return {"results": data}
    return {"results": []}

@app.post("/recommend")
def recommend(req: QueryRequest):
    return {"results": recommend_query(req.query)}


# New endpoint to trigger data scraping
@app.post("/update-data")
def update_data():
    try:
        load_data_and_update_index()  # Call the function to scrape the data
        return {"message": "Data updated successfully!"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/health")
def healthcheck():
    return {"status": "healthy"}

