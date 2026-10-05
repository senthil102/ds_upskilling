from database import get_connection

def authenticate_employee(
    employee_id: str,
    password: str
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            employee_id,
            name,
            department,
            email,
            password,
            role
        FROM employees
        WHERE employee_id = ?
        """,
        (employee_id,)
    )

    employee = cursor.fetchone()

    connection.close()


    if employee is None:
        return None


    if employee[4] != password:
        return None

    return {
        "employee_id": employee[0],
        "name": employee[1],
        "department": employee[2],
        "email": employee[3],
        "password": employee[4],
        "role": employee[5]
    }