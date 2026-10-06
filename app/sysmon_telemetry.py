import json
import subprocess
from pathlib import Path

import win32evtlog


class SysmonTelemetryCollector:

    LOG_NAME = "Microsoft-Windows-Sysmon/Operational"

    EVENT_CATEGORIES = {
        1: "PROCESS_CREATE",
        2: "FILE_TIME_CHANGE",
        3: "NETWORK_CONNECTION",
        5: "PROCESS_TERMINATE",
        7: "IMAGE_LOAD",
        10: "PROCESS_ACCESS",
        11: "FILE_CREATE",
        12: "REGISTRY_CREATE_DELETE",
        13: "REGISTRY_VALUE_SET",
        14: "REGISTRY_RENAME",
        15: "FILE_STREAM_CREATED",
        22: "DNS_QUERY",
        23: "FILE_DELETE",
        25: "PROCESS_TAMPERING",
    }

    def __init__(self, output_dir="telemetry"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def is_available(self):
        try:
            handle = win32evtlog.OpenEventLog(
                "localhost",
                self.LOG_NAME
            )

            win32evtlog.CloseEventLog(handle)
            return True

        except Exception:
            return False

    def collect_events(
        self,
        experiment_id,
        count=100
    ):

        if not self.is_available():
            return {
                "available": False,
                "events": []
            }

        handle = win32evtlog.OpenEventLog(
            "localhost",
            self.LOG_NAME
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

                    event_id = (
                        event.EventID & 0xFFFF
                    )

                    data = self.extract_event_data(
                        event
                    )

                    normalized = {
                        "experiment_id": experiment_id,

                        "timestamp":
                            event.TimeGenerated.isoformat(),

                        "event_id": event_id,

                        "record_number":
                            event.RecordNumber,

                        "source":
                            event.SourceName,

                        "computer":
                            event.ComputerName,

                        "event_type":
                            self.EVENT_CATEGORIES.get(
                                event_id,
                                "OTHER"
                            ),

                        "category":
                            self.get_category(event_id),

                        "process": {
                            "pid": data.get("ProcessId"),
                            "parent_pid":
                                data.get("ParentProcessId"),
                            "image":
                                data.get("Image"),
                            "command_line":
                                data.get("CommandLine"),
                            "parent_image":
                                data.get("ParentImage"),
                            "user":
                                data.get("User")
                        },

                        "file": {
                            "target_filename":
                                data.get("TargetFilename"),
                            "creation_utc_time":
                                data.get("CreationUtcTime")
                        },

                        "network": {
                            "source_ip":
                                data.get("SourceIp"),
                            "source_port":
                                data.get("SourcePort"),
                            "destination_ip":
                                data.get("DestinationIp"),
                            "destination_port":
                                data.get("DestinationPort"),
                            "protocol":
                                data.get("Protocol")
                        },

                        "dns": {
                            "query_name":
                                data.get("QueryName"),
                            "query_status":
                                data.get("QueryStatus"),
                            "query_results":
                                data.get("QueryResults")
                        },

                        "registry": {
                            "target_object":
                                data.get("TargetObject"),
                            "details":
                                data.get("Details")
                        },

                        "raw_data": data
                    }
                    events.append(normalized)

                    if len(events) >= count:
                        break
        finally:
            win32evtlog.CloseEventLog(handle)
        output_file = (
            self.output_dir
            / f"{experiment_id}_sysmon.json"
        )
        output_file.write_text(
            json.dumps(
                events,
                indent=4,
                default=str
            ),
            encoding="utf-8"
        )
        return {
            "available": True,
            "events": events
        }
    def extract_event_data(self, event):
        data = {}
        try:
            inserts = event.StringInserts
            if inserts:
                data["StringInserts"] = list(inserts)
        except Exception:
            pass
        return self.extract_named_fields(
            event.RecordNumber
        )
    def extract_named_fields(
        self,
        record_number
    ):
        script = f"""
$event = Get-WinEvent `
    -LogName '{self.LOG_NAME}' `
    -MaxEvents 200 |
    Where-Object {{ $_.RecordId -eq {record_number} }} |
    Select-Object -First 1
if ($event) {{
    $xml = [xml]$event.ToXml()
    $result = @{{}}
    foreach ($node in $xml.Event.EventData.Data) {{
        if ($node.Name) {{
            $result[$node.Name] = [string]$node.'#text'
        }}
    }}
    $result | ConvertTo-Json -Compress
}}
"""
        try:
            result = subprocess.run(
                [
                    "powershell.exe",
                    "-NoProfile",
                    "-NonInteractive",
                    "-Command",
                    script
                ],
                capture_output=True,
                text=True,
                timeout=5
            )
            output = result.stdout.strip()
            if not output:
                return {}
            parsed = json.loads(output)
            return parsed if isinstance(
                parsed,
                dict
            ) else {}
        except Exception:
            return {}
    @staticmethod
    def get_category(event_id):
        if event_id in {
            1, 5, 8, 10, 25
        }:
            return "PROCESS"
        if event_id in {
            2, 11, 15, 23
        }:
            return "FILE"
        if event_id == 3:
            return "NETWORK"
        if event_id in {
            12, 13, 14
        }:
            return "REGISTRY"
        if event_id == 22:
            return "DNS"
        return "OTHER"
if __name__ == "__main__":
    collector = SysmonTelemetryCollector()
    print(
        f"Sysmon available: "
        f"{collector.is_available()}"
    )
    if collector.is_available():
        result = collector.collect_events(
            experiment_id="SYS-TEST-001",
            count=20
        )
        print(
            f"Events collected: "
            f"{len(result['events'])}"
        )
        print(
            "Saved: "
            "telemetry/SYS-TEST-001_sysmon.json"
        )
    else:
        print(
            "[!] Sysmon is not available."
        )