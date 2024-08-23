# from evaluators import qa_evaluator,criteria_evaluator
# from langsmith.schemas import Example, Run
# from langsmith.evaluation import evaluate
# import os
# from dify_llm import Dify
# from langsmith.run_helpers import traceable
# import json

# dify = Dify()

# os.environ['LANGCHAIN_TRACING_V2'] = 'true' # enables tracing 
# os.environ['LANGCHAIN_API_KEY'] = "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"
# os.environ['LANGCHAIN_PROJECT'] = 'Test'


# @traceable(run_type="llm")
# def call_dify(messages):
#     response = dify.ask(messages)
#     return response

# def answer_dbrx_question_mistral(inputs: dict) -> dict:
#     """
#     Generates answers to user questions based on a provided website text using Ollama serving Mistral locally.

#     Parameters:
#     inputs (dict): A dictionary with a single key 'question', representing the user's question as a string.

#     Returns:
#     dict: A dictionary with a single key 'output', containing the generated answer as a string.
#     """

#     # System prompt 
#     # system_msg = f"Answer user questions about this context: \n\n\n {full_text}"
#     system_msg = f"Answer user questions about this context: Q:How many GPUs was DBRX trained on and what was the connectivity between GPUs? A:DBRX was trained on 3072 NVIDIA H100s connected by 3.2Tbps Infiniband"
    
#     # Pass in website text
#     messages = [{"role": "system", "content": system_msg},
#                 {"role": "user", "content": inputs["question"]}]
    
#     messages = json.dumps(messages)

#     # Call Mistral
#     response = call_dify(messages)

#     # Response in output dict
#     return {"answer": response} 

# evaluate(
#     answer_dbrx_question_mistral,
#     data="DBRX10",
#     evaluators=[criteria_evaluator],
#     experiment_prefix="criteria_evaluator",
# )

# -*- coding: utf-8 -*-
import requests
import json

class Dify:
    def __init__(self):
        # self.api_key = "app-crv56bm7UijiHKPVDTswSOOY"
        self.api_key = "app-KCl4UC5jdvEUc5Xkz923JEJk"
        self.url = 'http://14.29.175.216:8123/v1/chat-messages'

    def get_response_message(self, qurey:str, conversation_id="", userid= ""): 
        """
        conversation_id: 非必需参数
        """
        # print(f"query: {qurey}, conversation_id: {conversation_id}, role: {role}, userid: {userid}")
        userid = str(userid)
        response = requests.post(
            url = self.url,
            headers={'Authorization': f'Bearer {self.api_key}', 
                    'Content-Type': 'application/json'},
            json = {
            "inputs": {},
            "query": qurey,
            "response_mode": "streaming",
            "conversation_id": conversation_id,
            "user": userid,
            }
                    )
        return response


    
    
    # TODO: 异步返回events
    def parse_sse_event(self,event_str):
        """
        Parses a single SSE event string and returns a dictionary of its data.
        """
        event_prefix = "data: "
        if not event_str.startswith(event_prefix):
            return None
        trimmed_event_str = event_str[len(event_prefix):]

        # Check if trimmed_event_str is not empty and is a valid JSON string
        if trimmed_event_str:
            try:
                event = json.loads(trimmed_event_str)
                return event
            except json.JSONDecodeError:
                return None
        else:
            return None

    def append_agent_message(self,accumulated_agent_message,  merged_message):
        if accumulated_agent_message:
            merged_message.append({
                'type': 'agent_message',
                'content': accumulated_agent_message,
            })

    def handle_sse_response(self, response: requests.Response, role=""):
        events = []
        completion_tokens = ""
        prompt_tokens = ""
        total_tokens = ""
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                # print(decoded_line)
                event = self.parse_sse_event(decoded_line)
                if event:
                    events.append(event)

        accumulated_agent_message = ''
        conversation_id = None
        for event in events:
        
            if event.get("data"):
                data = event.get("data")
                if data.get("title"):
                    # print("角色测试：",data.get("title"))
                    if data.get("title")=="销售专家回复":
                        role = "zh-CN-XiaoxiaoNeural"
                    elif data.get("title")=="产品专家回复":
                        role = "zh-CN-YunjianNeural"
            if event.get("metadata"):
                metadata = event.get("metadata")
                if metadata.get("usage"):
                    usage = metadata.get("usage")
                    completion_tokens = usage.get("completion_tokens")
                    prompt_tokens = usage.get("prompt_tokens")
                    total_tokens = usage.get("total_tokens")
            if event.get("message_id"):
                message_id =event.get("message_id")
                

            event_name = event['event']
            if event_name == 'agent_message' or event_name == 'message':
                accumulated_agent_message += event['answer']
                # 保存conversation_id
                if not conversation_id:
                    conversation_id = event['conversation_id']

            elif event_name == 'error':
                raise Exception(event)
            
        if not conversation_id:
            raise Exception("conversation_id not found")
        return accumulated_agent_message, conversation_id, completion_tokens, prompt_tokens, total_tokens, message_id


if __name__ == '__main__':
    dify = Dify()
    response = dify.get_response_message("入驻有哪些优惠？",conversation_id="", userid ="xiaoxiaohong")
    message, conversation_id, role, completion_tokens, prompt_tokens, total_tokens, message_id = dify.handle_sse_response(response)
    print(f"message: {message}, conversation_id: {conversation_id},role:{role}")
