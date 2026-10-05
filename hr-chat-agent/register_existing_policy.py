from pathlib import Path
import shutil

from database import get_connection


BASE_DIR = Path(__file__).resolve().parent

OLD_FILE = (
    BASE_DIR
    / "data"
    / "hr_policies"
    / "company-policy.pdf"
)

DOCUMENTS_DIR = (
    BASE_DIR
    / "data"
    / "hr_documents"
)

NEW_FILE = (
    DOCUMENTS_DIR
    / "company-policy.pdf"
)

if not OLD_FILE.exists():

    print(
        "ERROR: Existing company-policy.pdf "
        "was not found."
    )

    raise SystemExit

DOCUMENTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


if not NEW_FILE.exists():

    shutil.copy2(
        OLD_FILE,
        NEW_FILE
    )

    print(
        "company-policy.pdf copied "
        "to hr_documents."
    )

else:

    print(
        "company-policy.pdf already exists "
        "in hr_documents."
    )


connection = get_connection()

cursor = connection.cursor()


cursor.execute(
    """
    SELECT id
    FROM documents
    WHERE file_name = ?
    """,
    ("company-policy.pdf",)
)

existing = cursor.fetchone()


if existing:

    print(
        "Document is already registered "
        "in SQLite."
    )

else:

    cursor.execute(
        """
        INSERT INTO documents
        (
            file_name,
            file_path,
            uploaded_by,
            status
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            "company-policy.pdf",
            str(NEW_FILE),
            "SYSTEM",
            "ACTIVE"
        )
    )

    connection.commit()

    print(
        "company-policy.pdf registered "
        "in SQLite."
    )


connection.close()


print(
    "\nExisting policy registration completed."
)