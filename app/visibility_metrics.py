import json
from pathlib import Path
from statistics import mean


class VisibilityMetricsEngine:

    MONITORED_CATEGORIES = [
        "PROCESS",
        "FILE",
        "NETWORK",
        "REGISTRY",
        "DNS"
    ]

    def __init__(
        self,
        correlation_file="reports/correlation_report.json"
    ):
        self.correlation_file = Path(correlation_file)

    def load_data(self):
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

    def calculate_experiment_metrics(self, experiment):
        process = experiment.get("Process", 0)
        file_events = experiment.get("File", 0)
        network = experiment.get("Network", 0)
        registry = experiment.get("Registry", 0)
        dns = experiment.get("DNS", 0)

        observed = {
            "PROCESS": process > 0,
            "FILE": file_events > 0,
            "NETWORK": network > 0,
            "REGISTRY": registry > 0,
            "DNS": dns > 0
        }

        observed_categories = [
            category
            for category, present in observed.items()
            if present
        ]

        coverage = (
            len(observed_categories)
            / len(self.MONITORED_CATEGORIES)
        ) * 100

        return {
            "experiment_id": experiment.get(
                "experiment_id",
                "UNKNOWN"
            ),

            "event_counts": {
                "process": process,
                "file": file_events,
                "network": network,
                "registry": registry,
                "dns": dns
            },

            "observed_categories":
                observed_categories,

            "observed_category_count":
                len(observed_categories),

            "monitored_category_count":
                len(self.MONITORED_CATEGORIES),

            "telemetry_category_coverage":
                round(coverage, 2)
        }

    def analyze(self):
        data = self.load_data()

        experiments = data.get(
            "experiments",
            []
        )

        results = []

        for experiment in experiments:
            result = self.calculate_experiment_metrics(
                experiment
            )

            results.append(result)

        return results

    def generate_summary(self, results):

        if not results:
            return {
                "experiments": 0,
                "average_coverage": 0,
                "max_coverage": 0,
                "min_coverage": 0,
                "categories_observed": []
            }

        coverages = [
            result["telemetry_category_coverage"]
            for result in results
        ]

        categories = set()

        for result in results:
            categories.update(
                result["observed_categories"]
            )

        return {
            "experiments": len(results),

            "average_coverage":
                round(mean(coverages), 2),

            "max_coverage":
                max(coverages),

            "min_coverage":
                min(coverages),

            "categories_observed":
                sorted(categories)
        }

    def save_report(
        self,
        results,
        summary,
        output_file="reports/visibility_metrics.json"
    ):

        output_path = Path(output_file)
        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        report = {
            "framework": (
                "AI-Driven Adaptive "
                "Evasion Research Framework"
            ),

            "purpose": (
                "Defensive telemetry visibility "
                "measurement"
            ),

            "summary": summary,

            "experiments": results
        }

        output_path.write_text(
            json.dumps(
                report,
                indent=4
            ),
            encoding="utf-8"
        )

        return output_path


if __name__ == "__main__":

    print()
    print("=" * 40)
    print(" TELEMETRY VISIBILITY METRICS")
    print("=" * 40)

    engine = VisibilityMetricsEngine()

    try:
        results = engine.analyze()

        summary = engine.generate_summary(
            results
        )

        output = engine.save_report(
            results,
            summary
        )

        print()
        print(
            f"Experiments        : "
            f"{summary['experiments']}"
        )

        print(
            f"Average Coverage   : "
            f"{summary['average_coverage']}%"
        )

        print(
            f"Minimum Coverage   : "
            f"{summary['min_coverage']}%"
        )

        print(
            f"Maximum Coverage   : "
            f"{summary['max_coverage']}%"
        )

        print(
            f"Categories Seen    : "
            f"{', '.join(summary['categories_observed'])}"
        )

        print()
        print(
            f"[+] Report saved: {output}"
        )

    except Exception as error:
        print()
        print(f"[!] Error: {error}")
        