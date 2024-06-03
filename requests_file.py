import multiprocessing
import time
import uvicorn
import requests


def run_server():
    uvicorn.run("endpoints:app", host="127.0.0.1", port=8000, reload=False)

def is_server_running(url, timeout=100):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return True
        except requests.ConnectionError:
            time.sleep(0.1)
    return False

def text_processing_request(query):
    url = "http://127.0.0.1:8000/text_processing/"
    body = {"text": query}
    headers = {"Content-Type": "application/json"}
    if is_server_running("http://127.0.0.1:8000/docs"):
        response = requests.get(url, json=body,headers=headers)
        if response.status_code == 200:
            print("Response:", response.json())
        else:
            print("Failed to get a response:", response.status_code)
    else:
        print("Server did not start in time")

def indexing_data_request():
    url = "http://127.0.0.1:8000/indexing"
    body = {"text": "Hello, FastAPI! This is a test."}
    headers = {"Content-Type": "application/json"}
    if is_server_running("http://127.0.0.1:8000/docs"):
        response = requests.get(url, json=body,headers=headers)
        if response.status_code == 200:
            print("Response:", response.json())
        else:
            print("Failed to get a response:", response.status_code)
    else:
        print("Server did not start in time")        

def match_data_request(dataset_number,query):
    url = f"http://127.0.0.1:8000/matching/{dataset_number}"
    body = {"text": query}
    headers = {"Content-Type": "application/json"}
    if is_server_running("http://127.0.0.1:8000/docs"):
        response = requests.post(url, json=body,headers=headers)
        if response.status_code == 200:
            print("Response:", response.json())
        else:
            print("Failed to get a response:", response.status_code)
    else:
        print("Server did not start in time")        

def correct_request():
    url = f"http://127.0.0.1:8000/correct"
    body = {"text": "Hello, FastAPI! This is a test."}
    headers = {"Content-Type": "application/json"}
    if is_server_running("http://127.0.0.1:8000/docs"):
        response = requests.get(url, json=body,headers=headers)
        if response.status_code == 200:
            print("Response:", response.json())
        else:
            print("Failed to get a response:", response.status_code)
    else:
        print("Server did not start in time")                


def calc_MAP_request(dataset_number):
    url = f"http://127.0.0.1:8000/calc_MAP/{dataset_number}"   
    headers = {'accept': 'application/json'}

    if is_server_running("http://127.0.0.1:8000/docs"):
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            print("Response:", response.json())
        else:
            print("Failed to get a response:", response.status_code)
    else:
        print("Server did not start in time")        


def calc_MRR_request(dataset_number):
    url = f"http://127.0.0.1:8000/calc_MRR/{dataset_number}"   
    headers = {'accept': 'application/json'}

    if is_server_running("http://127.0.0.1:8000/docs"):
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            print("Response:", response.json())
        else:
            print("Failed to get a response:", response.status_code)
    else:
        print("Server did not start in time")      

def calc_precision_request(dataset_number):
    url = f"http://127.0.0.1:8000/calc_precision/{dataset_number}"   
    headers = {'accept': 'application/json'}
    # body={
    #     "query_id": query_id,
    #     "input_data": input_text
    # }
    print("URL:", url)
    if is_server_running("http://127.0.0.1:8000/docs"):
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            print("Response:", response.json())
        else:
            print("Failed to get a response:", response.status_code)
    else:
        print("Server did not start in time")         

def calc_recall_request(dataset_number):
    url = f"http://127.0.0.1:8000/calc_recall/{dataset_number}"   
    headers = {'accept': 'application/json'}
    # body={
    #     "query_id": query_id,
    #     "input_data": input_text
    # }
    if is_server_running("http://127.0.0.1:8000/docs"):
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            print("Response:", response.json())
        else:
            print("Failed to get a response:", response.status_code)
    else:
        print("Server did not start in time")                   


def calc_MAP_clus_request():
    url = f"http://127.0.0.1:8000/calc_MAP_cluster"   
    headers = {'accept': 'application/json'}

    if is_server_running("http://127.0.0.1:8000/docs"):
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            print("Response:", response.json())
        else:
            print("Failed to get a response:", response.status_code)
    else:
        print("Server did not start in time")        

def calc_MRR_clus_request():
    url = f"http://127.0.0.1:8000/calc_MRR_cluster"   
    headers = {'accept': 'application/json'}

    if is_server_running("http://127.0.0.1:8000/docs"):
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            print("Response:", response.json())
        else:
            print("Failed to get a response:", response.status_code)
    else:
        print("Server did not start in time")      

def calc_precision_clus_request():
    url = f"http://127.0.0.1:8000/calc_precision_cluster"   
    headers = {'accept': 'application/json'}
    # body={
    #     "query_id": query_id,
    #     "input_data": input_text
    # }
    print("URL:", url)
    if is_server_running("http://127.0.0.1:8000/docs"):
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            print("Response:", response.json())
        else:
            print("Failed to get a response:", response.status_code)
    else:
        print("Server did not start in time")         

def calc_recall_clus_request():
    url = f"http://127.0.0.1:8000/calc_recall"   
    headers = {'accept': 'application/json'}
    # body={
    #     "query_id": query_id,
    #     "input_data": input_text
    # }
    if is_server_running("http://127.0.0.1:8000/docs"):
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            print("Response:", response.json())
        else:
            print("Failed to get a response:", response.status_code)
    else:
        print("Server did not start in time")                   

def kMean_avg_request():
    url = f"http://127.0.0.1:8000/k-mean"
    headers = {"Content-Type": "application/json"}
    if is_server_running("http://127.0.0.1:8000/docs"):
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            print("Response:", response.json())
        else:
            print("Failed to get a response:", response.status_code)
    else:
        print("Server did not start in time")                


if __name__ == "__main__":
    server_process = multiprocessing.Process(target=run_server)
    server_process.start()
    calc_recall_request(dataset_number=1)
    server_process.terminate()
