from src.langgraphagenticai.state.state import State

class ChatbotWithToolNode:
    def __init__(self, model):
        self.llm = model
    def process(self, state: State) -> dict:
        """
        Processes the user input and generates a response using the LLM model with tools.
        
        Args:
            state (State): The current state of the chatbot, including conversation history and tool usage.
        
        Returns:
            dict: A dictionary containing the response from the LLM and any tool outputs.
        """
        user_input = state['messages'][-1] if state['messages'] else ""
        llm_response = self.llm.invoke([{"role":"user","content":user_input}])
        tools_response = f"Tpp; integration for:'{user_input}'"
        return {"messages": [llm_response,tools_response]}
    
    def create_chatbot(self,tools):
        """
        Return a chatbot node that can handle user queries and provide responses using the LLM model with tools.
        """
        llm_with_tools = self.llm.bind_tools(tools)
        
        def chatbot_node(state:State):
            return {"messages":[llm_with_tools.invoke(state['messages'])]}
        
        return chatbot_node