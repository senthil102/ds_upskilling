import os

from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

from langfuse import get_client
from langfuse.langchain import CallbackHandler

from employee_tool import get_employee_details
from leave_calculator import calculate_leave
from policy_tool import search_hr_policy
from semantic_cache import SemanticCache


load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0
)

cache = SemanticCache()

langfuse = get_client()


def run_hr_agent(
    question: str,
    employee_id: str,
    chat_history=None
) -> str:


    langfuse_handler = CallbackHandler()

    @tool
    def get_my_employee_details() -> str:
        """
        Get HR information for the currently
        authenticated employee.
        """

        return get_employee_details.invoke(
            {
                "authenticated_employee_id": employee_id
            }
        )

    tools = [
        get_my_employee_details,
        calculate_leave,
        search_hr_policy
    ]


    agent = create_agent(

        model=llm,

        tools=tools,

        system_prompt="""

You are an HR Assistant.

You help the currently authenticated employee
with HR-related questions.

Available tools:

1. get_my_employee_details
   - Gets information about the currently
     authenticated employee.

2. calculate_leave
   - Calculates leave eligibility.

3. search_hr_policy
   - Searches company HR policy documents.

Rules:

- Always use get_my_employee_details for
  employee-specific information.

- Never ask the employee to provide an
  employee ID.

- Use the authenticated employee ID provided
  by the application.

- Never retrieve another employee's information.

- Never expose passwords.

- Use search_hr_policy for company policy questions.

- Use calculate_leave for leave calculations.

- Do not invent company policies.

- Give simple and clear answers.

- Use conversation history to understand
  references such as "it", "them",
  "those days", and "my balance".

"""
    )

    messages = []

    if chat_history:
        messages.extend(chat_history)

    messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    result = agent.invoke(
        {
            "messages": messages
        },
        config={
            "callbacks": [
                langfuse_handler
            ]
        }
    )


    final_message = result["messages"][-1]

    content = final_message.content


    if isinstance(content, str):

        answer = content


    elif isinstance(content, list):

        answer = ""

        for item in content:

            if (
                isinstance(item, dict)
                and item.get("type") == "text"
            ):

                answer = item.get(
                    "text",
                    ""
                )

                break

        if not answer:
            answer = str(content)


    else:

        answer = str(content)


    cache.save_response(
        question,
        answer
    )


    langfuse.flush()


    return answer