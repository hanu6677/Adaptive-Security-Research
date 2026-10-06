import json
from pathlib import Path
from collections import Counter


class TimelineAnalyzer:

    def __init__(
        self,
        correlation_file="reports/correlation_report.json"
    ):
        self.correlation_file = Path(
            correlation_file
        )

    def load(self):

        if not self.correlation_file.exists():
            raise FileNotFoundError(
                f"Correlation report not found: "
                f"{self.correlation_file}"
            )

        return json.loads(
            self.correlation_file.read_text(
                encoding="utf-8"
            )
        )

    def extract_events(self, experiment):

        possible_keys = [
            "timeline",
            "events",
            "Timeline",
            "Events"
        ]

        for key in possible_keys:

            value = experiment.get(key)

            if isinstance(value, list):
                return value

        return []

    def normalize_event(self, event):

        if not isinstance(event, dict):
            return None

        event_type = (
            event.get("event_type")
            or event.get("event_type_name")
            or event.get("type")
            or event.get("category")
            or "UNKNOWN"
        )

        timestamp = (
            event.get("timestamp")
            or event.get("time")
            or event.get("TimeCreated")
            or ""
        )

        category = (
            event.get("category")
            or self.detect_category(
                str(event_type)
            )
        )

        return {
            "timestamp": str(timestamp),
            "event_type": str(event_type),
            "category": str(category).upper(),
            "source": str(
                event.get(
                    "source",
                    ""
                )
            )
        }

    @staticmethod
    def detect_category(event_type):

        value = event_type.upper()

        if "PROCESS" in value:
            return "PROCESS"

        if "FILE" in value:
            return "FILE"

        if "NETWORK" in value:
            return "NETWORK"

        if "DNS" in value:
            return "DNS"

        if "REGISTRY" in value:
            return "REGISTRY"

        return "OTHER"

    def analyze(self):

        data = self.load()

        experiments = data.get(
            "experiments",
            []
        )

        results = []

        for experiment in experiments:

            experiment_id = experiment.get(
                "experiment_id",
                "UNKNOWN"
            )

            raw_events = self.extract_events(
                experiment
            )

            events = []

            for raw_event in raw_events:

                normalized = self.normalize_event(
                    raw_event
                )

                if normalized:
                    events.append(
                        normalized
                    )

            counts = Counter(
                event["category"]
                for event in events
            )

            results.append({

                "experiment_id":
                    experiment_id,

                "event_count":
                    len(events),

                "category_counts": {
                    "PROCESS":
                        counts.get(
                            "PROCESS",
                            0
                        ),

                    "FILE":
                        counts.get(
                            "FILE",
                            0
                        ),

                    "NETWORK":
                        counts.get(
                            "NETWORK",
                            0
                        ),

                    "DNS":
                        counts.get(
                            "DNS",
                            0
                        ),

                    "REGISTRY":
                        counts.get(
                            "REGISTRY",
                            0
                        ),

                    "OTHER":
                        counts.get(
                            "OTHER",
                            0
                        )
                },

                "timeline": events
            })

        return results

    def save(
        self,
        results,
        output_file="reports/timeline_data.json"
    ):

        output_path = Path(
            output_file
        )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        output_path.write_text(
            json.dumps(
                {
                    "experiments": results
                },
                indent=4
            ),
            encoding="utf-8"
        )

        return output_path


if __name__ == "__main__":

    print()
    print("=" * 50)
    print(" TELEMETRY TIMELINE ANALYZER")
    print("=" * 50)

    try:

        analyzer = TimelineAnalyzer()

        results = analyzer.analyze()

        output = analyzer.save(
            results
        )

        print()
        print(
            f"Experiments analyzed: "
            f"{len(results)}"
        )

        print(
            f"[+] Timeline data saved:"
        )

        print(
            f"    {output}"
        )

    except Exception as error:

        print()
        print(
            f"[!] Error: {error}"
        )