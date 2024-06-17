import os
import pandas as pd
os.environ['QUOTIENT_API_KEY'] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiIDogImh0dHBzOi8vaGhxcHBjcWx0a2x6ZnBnZ2RvY2Iuc3VwYWJhc2UuY28vYXV0aC92MSIsICJhcHBfbWV0YWRhdGEiIDogeyJwcm92aWRlcnMiOiBbImVtYWlsIl19LCAiYXVkIiA6ICJhdXRoZW50aWNhdGVkIiwgInJvbGUiIDogImF1dGhlbnRpY2F0ZWQiLCAidGlkIiA6ICJkOTkxZjY4OS1jNGY1LTQ5ZTgtOWYzYi01MGJlMjkyYzZlNGMiLCAic3ViIiA6ICIxMzNlOTEyMi1lN2M0LTRiNzgtOGFiNi00MmZiNDIzNTM3Y2QiLCAiaWF0IiA6IDE3MTc4OTE0NzguNzAzMzA3LCAiZXhwIiA6IDE3MjA0ODM0Nzl9.ZbbdXDAWtEsytFp2LdkIbqYetQxOVxPJ2S2qPccTAfc"

from quotientai.client import QuotientClient
from quotientai.utils import show_job_progress
import IPython
from IPython.display import display
client = QuotientClient()

def create_rubric_based_metric():
    rubric_template = "{input_text}: {(|a|+|b|)-Lev.dist(a,b) \over |a|+|b|}$$"
    custom_metric = client.create_rubric_based_metric(
        name= 'relevant_answer', description= "Refers to the degree to which a response directly addresses and is appropriate for a given question or context. This does not take the factuality of the answer into consideration but rather penalizes the presence of redundant information or incomplete answers given a question. It is calculated from question and answer",
        model_id = 77, rubric_template= rubric_template
    )
    return custom_metric


def get_all_metrics():
    metrics = client.list_metrics()
    print(metrics)

# custom_metric = create_rubric_based_metric()
# print(custom_metric)

get_all_metrics()
 