from langgraph.graph import StateGraph
from langgraph.graph import START,END
from src.langgraphagenticai.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraphagenticai.state.state import State
from src.langgraphagenticai.tools.search_tool import get_tools,create_tool_node
from langgraph.prebuilt import tools_condition,ToolNode
from src.langgraphagenticai.nodes.chatbot_with_tool_node import ChatbotWithToolNode
from src.langgraphagenticai.nodes.ai_news_node import AINewsNode

class GraphBuilder:
    def __init__(self,model):
        self.llm = model
        self.graph_builder = StateGraph(State)
    def basic_chatbot_build_graph(self):
        """
        Builds a basic chatbot graph with the given LLM model.
        """
        self.basic_chatbot_build_graph_node = BasicChatbotNode(self.llm)
        self.graph_builder.add_node("chatbot",self.basic_chatbot_build_graph_node.process)
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_edge("chatbot",END)

    def chatbot_with_internet_build_graph(self):
        """
        Placeholder for building a chatbot graph with internet capabilities.
        
        """
        ## defining the tool and tool node
        tools = get_tools()
        tool_node = create_tool_node(tools)

        ## define the LLM
        llm =self.llm

        ## define the chatbot node
        obj_chatbot_with_node = ChatbotWithToolNode(llm)
        chatbot_node = obj_chatbot_with_node.create_chatbot(tools)



        ## add nodes
        self.graph_builder.add_node("chatbot",chatbot_node)
        self.graph_builder.add_node("tools",tool_node)
        ## add edges
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_conditional_edges("chatbot",tools_condition)
        self.graph_builder.add_edge("tools","chatbot")
        # self.graph_builder.set_finish_point("chatbot")
        
    def ai_news_builder_graph(self):
        """
         for building a graph for AI news use case.
        """

        ai_news_node = AINewsNode(self.llm)
        ## Define the nodes for the AI news use case
        self.graph_builder.add_node('fetch_news',ai_news_node.fetch_news)
        self.graph_builder.add_node('summarize_news',ai_news_node.summarize_news)
        self.graph_builder.add_node('save_result',ai_news_node.save_result)
        ## Define the edges between the nodes
        self.graph_builder.set_entry_point('fetch_news')
        self.graph_builder.add_edge('fetch_news', 'summarize_news')
        self.graph_builder.add_edge('summarize_news', 'save_result')
        self.graph_builder.add_edge('save_result',END)

        
    
    def setup_graph(self, usecase: str):
        """
        Sets up the graph for the selected use case.
        """
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
        if usecase == "Chatbot with Internet":
            self.chatbot_with_internet_build_graph()
        if usecase == "AI News":
            self.ai_news_builder_graph()


        return self.graph_builder.compile()
        
        return self.graph_builder.build()
        