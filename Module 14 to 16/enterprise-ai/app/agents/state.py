from typing import TypedDict


class AgentState(TypedDict):

    question: str
    context: str
    tool_result: str
    answer: str