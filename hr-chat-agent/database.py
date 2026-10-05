import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(
    exist_ok=True
)

DB_PATH = DATA_DIR / "hr_agent.db"


def get_connection():

    return sqlite3.connect(
        DB_PATH
    )

def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (

            employee_id TEXT PRIMARY KEY,

            name TEXT NOT NULL,

            department TEXT NOT NULL,

            email TEXT NOT NULL UNIQUE,

            password TEXT NOT NULL,

            role TEXT NOT NULL DEFAULT 'EMPLOYEE',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leave_balances (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            employee_id TEXT NOT NULL,

            leave_type TEXT NOT NULL,

            balance INTEGER NOT NULL DEFAULT 0,

            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (employee_id)
                REFERENCES employees(employee_id),

            UNIQUE(employee_id, leave_type)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            file_name TEXT NOT NULL,

            file_path TEXT NOT NULL,

            uploaded_by TEXT NOT NULL,

            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            status TEXT NOT NULL DEFAULT 'ACTIVE'
        )
    """)

    connection.commit()

    connection.close()


if __name__ == "__main__":

    initialize_database()

    print(
        "SQLite database initialized successfully."
    )

    print(
        f"Database: {DB_PATH}"
    )