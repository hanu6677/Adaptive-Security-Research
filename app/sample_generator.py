from pathlib import Path
import uuid


def generate_sample(output_dir: str = "samples"):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    sample_id = f"BENIGN-{uuid.uuid4().hex[:8].upper()}"
    sample_file = output_path / f"{sample_id}.py"

    code = f'''"""
Benign Adaptive Evasion Research Sample
Sample ID: {sample_id}
"""

from pathlib import Path


def run_test():
    test_file = Path("research_test_file.txt")

    print("Sample ID: {sample_id}")
    print("Starting benign telemetry test")

    test_file.write_text(
        "This is harmless research data.",
        encoding="utf-8"
    )

    content = test_file.read_text(encoding="utf-8")
    print(f"Read test data: {{content}}")

    test_file.unlink(missing_ok=True)

    print("Benign telemetry test completed")


if __name__ == "__main__":
    run_test()
'''

    sample_file.write_text(code, encoding="utf-8")

    return sample_file


if __name__ == "__main__":
    path = generate_sample()
    print(f"[+] Generated: {path}")