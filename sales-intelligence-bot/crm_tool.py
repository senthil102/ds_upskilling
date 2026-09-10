import json
import os

CRM_FILE = os.path.join(
    os.path.dirname(__file__),
    "data",
    "crm_data.json"
)

def get_crm_account(company_name: str) -> str:
    
    with open(
        CRM_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        crm_data = json.load(file)

    account = crm_data.get(company_name)

   # First Check Case-insensitive match
    if account is None:

        for name, data in crm_data.items():
            if name.lower() == company_name.lower():
                account = data
                break

    # Account not found
    if account is None:
        return (
            f"No CRM information found for "
            f"{company_name}."
        )

    return json.dumps(
        account,
        indent=2
    )


