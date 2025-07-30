from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode

def get_tools():
    tools = [TavilySearchResults(max_results = 2)]
    return tools

def create_tool_node(tools):
    """
    Creates a ToolNode with the provided tools.
    
    Args:
        tools (list): List of tools to be included in the ToolNode.
        
    Returns:
        ToolNode: A ToolNode instance containing the specified tools.
    """
    return ToolNode(tools=tools)