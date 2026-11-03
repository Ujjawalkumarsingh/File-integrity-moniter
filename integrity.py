
import hashlib
import os
import json
from pathlib import Path


def calculate_hash(file_path):
    sha256 = hashlib.sha256()

    try:
        with open(file_path, "rb") as file:
            for chunk in iter(lambda: file.read(65536), b""):
                sha256.update(chunk)

        return sha256.hexdigest()

    except (OSError, PermissionError) as error:
        print(f"[ERROR] {file_path}: {error}")
        return None


def scan_directory(directory):
    directory = Path(directory).resolve()

    if not directory.is_dir():
        raise ValueError("Target must be an existing directory.")

    results = {}

    for root, dirs, files in os.walk(
        directory, followlinks=False
    ):
        # Do not follow symbolic links.
        dirs[:] = [
            d for d in dirs
            if not (Path(root) / d).is_symlink()
        ]

        for filename in files:
            file_path = Path(root) / filename

            if file_path.is_symlink():
                continue

            if not file_path.is_file():
                continue

            relative_path = str(
                file_path.relative_to(directory)
            )

            file_hash = calculate_hash(file_path)

            if file_hash:
                results[relative_path] = file_hash

    return results


def save_baseline(data, filename="baseline/baseline.json"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print("[+] Baseline saved successfully")


def load_baseline(filename="baseline/baseline.json"):
    if not os.path.exists(filename):
        raise FileNotFoundError("Baseline not found. Initialize first.")

    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def compare_files(old_data, new_data):
    old_files = set(old_data.keys())
    new_files = set(new_data.keys())

    created = new_files - old_files
    deleted = old_files - new_files

    modified = {
        path for path in old_files & new_files
        if old_data[path] != new_data[path]
    }

    return {
        "created": sorted(created),
        "deleted": sorted(deleted),
        "modified": sorted(modified)
    }
