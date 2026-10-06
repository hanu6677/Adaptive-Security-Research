import json
from pathlib import Path
from datetime import datetime
class CorrelationEngine:
    def __init__(self):
        self.telemetry_dir = Path("telemetry")
        self.report_dir = Path("reports")
        self.report_dir.mkdir(
            parents=True,
            exist_ok=True
        )
    def load_events(self, file_path):
        file_path = Path(file_path)
        if not file_path.exists():
            return []
        try:
            data = json.loads(
                file_path.read_text(
                    encoding="utf-8"
                )
            )
            return data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError):
            return []
    def classify_event(self, event):
        event_type = str(
            event.get("event_type", "")
        ).upper()
        event_id = event.get("event_id")
        # Sysmon
        if event_id == 1:
            return "PROCESS"
        if event_id == 3:
            return "NETWORK"
        if event_id == 5:
            return "PROCESS"
        if event_id == 11:
            return "FILE"
        if event_id in (12, 13, 14):
            return "REGISTRY"
        if event_id == 22:
            return "DNS"
        # Internal telemetry
        if "PROCESS" in event_type:
            return "PROCESS"
        if "FILE" in event_type:
            return "FILE"
        if "NETWORK" in event_type:
            return "NETWORK"
        if "REGISTRY" in event_type:
            return "REGISTRY"
        if "DNS" in event_type:
            return "DNS"
        if "SYSTEM" in event_type:
            return "SYSTEM"
        if event_type == "WINDOWS_EVENT":
            return "SYSTEM"
        return "OTHER"
    def normalize_event(
        self,
        event,
        source
    ):
        timestamp = event.get(
            "timestamp"
        )
        normalized = {
            "source": source,
            "timestamp": timestamp,
            "category": self.classify_event(
                event
            ),
            "event_type": event.get(
                "event_type"
            ),
            "event_id": event.get(
                "event_id"
            ),
            "record_number": event.get(
                "record_number"
            ),
            "details": event.get(
                "details"
            ),
            "computer": event.get(
                "computer"
            )
        }
        return normalized
    def build_timeline(
        self,
        internal_events,
        windows_events,
        sysmon_events
    ):
        timeline = []
        for event in internal_events:
            timeline.append(
                self.normalize_event(
                    event,
                    "INTERNAL"
                )
            )
        for event in windows_events:
            timeline.append(
                self.normalize_event(
                    event,
                    "WINDOWS"
                )
            )
        for event in sysmon_events:
            timeline.append(
                self.normalize_event(
                    event,
                    "SYSMON"
                )
            )
        # Keep events with valid timestamps
        timeline = [
            event
            for event in timeline
            if event.get("timestamp")
        ]
        timeline.sort(
            key=lambda event:
            event["timestamp"]
        )
        return timeline
    def calculate_metrics(self, timeline):
        metrics = {
            "total_events": len(timeline),
            "internal_events": 0,
            "windows_events": 0,
            "sysmon_events": 0,
            "process_events": 0,
            "file_events": 0,
            "network_events": 0,
            "registry_events": 0,
            "dns_events": 0,
            "system_events": 0,
            "other_events": 0
        }
        for event in timeline:
            source = event.get(
                "source"
            )
            category = event.get(
                "category"
            )
            if source == "INTERNAL":
                metrics["internal_events"] += 1
            elif source == "WINDOWS":
                metrics["windows_events"] += 1
            elif source == "SYSMON":
                metrics["sysmon_events"] += 1
            if category == "PROCESS":
                metrics["process_events"] += 1
            elif category == "FILE":
                metrics["file_events"] += 1
            elif category == "NETWORK":
                metrics["network_events"] += 1
            elif category == "REGISTRY":
                metrics["registry_events"] += 1
            elif category == "DNS":
                metrics["dns_events"] += 1
            elif category == "SYSTEM":
                metrics["system_events"] += 1
            else:
                metrics["other_events"] += 1
        return metrics
    def correlate_experiment(
        self,
        experiment_id
    ):
        internal_file = (
            self.telemetry_dir
            / f"{experiment_id}.json"
        )
        windows_file = (
            self.telemetry_dir
            / f"{experiment_id}_windows.json"
        )
        sysmon_file = (
            self.telemetry_dir
           / f"{experiment_id}_sysmon.json"
        )
        internal_events = self.load_events(
            internal_file
        )
        windows_events = self.load_events(
            windows_file
        )
        sysmon_events = self.load_events(
            sysmon_file
        )
        timeline = self.build_timeline(
            internal_events,
            windows_events,
            sysmon_events
        )
        metrics = self.calculate_metrics(
            timeline
        )
        result = {
            "experiment_id": experiment_id,
            "generated_at": (
                datetime.now().isoformat()
            ),
            "telemetry_sources": {
                "internal": len(
                    internal_events
                ),
                "windows": len(
                    windows_events
                ),
                "sysmon": len(
                    sysmon_events
                )
            },
            "metrics": metrics,
            "timeline": timeline
        }
        output_file = (
            self.report_dir
            / f"{experiment_id}_correlation.json"
        )
        output_file.write_text(
            json.dumps(
                result,
                indent=4
            ),
            encoding="utf-8"
        )
        return result
    def find_experiments(self):
        experiment_ids = set()
        for file in self.telemetry_dir.glob(
            "MUT-*.json"
        ):
            name = file.name
            if name.endswith(
                "_windows.json"
            ):
                continue
            if name.endswith(
                "_sysmon.json"
            ):
                continue
            experiment_ids.add(
                file.stem
            )
        return sorted(
            experiment_ids
        )
    def correlate_all(self):
        experiment_ids = (
            self.find_experiments()
        )
        results = []
        for experiment_id in experiment_ids:
            print(
                f"[*] Correlating "
                f"{experiment_id}"
            )
            result = self.correlate_experiment(
                experiment_id
            )
            results.append(result)
        final_report = {
            "project": (
                "AI-Driven Adaptive "
                "Evasion Research Framework"
            ),
            "generated_at": (
                datetime.now().isoformat()
            ),
            "total_experiments": len(
                results
            ),
            "experiments": results
        }
        output_file = (
            self.report_dir
            / "correlation_report.json"
        )
        output_file.write_text(
            json.dumps(
                final_report,
                indent=4
            ),
            encoding="utf-8"
        )
        return final_report
if __name__ == "__main__":
    engine = CorrelationEngine()
    report = engine.correlate_all()
    print("\n================================")
    print(" TELEMETRY CORRELATION")
    print("================================")
    print(
        f"\nExperiments: "
        f"{report['total_experiments']}"
    )
    for experiment in report["experiments"]:
        metrics = experiment["metrics"]
        print(
            f"\n{experiment['experiment_id']}"
        )
        print(
            f"  Total Events : "
            f"{metrics['total_events']}"
        )
        print(
            f"  Internal     : "
            f"{metrics['internal_events']}"
        )
        print(
            f"  Windows      : "
            f"{metrics['windows_events']}"
        )
        print(
            f"  Sysmon       : "
            f"{metrics['sysmon_events']}"
        )
        print(
            f"  Process      : "
            f"{metrics['process_events']}"
        )
        print(
            f"  File         : "
            f"{metrics['file_events']}"
        )
        print(
            f"  Network      : "
            f"{metrics['network_events']}"
        )
        print(
            f"  Registry     : "
            f"{metrics['registry_events']}"
        )
        print(
            f"  DNS          : "
            f"{metrics['dns_events']}"
        )
    print(
        "\n[+] Report saved:"
    )
    print(
        "    reports/"
        "correlation_report.json"
    )