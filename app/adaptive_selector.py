import json
from pathlib import Path


class AdaptiveExperimentSelector:

    def __init__(
        self,
        report_file="reports/final_research_report.json"
    ):
        self.report_file = Path(report_file)

    def load_report(self):

        if not self.report_file.exists():
            raise FileNotFoundError(
                f"Report not found: {self.report_file}"
            )

        return json.loads(
            self.report_file.read_text(
                encoding="utf-8"
            )
        )

    def select_next_experiment(self):

        report = self.load_report()

        experiments = report.get(
            "experiments",
            []
        )

        if not experiments:
            return {
                "strategy": "BASELINE",
                "reason": "No previous experiments found."
            }

        latest = experiments[-1]

        visibility = latest.get(
            "expected_behavior_visibility",
            0
        )

        missing = latest.get(
            "missing_expected_categories",
            []
        )

        # Safe research decision logic
        if "FILE" in missing:
            strategy = "FILE_STRUCTURE_VARIATION"

        elif "PROCESS" in missing:
            strategy = "PROCESS_STRUCTURE_VARIATION"

        elif visibility < 100:
            strategy = "CONTROLLED_SOURCE_VARIATION"

        else:
            strategy = "BASELINE_REPETITION"

        return {
            "previous_experiment":
                latest.get(
                    "experiment_id",
                    "UNKNOWN"
                ),

            "previous_visibility":
                visibility,

            "missing_categories":
                missing,

            "selected_strategy":
                strategy,

            "purpose":
                "Select the next safe benign "
                "telemetry experiment."
        }

    def save_decision(
        self,
        decision,
        output_file="reports/adaptive_decision.json"
    ):

        output_path = Path(output_file)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        output_path.write_text(
            json.dumps(
                decision,
                indent=4
            ),
            encoding="utf-8"
        )

        return output_path


if __name__ == "__main__":

    print()
    print("=" * 50)
    print(" ADAPTIVE EXPERIMENT SELECTOR")
    print("=" * 50)

    try:

        selector = AdaptiveExperimentSelector()

        decision = (
            selector.select_next_experiment()
        )

        output = selector.save_decision(
            decision
        )

        print()

        print(
            f"Previous Experiment : "
            f"{decision.get('previous_experiment')}"
        )

        print(
            f"Previous Visibility : "
            f"{decision.get('previous_visibility')}%"
        )

        print(
            f"Missing Categories  : "
            f"{', '.join(decision.get('missing_categories', [])) or 'None'}"
        )

        print(
            f"Next Strategy       : "
            f"{decision.get('selected_strategy')}"
        )

        print()

        print(
            f"[+] Decision saved: {output}"
        )

    except Exception as error:

        print()
        print(f"[!] Error: {error}")