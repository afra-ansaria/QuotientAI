import os
import pandas as pd

from quotientai.client import QuotientClient
from quotientai.utils import show_job_progress
import IPython
from IPython.display import display
from quotientai.utils import show_job_progress
import matplotlib


client = QuotientClient()

datasets = client.list_datasets()
print(datasets)
JOB_ID = '1538'
PROMPT_TEMPLATE_ID = 453
SYSTEM_PROMPT_ID = 408

PROMPT_3 = """
            Solve a question answering task with interleaving Thought, Action, Observation steps. Thought can reason about the current situation, and Action can be three types:
                (1) Search[entity], which searches the exact entity on Wikipedia and returns the first paragraph if it exists. If not, it will return some similar entities to search.
                (2) Lookup[keyword], which returns the next sentence containing keyword in the current passage.
                (3) Finish[answer], which returns the answer and finishes the task.
                At the end mention the final Answer
                You may take as many steps as necessary.
        Here is an example: 
        Question: Kam Heskin plays Paige Morgan in a 2004 film directed by who?
        Thought 1: I need to search Kam Heskin and Paige Morgan, find the 2004 film they are in, then find the director of the film.
        Action 1: Search[Kam Heskin]
        Observation 1: Kam Erika Heskin (born May 8, 1973) is an American actress. She began her career playing Caitlin Deschanel on the NBC daytime soap opera Sunset Beach (1998–1999), before appearing in films Planet of the Apes (2001) and Catch Me If You Can (2002). Heskin went on in 2003 to play Elizabeth Bennet in an independent film Pride & Prejudice: A Latter-Day Comedy, Robin in Charmed (2004), and Paige Morgan in The Prince and Me film franchise (2006–2010).
        Thought 2: Kam Heskin plays Paige Morgan in The Prince and Me film franchise. I need to search The Prince and Me film franchise and find the director of the 2004 film.
        Action 2: Search[The Prince and Me film franchise]
        Observation 2: Could not find [The Prince and Me film franchise]. Similar: ['Kam Heskin', 'Prince of Persia', 'Harry Potter and the Half-Blood Prince (film)', 'Prince of Persia: The Sands of Time (film)', 'The Chronicles of Narnia (film series)', 'Majestic Prince (franchise)', 'Kingsman (franchise)', 'The Little Prince (2015 film)', 'Shrek (franchise)', 'Harry Potter (film series)']
        Thought 3: I need to search The Prince and Me (2004 film) instead.
        Action 3: Search[The Prince and Me (2004 film)]
        Observation 3: Could not find [The Prince and Me (2004 film)]. Similar: ['The Prince & Me', 'The Prince & Me 2: The Royal Wedding', 'Kam Heskin', 'Prince of Darkness (film)', 'Prince of Persia: The Sands of Time (film)', 'Rob Knox', 'Alexander (2004 film)', 'Prince of Persia', 'Brooklynn Prince', 'Prince (musician)']
        Thought 4: I need to search The Prince & Me (2004 film).
        Action 4: Search[The Prince & Me (2004 film)]
        Observation 4: Could not find [The Prince & Me (2004 film)]. Similar: ['The Prince & Me', 'The Prince & Me 2: The Royal Wedding', 'Prince of Darkness (film)', 'Prince of Persia: The Sands of Time (film)', 'Rob Knox', 'Alexander (2004 film)', 'Prince (musician)', 'Prince of Persia', 'Kam Heskin', 'Brooklynn Prince']
        Thought 5: I need to search The Prince & Me (2004 film) instead.
        Action 5: Search[The Prince & Me (2004 film)]
        Observation 5: Could not find [The Prince & Me (2004 film)]. Similar: ['The Prince & Me', 'The Prince & Me 2: The Royal Wedding', 'Prince of Darkness (film)', 'Prince of Persia: The Sands of Time (film)', 'Rob Knox', 'Alexander (2004 film)', 'Prince (musician)', 'Prince of Persia', 'Kam Heskin', 'Brooklynn Prince']
        Thought 6: I need to search The Prince & Me (2004 film).
        Action 6: Search[The Prince & Me (2004 film)]
        Observation 6: Could not find [The Prince & Me (2004 film)]. Similar: ['The Prince & Me', 'The Prince & Me 2: The Royal Wedding', 'Prince of Darkness (film)', 'Prince of Persia: The Sands of Time (film)', 'Rob Knox', 'Alexander (2004 film)', 'Prince (musician)', 'Prince of Persia', 'Kam Heskin', 'Brooklynn Prince']
        Reflection: I got stuck in a loop where I kept trying to search 'The Prince & Me (2004 film)' but the page could not be found. Instead I should have tried to search the similar results that had a similar name to see and they were made in 2004.
        Questions: {input_text}. Answer:"""

PROMPT_4 = """
Please answer the following question using Google Search for the input key. 
<API>GoogleSearch(Question)</API>
Make sure the answer is factually correct. 
Try to keep the answer short and simple
Question: {input_text},
Answer
"""


# MODEL_ID=78
# RECIPE_NAME = 'llama-3-8b-chat-hf'
# RECIPE_DESCRIPTION ='LLama 3-8b'

MODEL_ID=80
RECIPE_NAME = 'databricks/dbrx-instruct'
RECIPE_DESCRIPTION ='DB'
DATASET_FILENAME= '/home/azureuser/quotient/dataset_case3.csv'
RECIPE_ID = 546
TASK_ID = 221

def create_dataset():
    dataset = client.create_dataset(
        file_path=DATASET_FILENAME, 
        name='dataset_3',
    )
    dataset = datasets[-1]
    print(dataset)
    dataset_ID = datasets[-1]['id']
    return dataset_ID

# dataset_ID = create_dataset()


def create_prompt_template():
    prompt_template = client.create_prompt_template(

    name = "Prompt4",
    template = PROMPT_4 )
    

    print(prompt_template)



create_prompt_template()

models = client.list_models()
def create_system_prompt():
    system_prompt = client.create_system_prompt(
        message_string='SYSTEM PROMPT TEXT.', 
        name='SYSTEM_PROMPT_NAME',
    )
    print(system_prompt)

def create_recipe():
    recipe = client.create_recipe(
        prompt_template_id=PROMPT_TEMPLATE_ID,
        system_prompt_id=SYSTEM_PROMPT_ID, 
        model_id=MODEL_ID, 
        name=RECIPE_NAME, 
        description='Prompt 1 with Model ID 10',
    )
    print(recipe)
    recipes = client.list_recipes()
    print(recipes)



def create_task():
    task = client.create_task(
        dataset_id=226, 
        name='case3_task', 
        task_type='question_answering',
    )
    print(task)        

# create_task()



#CREATE JOB
def create_job():
    job = client.create_job(task_id=TASK_ID, recipe_id=RECIPE_ID)
    print(job)
    jobs = client.list_jobs()
    job = client.list_jobs(filters={'id': JOB_ID})
    show_job_progress(client, JOB_ID)

# #VIEW RESULTS
results = client.get_eval_results(JOB_ID)
print(results)


### Iterate
df_report = pd.json_normalize(results, "results")

df_report.columns = df_report.columns.str.replace("metric.", "")

metrics = ['f1_score', 'bert_score_precision', 'completion_verbosity', 'selfcheckgpt_nli', 'rouge1_precision', 'rouge1_recall']
df_report.to_csv('results/out_prompt4.csv', index = False)

display(df_report[metrics].describe())

#BEST AND WORST F1 SCORES
df_report = df_report.sort_values('f1_score', ascending=False)


with pd.option_context('display.max_colwidth', 0):


 print("Best BERTscore performers:")
 display(df_report[['content.answer', 'content.completion', 'bert_score_f1', 'selfcheckgpt_nli', 'rougeL_fmeasure']].head(2))


 print("\n")
 print("Worst BERTscore performers:")
 display(df_report[['content.answer', 'content.completion', 'bert_score_f1', 'selfcheckgpt_nli', 'rougeL_fmeasure']].tail(2))


def compare_two_models():
    results_77 = client.get_eval_results('1537')
    results_80 = client.get_eval_results('1538')
    df_report_77 = pd.json_normalize(results_77, "results")
    df_report_80 = pd.json_normalize(results_80, "results")


    starter_mean = df_report_77.describe().loc['mean']
    starter_mean.name = "Llama recipe: zero-shot"


    second_model_mean = df_report_80.describe().loc['mean']
    second_model_mean.name = "Databricks recipe: zero-shot"


    llama_experiments = pd.concat([starter_mean, second_model_mean], axis=1)


    llama_experiments.drop(['completion_time_ms']).plot(kind='bar',
                                                                  figsize=(10,4),
                                                                  xlabel="Metric",
                                                                  ylabel='Score',
                                                                  title="Comparison of Llama vs. Databricks");
    display(llama_experiments.loc[['completion_time_ms']])

compare_two_models()
