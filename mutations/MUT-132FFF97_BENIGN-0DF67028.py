"""
Mutation Experiment: MUT-132FFF97
Generated for defensive security research.
"""

"""
Benign Adaptive Evasion Research Sample
Sample ID: BENIGN-0DF67028
"""

from pathlib import Path


def run_test():
    research_file = Path("research_test_file.txt")

    print("Sample ID: BENIGN-0DF67028")
    print("Starting benign telemetry test")

    research_file.write_text(
        "This is harmless research data.",
        encoding="utf-8"
    )

    research_content = research_file.read_text(encoding="utf-8")
    print(f"Read test data: {research_content}")

    research_file.unlink(missing_ok=True)

    print("Benign telemetry test completed")


if __name__ == "__main__":
    run_test()
