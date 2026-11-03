
import argparse
import os
import logging

from datetime import datetime, timezone

from integrity import (
    scan_directory,
    save_baseline,
    load_baseline,
    compare_files
)

from monitor import monitor_directory
from reporter import save_reports


os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/activity.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def create_baseline(directory):
    data = scan_directory(directory)

    save_baseline(data)

    logging.info(
        "Baseline created for %s with %d files",
        directory,
        len(data)
    )

    print(f"[+] Baseline created: {len(data)} files")


def check_integrity(directory):
    baseline = load_baseline()
    current = scan_directory(directory)

    changes = compare_files(baseline, current)

    report = {
        "directory": directory,
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
        "created": changes["created"],
        "modified": changes["modified"],
        "deleted": changes["deleted"]
    }

    for category in ("created", "modified", "deleted"):
        for filename in changes[category]:
            logging.warning(
                "%s: %s",
                category.upper(),
                filename
            )

    save_reports(report)

    print("\n=== INTEGRITY ASSESSMENT ===")
    print("Created:", len(changes["created"]))
    print("Modified:", len(changes["modified"]))
    print("Deleted:", len(changes["deleted"]))


def start_monitoring(directory):
    baseline = load_baseline()

    # Keep watching for changes.
    events = monitor_directory(directory, baseline)

    # Compare the final state to the original baseline.
    current = scan_directory(directory)
    changes = compare_files(baseline, current)

    report = {
        "directory": directory,
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
        "created": changes["created"],
        "modified": changes["modified"],
        "deleted": changes["deleted"],
        "monitoring_events": events
    }

    save_reports(report)

    print("\n[+] Final monitoring report saved")


def main():
    parser = argparse.ArgumentParser(
        description="Python File Integrity Monitoring Tool"
    )

    parser.add_argument(
        "action",
        choices=["init", "check", "monitor"]
    )

    parser.add_argument(
        "--directory",
        required=True,
        help="Directory to monitor"
    )

    args = parser.parse_args()

    try:
        if args.action == "init":
            create_baseline(args.directory)

        elif args.action == "check":
            check_integrity(args.directory)

        elif args.action == "monitor":
            start_monitoring(args.directory)

    except (OSError, ValueError, FileNotFoundError) as error:
        print("[ERROR]", error)


if __name__ == "__main__":
    main()
