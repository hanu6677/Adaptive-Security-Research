from pathlib import Path
import hashlib

from app.config import SEEDS_DIR


def calculate_sha256(file_path: Path) -> str:
    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:
        while chunk := file.read(8192):
            sha256.update(chunk)

    return sha256.hexdigest()


def main():
    seed = SEEDS_DIR / "benign_test.py"

    if not seed.exists():
        print(f"[ERROR] Seed not found: {seed}")
        return

    file_hash = calculate_sha256(seed)

    print("=" * 50)
    print(" AI ADAPTIVE SECURITY RESEARCH")
    print("=" * 50)
    print(f"Seed:   {seed.name}")
    print(f"SHA256: {file_hash}")
    print("Status: READY")
if __name__ == "__main__":
    main()




