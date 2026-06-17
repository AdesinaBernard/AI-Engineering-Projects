from coordinator import coordinate


TEST_CASES = [
    "Research NumPy and explain why it matters",
    "Analyze numpy/numpy",
    "What is RAG?",
    "Summarize artificial intelligence"
]


def run_tests():

    passed = 0

    for test in TEST_CASES:

        print("\n" + "=" * 50)
        print(f"TEST: {test}")

        try:

            result = coordinate(test)

            print("PASS")

            passed += 1

        except Exception as e:

            print(
                f"FAIL: {e}"
            )

    print(
        f"\nPassed "
        f"{passed}/{len(TEST_CASES)}"
    )


if __name__ == "__main__":
    run_tests()