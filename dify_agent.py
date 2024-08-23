from dify_llm import Dify


class Agent:
    def __init__(self, api_key):
        self.dify = Dify(api_key)
    def ask(self, query, inputs:dict={}):
        """
        返回的是完整文本
        """
        response = self.dify.get_response_message(query, conversation_id="", userid= "xxxtestxxx", inputs= inputs)
        # print("智能体回复：：：：",response.text)
        return self.dify.handle_sse_response(response)

   

if __name__ == '__main__':
    agent = Agent(api_key="app-Deq3fPPlVLHDTAAi4sXqx1Qg")
    response = agent.ask("你好", inputs={"brand":"长安","type":"欧诺"})
    print(response)
