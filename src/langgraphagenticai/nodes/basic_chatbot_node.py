

from src.langgraphagenticai.state.state import State

class BasicChatbotNode:
    """
    A node for a basic chatbot that can handle user queries and provide responses.
    This node is designed to be used in a LangGraph Agentic AI application.
    """

    def __init__(self,model):
        self.llm = model
    
    def process(self,state:State) -> dict:
        """
        Processes the user input and generates a response using the LLM model.
        
        Args:
            state (State): The current state of the chatbot, including conversation history.
        
        Returns:
            dict: A dictionary containing the response from the LLM.
        """
        return {"messages":self.llm.invoke(state["messages"])}