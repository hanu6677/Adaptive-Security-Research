import json
from pathlib import Path


class TelemetryAnalyzer:

    def analyze(self, telemetry_file):

        telemetry_file = Path(telemetry_file)

        if not telemetry_file.exists():
            raise FileNotFoundError(
                f"Telemetry file not found: {telemetry_file}"
            )

        events = json.loads(
            telemetry_file.read_text(
                encoding="utf-8"
            )
        )

        result = {
            "total_events": len(events),
            "process_events": 0,
            "file_events": 0,
            "network_events": 0,
            "system_events": 0,
            "unknown_events": 0
        }

        for event in events:

            event_type = str(
                event.get("event_type", "")
            ).lower()

            source = str(
                event.get("source", "")
            ).lower()

            if "process" in event_type:
                result["process_events"] += 1

            elif "file" in event_type:
                result["file_events"] += 1

            elif "network" in event_type:
                result["network_events"] += 1

            elif (
                "system" in event_type
                or source
            ):
                result["system_events"] += 1

            else:
                result["unknown_events"] += 1

        return result


if __name__ == "__main__":

    analyzer = TelemetryAnalyzer()

    files = list(
        Path("telemetry").glob(
            "*_windows.json"
        )
    )

    if not files:
        print(
            "[!] No Windows telemetry files found."
        )
        raise SystemExit(1)

    result = analyzer.analyze(files[-1])

    print("\n==============================")
    print(" WINDOWS TELEMETRY ANALYSIS")
    print("==============================")

    print(
        f"Total Events   : "
        f"{result['total_events']}"
    )

    print(
        f"Process Events : "
        f"{result['process_events']}"
    )

    print(
        f"File Events    : "
        f"{result['file_events']}"
    )

    print(
        f"Network Events : "
        f"{result['network_events']}"
    )

    print(
        f"System Events  : "
        f"{result['system_events']}"
    )

    print(
        f"Unknown Events : "
        f"{result['unknown_events']}"
    )