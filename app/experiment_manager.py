from pathlib import Path
import json
import subprocess
import sys
from datetime import datetime, timezone
from app.mutation_engine import BenignMutationEngine
from app.telemetry_collector import TelemetryCollector
from app.reward_engine import ResearchAnalysisEngine
from app.windows_telemetry import WindowsTelemetryCollector
from app.sysmon_telemetry import SysmonTelemetryCollector
class ExperimentManager:
    def __init__(self):
        self.mutation_engine = BenignMutationEngine()
        self.telemetry_collector = TelemetryCollector()
        self.analysis_engine = ResearchAnalysisEngine()
        self.windows_telemetry = WindowsTelemetryCollector()
        self.experiment_dir = Path("experiments")
        self.experiment_dir.mkdir(
            parents=True,
            exist_ok=True
        )
    def execute_sample(self, sample_path):
        process = subprocess.run(
            [
                sys.executable,
                str(sample_path)
            ],
            capture_output=True,
            text=True,
            timeout=30
        )
        return {
            "return_code": process.returncode,
            "stdout": process.stdout,
            "stderr": process.stderr,
            "status": (
                "COMPLETED"
                if process.returncode == 0
                else "FAILED"
            )
        }
    def run_experiment(
        self,
        sample_path,
        count=3
    ):
        sample_path = Path(sample_path)
        if not sample_path.exists():
            raise FileNotFoundError(
                f"Sample not found: {sample_path}"
            )
        results = []
        for iteration in range(1, count + 1):
            print(
                f"\n[*] Starting experiment "
                f"{iteration}/{count}"
            )
            # Create benign mutation
            mutation = self.mutation_engine.mutate(
                sample_path
            )
            experiment_id = mutation["experiment_id"]
            mutated_sample = Path(
                mutation["output"]
            )
            print(
                f"[+] Experiment ID: "
                f"{experiment_id}"
            )
            # Execute benign sample
            execution = self.execute_sample(
                mutated_sample
            )
            print(
                f"[+] Execution: "
                f"{execution['status']}"
            )
            # Internal research telemetry
            self.telemetry_collector.record_event(
                experiment_id,
                "PROCESS_START",
                f"Started {mutated_sample.name}"
            )
            self.telemetry_collector.record_event(
                experiment_id,
                "FILE_OPERATION",
                "Benign test file operation completed"
            )
            self.telemetry_collector.record_event(
                experiment_id,
                "PROCESS_END",
                f"Process returned code "
                f"{execution['return_code']}"
            )
            # Windows Event Log telemetry
            print(
                "[*] Collecting Windows Event Log..."
            )
            windows_events = (
                self.windows_telemetry.collect_system_events(
                    experiment_id=experiment_id,
                    count=20
                )
            )
            print(
                f"[+] Windows events collected: "
                f"{len(windows_events)}"
            )
            # Analyze internal telemetry
            telemetry_file = (
                Path("telemetry")
                / f"{experiment_id}.json"
            )
            analysis = self.analysis_engine.analyze(
                telemetry_file
            )
            results.append({
                "experiment_id": experiment_id,
                "iteration": iteration,
                "sample": str(mutated_sample),
                "execution": execution,
                "analysis": analysis,
                "windows_event_count": len(
                    windows_events
                ),
                "timestamp": datetime.now().isoformat()
            })
        # Final experiment report
        report = {
            "project": (
                "AI-Driven Adaptive "
                "Evasion Research Framework"
            ),
            "experiment_started": (
                datetime.now().isoformat()
            ),
            "total_variants": len(results),
            "results": results
        }
        report_file = (
            self.experiment_dir
            / "full_experiment_report.json"
        )
        report_file.write_text(
            json.dumps(
                report,
                indent=4
            ),
            encoding="utf-8"
        )
        return report

if __name__ == "__main__":
    manager = ExperimentManager()
    samples = list(
        Path("samples").glob("*.py")
    )
    if not samples:
        print(
            "[!] No benign sample found."
        )
        sys.exit(1)
    report = manager.run_experiment(
        samples[0],
        count=3
    )
    print("\n================================")
    print(" EXPERIMENT COMPLETED")
    print("================================")
    for result in report["results"]:
        print(
            f"\n{result['experiment_id']}"
        )
        print(
            f"  Execution : "
            f"{result['execution']['status']}"
        )
        print(
            f"  Events    : "
            f"{result['analysis']['total_events']}"
        )
        print(
            f"  Process   : "
            f"{result['analysis']['process_events']}"
        )
        print(
            f"  Files     : "
            f"{result['analysis']['file_events']}"
        )
        print(
            f"  Network   : "
            f"{result['analysis']['network_events']}"
        )
        print(
            f"  Windows   : "
            f"{result['windows_event_count']}"
        )
    print(
        "\n[+] Full report:"
    )
    print(
        "    experiments/"
        "full_experiment_report.json"
    )