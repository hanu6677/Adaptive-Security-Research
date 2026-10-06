from pathlib import Path
import re
import uuid


class BenignMutationEngine:
    """
    Generates harmless source-code variants for
    defensive telemetry research.
    """

    def __init__(self, output_dir="mutations"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def mutate(
        self,
        source_file,
        strategy="CONTROLLED_SOURCE_VARIATION"
    ):
        source_file = Path(source_file)

        if not source_file.exists():
            raise FileNotFoundError(
                f"Source file not found: {source_file}"
            )

        code = source_file.read_text(
            encoding="utf-8"
        )

        experiment_id = (
            f"MUT-{uuid.uuid4().hex[:8].upper()}"
        )

        mutated_code = self.apply_strategy(
            code,
            strategy,
            experiment_id
        )

        output_file = (
            self.output_dir
            / f"{experiment_id}_{source_file.name}"
        )

        output_file.write_text(
            mutated_code,
            encoding="utf-8"
        )

        return {
            "experiment_id": experiment_id,
            "strategy": strategy,
            "source": str(source_file),
            "output": str(output_file)
        }

    def apply_strategy(
        self,
        code,
        strategy,
        experiment_id
    ):

        if strategy == "FILE_STRUCTURE_VARIATION":
            code = self.file_structure_variation(code)

        elif strategy == "PROCESS_STRUCTURE_VARIATION":
            code = self.process_structure_variation(code)

        elif strategy == "BASELINE_REPETITION":
            code = self.baseline_variation(code)

        else:
            code = self.controlled_source_variation(code)

        return self.add_research_header(
            code,
            experiment_id,
            strategy
        )

    def file_structure_variation(self, code):

        code = re.sub(
            r'\btest_file\b',
            'telemetry_test_file',
            code
        )

        code = code.replace(
            'research_test_file.txt',
            'research_file_variant.txt'
        )

        return code

    def process_structure_variation(self, code):

        code = code.replace(
            'def run_test():',
            'def execute_research_test():'
        )

        code = code.replace(
            'run_test()',
            'execute_research_test()'
        )

        return code

    def baseline_variation(self, code):

        return code

    def controlled_source_variation(self, code):

        replacements = {
            "test_file": "research_file",
            "content": "research_content"
        }

        for old_name, new_name in replacements.items():

            code = re.sub(
                rf"\b{old_name}\b",
                new_name,
                code
            )

        return code

    def add_research_header(
        self,
        code,
        experiment_id,
        strategy
    ):

        header = f'''"""
Adaptive Research Experiment
Experiment ID: {experiment_id}
Strategy: {strategy}
Purpose: Defensive telemetry visibility research.
"""

'''

        return header + code