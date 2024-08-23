from langsmith.schemas import Run, Example
from prompt_template import *
from dify_llm import Dify
import json

llm = Dify(api_key="app-R7nufINYeQfQHzhcPTTjpeFv")

def evaluate_length(run: Run, example: Example) -> dict:
    prediction = run.outputs.get("output") or ""
    required = example.outputs.get("answer") or ""
    score = int(len(prediction) < 2 * len(required))
    return {"key":"length", "score": score}


def qa_evaluator(run: Run, example: Example) -> dict:
    query = run.inputs["inputs"]["question"]
    answer = example.outputs["answer"]
    result = run.outputs["answer"]
    
    system_template =QA_PROMPT_TEMPLATE.format(query=query, answer=answer, result=result)

    Grade =llm.ask(system_template)
    if Grade == "CORRECT":
        score = 1
    elif Grade == "INCORRECT":
        score = 0    
    return {"key": "qa_evaluator", "score": score}


def summary_eval(runs: list[Run], examples: list[Example]) -> dict:
    correct = 0
    for i, run in enumerate(runs):
        if run.outputs["output"] == examples[i].outputs["label"]:
            correct += 1
    if correct / len(runs) > 0.5:
        return {"key": "pass", "score": True}
    else:
        return {"key": "pass", "score": False}


def criteria_evaluator(run: Run, example: Example):
    """
    根据问题涉及到的信息进行的回答来进行评估
    """
    query = run.inputs["inputs"]["question"]
    information = example.outputs["answer"]
    result = run.outputs["answer"]
    system_template = CRITERIA_PROMPT_TEMPLATE.format(query=query, information=information, result=result)

    score =llm.ask(system_template)
    print("评估器打分：：：：", score)
    return {"key": "criteria_evaluator", "score": int(float(score))}


def qa_evaluator_v1(run: Run, example: Example) -> dict:
    print("==========",run.inputs)
    query = run.inputs["inputs"]["question"]
    print("==========",example.outputs)
    answer = example.outputs["answer"]
    print("==========",run.outputs)
    result = run.outputs["answer"]
    
    system_template = f"""You are an expert professor specialized in grading students' answers to questions.
You are grading the following question:
{query}
Here is the real answer:
{answer}
You are grading the following predicted answer:
{result}
Respond with CORRECT or INCORRECT:
Grade:
"""    
    message = {
        "role": "system",
        "content":  system_template
    }
    # 将字典转为字符串
    message = json.dumps(message)
    Grade =llm.ask(message)
    if Grade == "CORRECT":
        score = 1
    elif Grade == "INCORRECT":
        score = 0
    print("score===========>", score)
    
    return {"key": "qa_evaluator", "score": score}