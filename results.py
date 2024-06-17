import os
import pandas as pd
os.environ['QUOTIENT_API_KEY'] = "YOUR_KEY"

from quotientai.client import QuotientClient
from quotientai.utils import show_job_progress
import IPython
from IPython.display import display

client = QuotientClient()
jobs = client.list_jobs(filters={'id': 1504})
results = client.get_eval_results(jobs[0]['id'])

df_report = pd.json_normalize(results, "results")
df_report.columns = df_report.columns.str.replace("metric.", "")


metrics = ['completion_time_ms',
          'rougeL_precision', 'rougeL_recall', 'rougeL_fmeasure',
          'bert_score_precision', 'bert_score_recall', 'bert_score_f1']


display(df_report[metrics].describe())