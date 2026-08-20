from reliability import (
    retry_call,
    validate_output,
    fallback_response,
    log
)


def main():

    task = "Explain photosynthesis to a 10-year-old."

    log("Agent started")

    # Try calling the AI
    result = retry_call(task)

    # Guardrail
    if result and validate_output(result):

        log("Response passed guardrail")

        print("\n========== FINAL ANSWER ==========")
        print(result)

    else:

        log("AI response failed")

        # Fallback
        result = fallback_response()

        print("\n========== FALLBACK ANSWER ==========")
        print(result)


if __name__ == "__main__":
    main()