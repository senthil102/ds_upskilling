import json

from database import get_connection

JSON_FILE = "data/employees.json"

with open(
    JSON_FILE,
    "r",
    encoding="utf-8"
) as file:

    employees = json.load(file)

connection = get_connection()

cursor = connection.cursor()

for employee_id, employee in employees.items():

    cursor.execute(
        """
        INSERT OR IGNORE INTO employees
        (
            employee_id,
            name,
            department,
            email,
            password,
            role
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            employee_id,
            employee["name"],
            employee["department"],
            employee["email"],
            employee["password"],
            "EMPLOYEE"
        )
    )


    cursor.execute(
        """
        INSERT OR IGNORE INTO leave_balances
        (
            employee_id,
            leave_type,
            balance
        )
        VALUES (?, ?, ?)
        """,
        (
            employee_id,
            "ANNUAL",
            employee["annual_leave_balance"]
        )
    )

    cursor.execute(
        """
        INSERT OR IGNORE INTO leave_balances
        (
            employee_id,
            leave_type,
            balance
        )
        VALUES (?, ?, ?)
        """,
        (
            employee_id,
            "SICK",
            employee["sick_leave_balance"]
        )
    )

connection.commit()

connection.close()


print("Employee migration completed successfully.")