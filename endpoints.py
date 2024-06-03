from typing import Union
import nltk
import uvicorn
from fastapi.responses import JSONResponse
from pydantic import BaseModel 
from nltk.corpus import stopwords
from fastapi import FastAPI, File, UploadFile,Form
from text_processing import TextProcessor
from evaluation_file import calc_MAP,calc_MRR,calc_avg_precision,calc_avg_recall
from calc_cluster import calc_avg_precision_cluster,calc_avg_reacll_cluster,calc_MRR_cluster,calc_MAP_cluster,calc_avg
from fastapi.responses import PlainTextResponse
from indexing_data import indexing_data
from matching import match_data
from suggest_query import suggest_corrected_query
from fastapi.middleware.cors import CORSMiddleware
class TextInput(BaseModel):
    text: str

class QueryData(BaseModel):
    query_id: str
    input_data: str


app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, restrict in production
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/text_processing/")
def text_processing(input_data: TextInput):
    processor = TextProcessor()
    clean_txt = processor.process_text(text=input_data.text)
    return {"proceesed_txt" : clean_txt}


@app.get("/calc_MAP/{dataset_number}")
def calc_MAP_endpoint(dataset_number:int):    
    value=calc_MAP(dataset_number=dataset_number)
    value_with_percentage = f"{value}%"
    return {"Mean Average Precision (MAP)" : value_with_percentage}


@app.get("/calc_MRR/{dataset_number}")
def calc_MRR_endpoint(dataset_number:int):
    value=calc_MRR(dataset_number)
    value_with_percentage = f"{value}%"
    return {"Mean Reciprocal Rank (MRR):" : value_with_percentage}


@app.get("/calc_precision/{dataset_number}")
def calc_precision_endpoint(dataset_number:int):
    value=calc_avg_precision(dataset_number=dataset_number)
    return {"precision@10_avg:" : value}


@app.get("/calc_recall/{dataset_number}")
def calc_recall_endpoint(dataset_number:int):
   
    value=calc_avg_recall(dataset_number=dataset_number)
    return {"recall_avg:" : value}


@app.get("/calc_MAP_cluster")
def calc_MAP_endpoint():    
    value=calc_MAP_cluster()
    value_with_percentage = f"{value}%"
    return {"Mean Average Precision (MAP)" : value_with_percentage}


@app.get("/calc_MRR_cluster")
def calc_MRR_endpoint():
    value=calc_MRR_cluster()
    value_with_percentage = f"{value}%"
    return {"Mean Reciprocal Rank (MRR):" : value_with_percentage}


@app.get("/calc_precision_cluster")
def calc_precision_endpoint():
    value=calc_avg_precision_cluster()
    return {"precision@10_avg:" : value}


@app.get("/calc_recall_cluster")
def calc_recall_endpoint():
   
    value=calc_avg_reacll_cluster()
    return {"recall_avg:" : value}

@app.get("/indexing")
def indixing_data_endpoint(input_data: TextInput):
    value=indexing_data()
    return {"Result:" : value}

@app.post("/matching/{dataset_number}")
def matching_data_endpoint(input_data: TextInput,dataset_number:int):
   try:
        value = match_data(input_data.text, dataset_number)
        
        # Check if result_dict is empty
        if not value:
            return JSONResponse(
                status_code=200,
                content={
                    "dataset_number": dataset_number,
                    "matched_data":{}
                }
            )
        
        # Format the output
        response = {
            "dataset_number": dataset_number,
            "matched_data": value
        }
        
        return JSONResponse(status_code=200, content=response)
    
   except Exception as e:
        # Handle exceptions and return a 500 status code with an error message
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@app.get("/k-mean")
def kMean_avg_endpoint():
    value=calc_avg()
    value_with_percentage = f"{value}%"
    return {"Result:" : value_with_percentage}

@app.get("/correct/{dataset_number}")
def correct_query_endpoint(input_data: TextInput):
    value=suggest_corrected_query(input_data.text)
    return {"Result:" : value}

