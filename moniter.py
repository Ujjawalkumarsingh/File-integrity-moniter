
import time
from datetime import datetime, timezone

from integrity import scan_directory, compare_files


def monitor_directory(directory, baseline):
    print("\n[*] File monitoring started")
    print("[*] Press CTRL+C to stop")

    previous = baseline.copy()
    events = []

    try:
        while True:
            current = scan_directory(directory)

            changes = compare_files(previous, current)

            timestamp = datetime.now(
                timezone.utc
            ).isoformat()

            for category in ("created", "modified", "deleted"):
                for filename in changes[category]:

                    event = {
                        "timestamp": timestamp,
                        "event": category.upper(),
                        "file": filename
                    }

                    events.append(event)

                    print(
                        f"[ALERT] {category.upper()}: "
                        f"{filename}"
                    )

            previous = current

            time.sleep(5)

    except KeyboardInterrupt:
        print("\n[*] Monitoring stopped")

    return events
