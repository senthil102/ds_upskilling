from pathlib import Path
import shutil

from database import get_connection


BASE_DIR = Path(__file__).resolve().parent

DOCUMENTS_DIR = BASE_DIR / "data" / "hr_documents"

DOCUMENTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def save_document_metadata(
    file_name: str,
    file_path: str,
    uploaded_by: str
):
    connection = get_connection()
    cursor = connection.cursor()

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
            file_name,
            file_path,
            uploaded_by,
            "ACTIVE"
        )
    )

    connection.commit()
    connection.close()



def get_documents():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            file_name,
            uploaded_by,
            uploaded_at,
            status
        FROM documents
        ORDER BY uploaded_at DESC
        """
    )

    documents = cursor.fetchall()

    connection.close()

    return documents

def delete_document(document_id: int):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT file_path
        FROM documents
        WHERE id = ?
        """,
        (document_id,)
    )

    document = cursor.fetchone()

    if document is None:
        connection.close()
        return False


    file_path = Path(document[0])


    # Delete physical file
    if file_path.exists():
        file_path.unlink()


    # Delete database record
    cursor.execute(
        """
        DELETE FROM documents
        WHERE id = ?
        """,
        (document_id,)
    )

    connection.commit()
    connection.close()

    return True