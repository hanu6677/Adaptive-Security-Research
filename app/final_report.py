import json
from pathlib import Path
from datetime import datetime


class FinalResearchReport:

    def __init__(
        self,
        correlation_file="reports/correlation_report.json",
        behavior_file="reports/behavior_profile.json",
        visibility_file="reports/visibility_metrics.json"
    ):
        self.correlation_file = Path(correlation_file)
        self.behavior_file = Path(behavior_file)
        self.visibility_file = Path(visibility_file)

    def load_json(self, path):

        if not path.exists():
            raise FileNotFoundError(
                f"File not found: {path}"
            )

        return json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

    def generate(self):

        correlation = self.load_json(
            self.correlation_file
        )

        behavior = self.load_json(
            self.behavior_file
        )

        visibility = self.load_json(
            self.visibility_file
        )

        correlation_experiments = {
            item.get("experiment_id"):
            item
            for item in correlation.get(
                "experiments",
                []
            )
        }

        behavior_experiments = {
            item.get("experiment_id"):
            item
            for item in behavior.get(
                "experiments",
                []
            )
        }

        visibility_experiments = {
            item.get("experiment_id"):
            item
            for item in visibility.get(
                "experiments",
                []
            )
        }

        experiment_ids = sorted(
            set(correlation_experiments)
            | set(behavior_experiments)
            | set(visibility_experiments)
        )

        experiments = []

        for experiment_id in experiment_ids:

            correlation_data = (
                correlation_experiments.get(
                    experiment_id,
                    {}
                )
            )

            behavior_data = (
                behavior_experiments.get(
                    experiment_id,
                    {}
                )
            )

            visibility_data = (
                visibility_experiments.get(
                    experiment_id,
                    {}
                )
            )

            experiments.append({

                "experiment_id":
                    experiment_id,

                "telemetry": {
                    "total_events":
                        correlation_data.get(
                            "Total Events",
                            0
                        ),

                    "internal_events":
                        correlation_data.get(
                            "Internal",
                            0
                        ),

                    "windows_events":
                        correlation_data.get(
                            "Windows",
                            0
                        ),

                    "sysmon_events":
                        correlation_data.get(
                            "Sysmon",
                            0
                        ),

                    "process_events":
                        correlation_data.get(
                            "Process",
                            0
                        ),

                    "file_events":
                        correlation_data.get(
                            "File",
                            0
                        ),

                    "network_events":
                        correlation_data.get(
                            "Network",
                            0
                        ),

                    "registry_events":
                        correlation_data.get(
                            "Registry",
                            0
                        ),

                    "dns_events":
                        correlation_data.get(
                            "DNS",
                            0
                        )
                },

                "expected_behavior":
                    behavior_data.get(
                        "expected_behavior",
                        {}
                    ),

                "observed_behavior":
                    behavior_data.get(
                        "observed_behavior",
                        {}
                    ),

                "observed_expected_categories":
                    behavior_data.get(
                        "observed_expected_categories",
                        []
                    ),

                "missing_expected_categories":
                    behavior_data.get(
                        "missing_expected_categories",
                        []
                    ),

                "expected_behavior_visibility":
                    behavior_data.get(
                        "expected_behavior_visibility",
                        0
                    ),

                "telemetry_category_coverage":
                    visibility_data.get(
                        "telemetry_category_coverage",
                        0
                    )
            })

        report = {

            "report_name":
                "Adaptive Security Research Report",

            "framework":
                "AI-Driven Adaptive "
                "Evasion Research Framework",

            "purpose":
                "Defensive analysis of telemetry "
                "visibility across controlled "
                "benign experiments.",

            "generated_at":
                datetime.now().isoformat(),

            "summary": {

                "total_experiments":
                    len(experiments),

                "average_behavior_visibility":
                    behavior.get(
                        "summary",
                        {}
                    ).get(
                        "average_visibility",
                        0
                    ),

                "fully_visible_experiments":
                    behavior.get(
                        "summary",
                        {}
                    ).get(
                        "fully_visible",
                        0
                    ),

                "partially_visible_experiments":
                    behavior.get(
                        "summary",
                        {}
                    ).get(
                        "partially_visible",
                        0
                    ),

                "missing_visibility_experiments":
                    behavior.get(
                        "summary",
                        {}
                    ).get(
                        "missing_visibility",
                        0
                    ),

                "average_telemetry_coverage":
                    visibility.get(
                        "summary",
                        {}
                    ).get(
                        "average_coverage",
                        0
                    ),

                "categories_observed":
                    visibility.get(
                        "summary",
                        {}
                    ).get(
                        "categories_observed",
                        []
                    )
            },

            "experiments": experiments
        }

        return report

    def save(
        self,
        report,
        output_file="reports/final_research_report.json"
    ):

        output_path = Path(output_file)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

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
    print("=" * 50)
    print(" FINAL SECURITY RESEARCH REPORT")
    print("=" * 50)

    try:

        generator = FinalResearchReport()

        report = generator.generate()

        output = generator.save(
            report
        )

        summary = report["summary"]

        print()

        print(
            f"Experiments              : "
            f"{summary['total_experiments']}"
        )

        print(
            f"Avg Behavior Visibility  : "
            f"{summary['average_behavior_visibility']}%"
        )

        print(
            f"Fully Visible            : "
            f"{summary['fully_visible_experiments']}"
        )

        print(
            f"Partially Visible        : "
            f"{summary['partially_visible_experiments']}"
        )

        print(
            f"Missing Visibility       : "
            f"{summary['missing_visibility_experiments']}"
        )

        print(
            f"Avg Telemetry Coverage   : "
            f"{summary['average_telemetry_coverage']}%"
        )

        print()

        print(
            "[+] Final report generated:"
        )

        print(
            f"    {output}"
        )

    except Exception as error:

        print()
        print(f"[!] Error: {error}")