from pathlib import Path
import json
from datetime import datetime


class TelemetryCollector:

    def __init__(self, output_dir="telemetry"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def record_event(self, experiment_id, event_type, details):
        event = {
            "timestamp": datetime.now().isoformat(),
            "experiment_id": experiment_id,
            "event_type": event_type,
            "details": details
        }

        output_file = self.output_dir / f"{experiment_id}.json"

        events = []

        if output_file.exists():
            try:
                events = json.loads(
                    output_file.read_text(encoding="utf-8")
                )
            except json.JSONDecodeError:
                events = []

        events.append(event)

        output_file.write_text(
            json.dumps(events, indent=4),
            encoding="utf-8"
        )

        return event


if __name__ == "__main__":

    collector = TelemetryCollector()

    experiment_id = "TEST-001"

    collector.record_event(
        experiment_id,
        "PROCESS_START",
        "Benign research sample started"
    )

    collector.record_event(
        experiment_id,
        "FILE_OPERATION",
        "Test file created and accessed"
    )

    collector.record_event(
        experiment_id,
        "PROCESS_END",
        "Benign research sample completed"
    )

    print("[+] Test telemetry recorded")
    print("[+] Check telemetry/TEST-001.json")