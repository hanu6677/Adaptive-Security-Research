import json
from pathlib import Path
from datetime import datetime
import win32evtlog
class WindowsTelemetryCollector:
    def __init__(self, output_dir="telemetry"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )
    def collect_system_events(
        self,
        experiment_id,
        count=50
    ):
        server = "localhost"
        log_name = "System"
        handle = win32evtlog.OpenEventLog(
            server,
            log_name
        )
        flags = (
            win32evtlog.EVENTLOG_BACKWARDS_READ
            | win32evtlog.EVENTLOG_SEQUENTIAL_READ
        )
        events = []
        try:
            while len(events) < count:
                records = win32evtlog.ReadEventLog(
                    handle,
                    flags,
                    0
                )
                if not records:
                    break
                for event in records:
                    event_time = event.TimeGenerated
                    events.append({
                        "experiment_id": experiment_id,
                        "timestamp": event_time.isoformat(),
                        "event_id": event.EventID & 0xFFFF,
                        "record_number": event.RecordNumber,
                        "source": event.SourceName,
                        "computer": event.ComputerName,
                        "event_type": "WINDOWS_SYSTEM_EVENT",
                        "category": self.classify_event(
                            event.EventID & 0xFFFF
                        )
                    })
                    if len(events) >= count:
                        break
        finally:
            win32evtlog.CloseEventLog(handle)
        output_file = (
            self.output_dir
            / f"{experiment_id}_windows.json"
        )
        output_file.write_text(
            json.dumps(
                events,
                indent=4
            ),
            encoding="utf-8"
        )
        return events
    @staticmethod
    def classify_event(event_id):
        # Generic Windows System log classification.
        categories = {
            6005: "SYSTEM_START",
            6006: "SYSTEM_SHUTDOWN",
            6008: "UNEXPECTED_SHUTDOWN",
            7036: "SERVICE_STATE_CHANGE",
            7040: "SERVICE_CONFIGURATION_CHANGE"
        }
        return categories.get(
            event_id,
            "SYSTEM"
        )