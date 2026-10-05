from database import get_connection


connection = get_connection()

cursor = connection.cursor()

print("\n===== EMPLOYEES =====")

cursor.execute("""
    SELECT
        employee_id,
        name,
        department,
        email,
        role
    FROM employees
""")

employees = cursor.fetchall()

for employee in employees:

    print(employee)


print("\n===== LEAVE BALANCES =====")

cursor.execute("""
    SELECT
        employee_id,
        leave_type,
        balance
    FROM leave_balances
    ORDER BY employee_id, leave_type
""")

balances = cursor.fetchall()

for balance in balances:

    print(balance)

connection.close()