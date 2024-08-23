# -*- coding: utf-8 -*-
import requests
import json

class Dify:
    def __init__(self, api_key="app-R7nufINYeQfQHzhcPTTjpeFv"):
        self.api_key = api_key
        self.url = 'http://14.29.175.216:8123/v1/chat-messages'

    def get_response_message(self, qurey:str, conversation_id="", userid= "", inputs:dict={}): 
        """
        conversation_id: 非必需参数
        """
        userid = str(userid)
        response = requests.post(
            url = self.url,
            headers={'Authorization': f'Bearer {self.api_key}', 
                    'Content-Type': 'application/json'},
            json = {
            "inputs": inputs,
            "query": qurey,
            "response_mode": "streaming",
            "conversation_id": conversation_id,
            "user": userid,
            }
                    )
        # print("response: ", response.text)
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
        return accumulated_agent_message
    
    def ask(self, query, inputs={})->str:
        """
        返回的是完整文本
        """
        response = self.get_response_message(query, conversation_id="", userid= "xxxtestxxx", inputs= inputs)
        return self.handle_sse_response(response)


if __name__ == '__main__':
    dify = Dify()
    response = dify.get_response_message("线不一样",conversation_id="", userid ="xiaoxiaohong", inputs={"brand":"长安","type":"欧诺"})
    message = dify.handle_sse_response(response)
    print(f"message: {message}")
