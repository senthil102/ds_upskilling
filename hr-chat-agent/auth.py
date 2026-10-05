import json
import os


EMPLOYEE_FILE = os.path.join(
    os.path.dirname(__file__),
    "data",
    "employees.json"
)


def authenticate_employee(
    employee_id: str,
    password: str
):

    with open(
        EMPLOYEE_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        employees = json.load(file)

    employee = employees.get(employee_id)

    if employee is None:
        return None

    if employee["password"] != password:
        return None

    return employee