from pathlib import Path
import json

from app.adaptive_selector import AdaptiveExperimentSelector
from app.mutation_engine import BenignMutationEngine


class AdaptiveResearchLoop:

    def __init__(self):

        self.source_dir = Path("samples")

        self.selector = (
            AdaptiveExperimentSelector()
        )

        self.mutation_engine = (
            BenignMutationEngine()
        )

    def find_source_sample(self):

        samples = list(
            self.source_dir.glob("*.py")
        )

        samples = [
            sample
            for sample in samples
            if sample.name != "__init__.py"
        ]

        if not samples:
            raise FileNotFoundError(
                "No benign sample found in samples/"
            )

        return samples[0]

    def select_strategy(self):

        decision = (
            self.selector
            .select_next_experiment()
        )

        return decision

    def create_experiment(self):

        decision = self.select_strategy()

        strategy = decision.get(
            "selected_strategy",
            "CONTROLLED_SOURCE_VARIATION"
        )

        source_file = (
            self.find_source_sample()
        )

        mutation = (
            self.mutation_engine.mutate(
                source_file,
                strategy=strategy
            )
        )

        result = {
            "previous_experiment":
                decision.get(
                    "previous_experiment"
                ),

            "previous_visibility":
                decision.get(
                    "previous_visibility"
                ),

            "selected_strategy":
                strategy,

            "experiment_id":
                mutation["experiment_id"],

            "source":
                mutation["source"],

            "generated_sample":
                mutation["output"]
        }

        return result

    def save_state(
        self,
        result,
        output_file="experiments/adaptive_state.json"
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
                result,
                indent=4
            ),
            encoding="utf-8"
        )

        return output_path


def main():

    print()
    print("=" * 60)
    print(" ADAPTIVE SECURITY RESEARCH LOOP")
    print("=" * 60)

    try:

        loop = AdaptiveResearchLoop()

        result = (
            loop.create_experiment()
        )

        state_file = (
            loop.save_state(result)
        )

        print()

        print(
            f"Previous Experiment : "
            f"{result.get('previous_experiment')}"
        )

        print(
            f"Previous Visibility : "
            f"{result.get('previous_visibility')}%"
        )

        print(
            f"Selected Strategy   : "
            f"{result.get('selected_strategy')}"
        )

        print(
            f"New Experiment      : "
            f"{result.get('experiment_id')}"
        )

        print(
            f"Generated Sample    : "
            f"{result.get('generated_sample')}"
        )

        print()

        print(
            f"[+] State saved: "
            f"{state_file}"
        )

        print()
        print(
            "[+] Adaptive experiment ready."
        )

    except Exception as error:

        print()
        print(
            f"[!] Error: {error}"
        )


if __name__ == "__main__":
    main()