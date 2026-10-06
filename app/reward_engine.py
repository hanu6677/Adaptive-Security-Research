import json
from pathlib import Path


class ResearchAnalysisEngine:

    def analyze(self, telemetry_file):

        telemetry_file = Path(telemetry_file)

        if not telemetry_file.exists():
            raise FileNotFoundError(
                f"Telemetry file not found: {telemetry_file}"
            )

        events = json.loads(
            telemetry_file.read_text(encoding="utf-8")
        )

        process_events = 0
        file_events = 0
        network_events = 0

        for event in events:

            event_type = event.get(
                "event_type", ""
            ).upper()

            details = event.get(
                "details", ""
            ).lower()

            if "process" in event_type or "process" in details:
                process_events += 1

            if "file" in event_type or "file" in details:
                file_events += 1

            if "network" in event_type or "network" in details:
                network_events += 1

        result = {
            "total_events": len(events),
            "process_events": process_events,
            "file_events": file_events,
            "network_events": network_events
        }

        return result


if __name__ == "__main__":

    engine = ResearchAnalysisEngine()

    result = engine.analyze(
        "telemetry/TEST-001.json"
    )

    print("\n[+] Research Analysis")
    print("---------------------")
    print(f"Total Events    : {result['total_events']}")
    print(f"Process Events  : {result['process_events']}")
    print(f"File Events     : {result['file_events']}")
    print(f"Network Events  : {result['network_events']}")



