import streamlit as st

from src.langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraphagenticai.LLMS.groqllm import GroqLLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.ui.streamlitui.display_result import DisplayResultStreamlit

def load_langgraph_agentic_ai_app():
    """
    Load the LangGraph Agentic AI application with Streamlit UI.
    """
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    if not user_input:
        st.error("Error: Failed to load user input from the UI")
        return
    user_message = st.chat_input("Enter your message here...")

    if user_message:
        try:
            obj_llm_config = GroqLLM(user_controls_input=user_input)
            model = obj_llm_config.get_llm_model()
            if model is None:
                st.error("Error: LLM model could not be initialized. Please check your API key and model selection.")
                return
            usecase = user_input.get("selected_usecase")
            if not usecase:
                st.error("Error: No use case selected. Please select a use case to proceed.")
                return

            graph_builder = GraphBuilder(model)
            try:
                graph = graph_builder.setup_graph(usecase)
                DisplayResultStreamlit(usecase, graph, user_message).display_result_on_ui()
            except Exception as e:
                st.error(f"Error setting up graph: {e}")
                return

        except Exception as e:
            st.error(f"Error processing your message: {e}")
