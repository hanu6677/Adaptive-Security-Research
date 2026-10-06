from pathlib import Path
import json
import subprocess
from datetime import datetime, timezone

from app.adaptive_selector import AdaptiveExperimentSelector
from app.mutation_engine import BenignMutationEngine
from app.telemetry_collector import TelemetryCollector
from app.windows_telemetry import WindowsTelemetryCollector
from app.sysmon_telemetry import SysmonTelemetryCollector


class AdaptiveRunner:

    def __init__(self):

        self.selector = AdaptiveExperimentSelector()

        self.mutation_engine = BenignMutationEngine()

        self.internal_telemetry = (
            TelemetryCollector()
        )

        self.windows_telemetry = (
            WindowsTelemetryCollector()
        )

        self.sysmon_telemetry = (
            SysmonTelemetryCollector()
        )

    def find_source(self):

        samples = list(
            Path("samples").glob("*.py")
        )

        samples = [
            item for item in samples
            if item.name != "__init__.py"
        ]

        if not samples:
            raise FileNotFoundError(
                "No benign sample found in samples/"
            )

        return samples[0]

    def run(self):

        print()
        print("=" * 60)
        print(" ADAPTIVE SECURITY RESEARCH RUN")
        print("=" * 60)

        # --------------------------------
        # 1. Select next strategy
        # --------------------------------

        decision = (
            self.selector
            .select_next_experiment()
        )

        strategy = decision.get(
            "selected_strategy",
            "CONTROLLED_SOURCE_VARIATION"
        )

        print()
        print(
            f"[1] Selected Strategy : {strategy}"
        )

        # --------------------------------
        # 2. Generate safe mutation
        # --------------------------------

        source_file = self.find_source()

        mutation = (
            self.mutation_engine.mutate(
                source_file,
                strategy=strategy
            )
        )

        experiment_id = mutation[
            "experiment_id"
        ]

        generated_sample = Path(
            mutation["output"]
        )

        print(
            f"[2] Experiment ID      : "
            f"{experiment_id}"
        )

        print(
            f"[2] Generated Sample   : "
            f"{generated_sample}"
        )

        # --------------------------------
        # 3. Start experiment
        # --------------------------------

        start_time = datetime.now(
            timezone.utc
        )

        self.internal_telemetry.record_event(
            experiment_id,
            "PROCESS_START",
            "Benign adaptive research sample started"
        )

        # --------------------------------
        # 4. Execute benign sample
        # --------------------------------

        print()
        print(
            "[3] Running benign experiment..."
        )

        execution = subprocess.run(
            [
                "python",
                str(generated_sample)
            ],
            capture_output=True,
            text=True,
            timeout=30
        )

        print(
            f"[3] Exit Code          : "
            f"{execution.returncode}"
        )

        if execution.stdout:
            print(
                execution.stdout.strip()
            )

        # --------------------------------
        # 5. Internal telemetry
        # --------------------------------

        self.internal_telemetry.record_event(
            experiment_id,
            "FILE_OPERATION",
            "Benign research sample performed controlled file activity"
        )

        self.internal_telemetry.record_event(
            experiment_id,
            "PROCESS_END",
            "Benign adaptive research sample completed"
        )

        # --------------------------------
        # 6. Windows telemetry
        # --------------------------------

        print()
        print(
            "[4] Collecting Windows telemetry..."
        )

        try:

            windows_events = (
                self.windows_telemetry
                .collect_system_events(
                    experiment_id,
                    count=50
                )
            )

        except Exception as error:

            print(
                f"[!] Windows telemetry error: "
                f"{error}"
            )

            windows_events = []

        # --------------------------------
        # 7. Sysmon telemetry
        # --------------------------------

        print(
            "[5] Collecting Sysmon telemetry..."
        )

        try:

            sysmon_result = (
                self.sysmon_telemetry
                .collect_events(
                    experiment_id,
                    count=100
                )
            )

        except Exception as error:

            print(
                f"[!] Sysmon telemetry error: "
                f"{error}"
            )

            sysmon_result = {
                "available": False,
                "events": []
            }

        end_time = datetime.now(
            timezone.utc
        )

        # --------------------------------
        # 8. Save adaptive experiment state
        # --------------------------------

        result = {

            "experiment_id":
                experiment_id,

            "strategy":
                strategy,

            "source":
                str(source_file),

            "generated_sample":
                str(generated_sample),

            "experiment_start":
                start_time.isoformat(),

            "experiment_end":
                end_time.isoformat(),

            "execution": {

                "return_code":
                    execution.returncode,

                "stdout":
                    execution.stdout,

                "stderr":
                    execution.stderr

            },

            "telemetry": {

                "internal":
                    3,

                "windows":
                    len(windows_events),

                "sysmon_available":
                    sysmon_result.get(
                        "available",
                        False
                    ),

                "sysmon":
                    len(
                        sysmon_result.get(
                            "events",
                            []
                        )
                    )
            }
        }

        output_file = Path(
            "experiments"
        ) / f"{experiment_id}_adaptive.json"

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        output_file.write_text(
            json.dumps(
                result,
                indent=4
            ),
            encoding="utf-8"
        )

        print()
        print("=" * 60)
        print(" ADAPTIVE RUN COMPLETED")
        print("=" * 60)

        print(
            f"Experiment : {experiment_id}"
        )

        print(
            f"Windows    : {len(windows_events)}"
        )

        print(
            f"Sysmon     : "
            f"{len(sysmon_result.get('events', []))}"
        )

        print(
            f"Saved      : {output_file}"
        )

        return result


if __name__ == "__main__":

    runner = AdaptiveRunner()

    try:
        runner.run()

    except Exception as error:

        print()
        print(
            f"[!] Adaptive run failed: {error}"
        )