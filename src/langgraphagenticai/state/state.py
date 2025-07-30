from pydantic import BaseModel, Field
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from typing import Annotated

class State(TypedDict):
    """
    Represents the state of the agentic AI, including the conversation history and any additional data.
    """
    messages: Annotated[list,add_messages]