from evaluators import criteria_evaluator
from langsmith.evaluation import evaluate
import os
from dify_llm import Dify
from langsmith.run_helpers import traceable
from agent import Dify as agent_K


agent_k = agent_K()

dify = Dify()

os.environ['LANGCHAIN_TRACING_V2'] = 'true' # enables tracing 
os.environ['LANGCHAIN_API_KEY'] = "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"
os.environ['LANGCHAIN_PROJECT'] = 'Test'


@traceable(run_type="llm")
def call_dify(messages):
    response = agent_k.ask(messages)
    return response

def answer_dbrx_question_mistral(inputs: dict) -> dict:
    """
    Generates answers to user questions based on a provided website text using Ollama serving Mistral locally.

    Parameters:
    inputs (dict): A dictionary with a single key 'question', representing the user's question as a string.

    Returns:
    dict: A dictionary with a single key 'output', containing the generated answer as a string.
    """
    
    messages = inputs["question"]

    # Call Mistral
    response = call_dify(messages)

    # Response in output dict
    return {"answer": response} 



evaluate(
    answer_dbrx_question_mistral,
    data="况总",
    evaluators=[criteria_evaluator],
    experiment_prefix="criteria_evaluator",
)