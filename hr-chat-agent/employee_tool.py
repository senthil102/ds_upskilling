import json

from langchain_core.tools import tool

from database import get_connection


@tool
def get_employee_details(
    authenticated_employee_id: str
) -> str:
    """Get HR information for the authenticated employee."""

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            employee_id,
            name,
            department,
            email
        FROM employees
        WHERE employee_id = ?
        """,
        (authenticated_employee_id,)
    )

    employee = cursor.fetchone()

    if employee is None:

        connection.close()

        return "Employee information was not found."


   # Get Leave Balances
    cursor.execute(
        """
        SELECT
            leave_type,
            balance
        FROM leave_balances
        WHERE employee_id = ?
        """,
        (authenticated_employee_id,)
    )

    leave_balances = cursor.fetchall()

    connection.close()


    # Default Leave Balances
    annual_leave_balance = 0

    sick_leave_balance = 0


    # Read Leave Balances
    for leave_type, balance in leave_balances:

        if leave_type == "ANNUAL":

            annual_leave_balance = balance

        elif leave_type == "SICK":

            sick_leave_balance = balance


    # Employee Details
    employee_details = {

        "employee_id": employee[0],

        "name": employee[1],

        "department": employee[2],

        "email": employee[3],

        "annual_leave_balance": annual_leave_balance,

        "sick_leave_balance": sick_leave_balance
    }
    return json.dumps(
        employee_details,
        indent=2
    )