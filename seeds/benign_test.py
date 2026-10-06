from pathlib import Path
from datetime import datetime
import hashlib


TEST_DIR = Path("sandbox_test")
TEST_DIR.mkdir(exist_ok=True)

test_file = TEST_DIR / "activity.txt"

message = f"Security research test: {datetime.now().isoformat()}"

test_file.write_text(message, encoding="utf-8")

content = test_file.read_bytes()
file_hash = hashlib.sha256(content).hexdigest()

print("=== AI Security Research Test ===")
print(f"Test file: {test_file}")
print(f"SHA256: {file_hash}")
print("Status: SUCCESS")    