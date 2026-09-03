from pypdf import PdfReader


def load_pdf(path: str) -> str:

    reader = PdfReader(path)

    pages = []

    for page_number, page in enumerate(
        reader.pages,
        start=1
    ):

        text = page.extract_text()

        if text:
            pages.append(
                f"[Page {page_number}]\n{text}"
            )

    return "\n\n".join(pages)