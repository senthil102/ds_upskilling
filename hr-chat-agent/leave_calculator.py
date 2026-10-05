from langchain_core.tools import tool


@tool
def calculate_leave(
    available_days: int,
    requested_days: int
) -> str:
    """Calculate whether an employee has enough leave balance."""

    if requested_days <= 0:
        return "Requested leave days must be greater than 0."

    if requested_days <= available_days:

        remaining_days = available_days - requested_days

        return (
            f"Leave request is eligible. "
            f"You have {available_days} days available, "
            f"you requested {requested_days} days, "
            f"and {remaining_days} days will remain."
        )

    shortage = requested_days - available_days

    return (
        f"Leave request is not eligible. "
        f"You have only {available_days} days available, "
        f"but you requested {requested_days} days. "
        f"You are short by {shortage} days."
    )