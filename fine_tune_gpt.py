import json
from openai import OpenAI


OPEN_API_KEY='Your-key'
FILE_PATH = "/home/azureuser/quotient/dataset/fine_tune_llm_dataset.jsonl"
TEST_FILE = "/home/azureuser/quotient/dataset/test_dataset.jsonl"

client = OpenAI(api_key = OPEN_API_KEY)


#upload the data for the fine tuning model
def upload_response():
    upload_response = client.files.create(
    file=open(FILE_PATH, "rb"),
    purpose='fine-tune'
    )
    file_id = upload_response.id
    print(upload_response)
    return file_id

def fine_tune_model(file_id):
    response = client.fine_tuning.jobs.create(
    training_file = file_id,
     model="gpt-3.5-turbo")
    print(response)
    return response


file_id = upload_response()
fine_tune_model(file_id)

   
 


