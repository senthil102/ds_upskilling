import json
import os

from langchain_core.tools import tool


EMPLOYEE_FILE = os.path.join(
    os.path.dirname(__file__),
    "data",
    "employees.json"
)


@tool
def get_employee_details(
    authenticated_employee_id: str
) -> str:
    """Get HR information for the authenticated employee."""

    with open(EMPLOYEE_FILE, "r", encoding="utf-8") as file:
        employees = json.load(file)

    employee = employees.get(authenticated_employee_id)

    if employee is None:
        return "Employee information was not found."

    employee_details = {
        "employee_id": authenticated_employee_id,
        "name": employee["name"],
        "department": employee["department"],
        "email": employee["email"],
        "annual_leave_balance": employee.get(
            "annual_leave_balance", 0
        ),
        "sick_leave_balance": employee.get(
            "sick_leave_balance", 0
        )
    }

    return json.dumps(
        employee_details,
        indent=2
    )