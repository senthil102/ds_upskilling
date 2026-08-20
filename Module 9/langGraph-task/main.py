from typing import TypedDict, Annotated
import operator

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

llm = ChatOllama(
    model="llama3.1",
    temperature=0
)

@tool
def calculator(expression: str) -> str:
    """
    Calculate a mathematical expression.

    Example:
    25 * 10
    100 + 50
    """

    try:
        result = eval(
            expression,
            {"__builtins__": {}},
            {}
        )

        return str(result)

    except Exception as e:
        return f"Error: {str(e)}"


tools = [calculator]

llm_with_tools = llm.bind_tools(tools)


class AgentState(TypedDict):
    messages: Annotated[list, operator.add]


def call_llm(state: AgentState):

    print("\n--- LLM NODE ---")

    response = llm_with_tools.invoke(state["messages"])

    print("LLM response:")
    print(response)

    return {
        "messages": [response]
    }

tool_node = ToolNode(tools)

#Conditional edge
def should_continue(state: AgentState):

    last_message = state["messages"][-1]

    # Check whether LLM requested a tool
    if last_message.tool_calls:

        print("\nLLM requested a tool.")

        return "tools"

    print("\nNo tool requested. Agent finished.")

    return END


graph = StateGraph(AgentState)


# Add nodes
graph.add_node("llm", call_llm)
graph.add_node("tools", tool_node)


# Starting point
graph.set_entry_point("llm")


# Conditional edge
graph.add_conditional_edges(
    "llm",
    should_continue
)


# After tool execution → back to LLM
graph.add_edge(
    "tools",
    "llm"
)

app = graph.compile()

#Run Agent
result = app.invoke(
    {
        "messages": [
            HumanMessage(
                content="Calculate 125 * 8 + 50"
            )
        ]
    }
)

print(result["messages"][-1].content)