from memory.failure_memory import get_failures


def show_failures():

    failures = get_failures()

    print(
        f"\nTotal Failures: "
        f"{len(failures)}"
    )

    for item in failures:

        print(
            f"- {item['tool']}: "
            f"{item['reason']}"
        )


if __name__ == "__main__":
    show_failures()