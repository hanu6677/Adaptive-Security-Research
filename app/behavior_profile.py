import json
from pathlib import Path


class BehaviorProfileEngine:

    def __init__(
        self,
        correlation_file="reports/correlation_report.json"
    ):
        self.correlation_file = Path(correlation_file)

    def load_correlation(self):
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

    def get_expected_behavior(self):
        """
        Expected behavior of our current benign sample.

        The sample creates, reads and deletes a test file
        and runs as a normal process.
        """

        return {
            "PROCESS": True,
            "FILE": True,
            "NETWORK": False,
            "DNS": False,
            "REGISTRY": False
        }

    def get_observed_behavior(self, experiment):
        return {
            "PROCESS": experiment.get("Process", 0) > 0,
            "FILE": experiment.get("File", 0) > 0,
            "NETWORK": experiment.get("Network", 0) > 0,
            "DNS": experiment.get("DNS", 0) > 0,
            "REGISTRY": experiment.get("Registry", 0) > 0
        }

    def analyze_experiment(self, experiment):

        expected = self.get_expected_behavior()
        observed = self.get_observed_behavior(
            experiment
        )

        expected_categories = [
            category
            for category, required in expected.items()
            if required
        ]

        observed_expected = [
            category
            for category in expected_categories
            if observed.get(category, False)
        ]

        missing_expected = [
            category
            for category in expected_categories
            if not observed.get(category, False)
        ]

        if expected_categories:
            visibility = (
                len(observed_expected)
                / len(expected_categories)
            ) * 100
        else:
            visibility = 100

        return {
            "experiment_id": experiment.get(
                "experiment_id",
                "UNKNOWN"
            ),

            "expected_behavior": expected,

            "observed_behavior": observed,

            "expected_categories":
                expected_categories,

            "observed_expected_categories":
                observed_expected,

            "missing_expected_categories":
                missing_expected,

            "expected_behavior_visibility":
                round(visibility, 2)
        }

    def analyze(self):

        data = self.load_correlation()

        experiments = data.get(
            "experiments",
            []
        )

        results = []

        for experiment in experiments:
            results.append(
                self.analyze_experiment(
                    experiment
                )
            )

        return results

    def generate_summary(self, results):

        if not results:
            return {
                "experiments": 0,
                "average_visibility": 0,
                "fully_visible": 0,
                "partially_visible": 0,
                "missing_visibility": 0
            }

        visibility_values = [
            item["expected_behavior_visibility"]
            for item in results
        ]

        fully_visible = sum(
            value == 100
            for value in visibility_values
        )

        partially_visible = sum(
            0 < value < 100
            for value in visibility_values
        )

        missing_visibility = sum(
            value == 0
            for value in visibility_values
        )

        return {
            "experiments": len(results),

            "average_visibility": round(
                sum(visibility_values)
                / len(visibility_values),
                2
            ),

            "fully_visible": fully_visible,

            "partially_visible":
                partially_visible,

            "missing_visibility":
                missing_visibility
        }

    def save_report(
        self,
        results,
        summary,
        output_file="reports/behavior_profile.json"
    ):

        output_path = Path(output_file)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        report = {
            "framework":
                "AI-Driven Adaptive "
                "Evasion Research Framework",

            "purpose":
                "Expected versus observed "
                "behavior visibility analysis",

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
    print("=" * 45)
    print(" BEHAVIOR PROFILE ANALYSIS")
    print("=" * 45)

    engine = BehaviorProfileEngine()

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
            f"Experiments              : "
            f"{summary['experiments']}"
        )

        print(
            f"Average Visibility       : "
            f"{summary['average_visibility']}%"
        )

        print(
            f"Fully Visible            : "
            f"{summary['fully_visible']}"
        )

        print(
            f"Partially Visible        : "
            f"{summary['partially_visible']}"
        )

        print(
            f"Missing Visibility       : "
            f"{summary['missing_visibility']}"
        )

        print()
        print(
            f"[+] Report saved: {output}"
        )

    except Exception as error:

        print()
        print(f"[!] Error: {error}")