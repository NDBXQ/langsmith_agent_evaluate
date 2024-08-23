QA_PROMPT_TEMPLATE = """
You are an expert professor specialized in grading students' answers to questions.
You are grading the following question:
{query}
Here is the real answer:
{answer}
You are grading the following predicted answer:
{result}
Respond with CORRECT or INCORRECT:
Grade:
"""


CRITERIA_PROMPT_TEMPLATE = """
You are an expert professor specialized in grading students' answers to questions.
You are grading the following question:
{query}
Here is the information involved in this question:
{information}
You are grading the following predicted answer:
{result}
Please use 1-10 to criteria, you can only reply to me with numbers, other words are not required.:
Criteria:
"""





"""
You are assessing a chat bot RESPONSE to a user's QUERY in comparison to a REFERENCE response. 
A score of 10 is best and means that the response fits the criteria,
whereas a score of 0 is worst and means that it did not fit the criteria.

Criteria:

1. The reply should address the user's issue.
2. When the answer can be found in the reference information, 
ensure the accuracy of the answer without distorting the meaning in the reference.
3. The reply should be friendly.

Use the examples below for reference.


"""



