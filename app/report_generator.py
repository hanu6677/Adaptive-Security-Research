import json
from pathlib import Path
from datetime import datetime
class ResearchReportGenerator:
    def __init__(self):
        self.report_dir = Path("reports")
        self.report_dir.mkdir(
            parents=True,
            exist_ok=True
        )
    def load_experiment_report(self):
        report_file = (
            Path("experiments")
            / "full_experiment_report.json"
        )
        if not report_file.exists():
            raise FileNotFoundError(
                "Experiment report not found: "
                "experiments/full_experiment_report.json"
            )
        return json.loads(
            report_file.read_text(
                encoding="utf-8"
            )
        )
    def generate_json_report(self, data):
        output_file = (
            self.report_dir
            / "research_report.json"
        )
        final_report = {
            "project": data.get(
                "project",
                "Adaptive Security Research Framework"
            ),
            "generated_at": datetime.now().isoformat(),
            "total_experiments": data.get(
                "total_variants",
               0
            ),
            "experiments": data.get(
                "results",
                []
            )
        }
        output_file.write_text(
            json.dumps(
                final_report,
                indent=4
            ),
            encoding="utf-8"
        )
        return output_file
    def generate_html_report(self, data):
        results = data.get("results", [])
        rows = ""
        for result in results:
            experiment_id = result.get(
                "experiment_id",
                "N/A"
            )
            execution = result.get(
                "execution",
                {}
            )
            analysis = result.get(
                "analysis",
                {}
            )
            windows_count = result.get(
                "windows_event_count",
                0
            )
            sysmon_count = result.get(
                "sysmon_event_count",
                0
            )
            rows += f"""
            <tr>
                <td>{experiment_id}</td>
                <td>{result.get("iteration", "N/A")}</td>
                <td>{execution.get("status", "N/A")}</td>
                <td>{analysis.get("total_events", 0)}</td>
                <td>{analysis.get("process_events", 0)}</td>
                <td>{analysis.get("file_events", 0)}</td>
                <td>{analysis.get("network_events", 0)}</td>
                <td>{windows_count}</td>
                <td>{sysmon_count}</td>
            </tr>
            """
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport"
      content="width=device-width, initial-scale=1.0">
<title>Adaptive Security Research Report</title>
<style>
body {{
    font-family: Arial, sans-serif;
    margin: 40px;
    background: #f5f7fa;
    color: #222;
}}
.container {{
    max-width: 1400px;
    margin: auto;
}}
.header {{
    background: #1f2937;
    color: white;
    padding: 25px;
    border-radius: 10px;
    margin-bottom: 25px;
}}
.cards {{
    display: flex;
    gap: 15px;
    flex-wrap: wrap;
    margin-bottom: 25px;
}}
.card {{
    background: white;
    padding: 20px;
    border-radius: 10px;
    min-width: 180px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}}
.card h2 {{
    margin: 0;
    font-size: 28px;
}}
.card p {{
    margin-bottom: 0;
    color: #666;
}}
table {{
    width: 100%;
    border-collapse: collapse;
    background: white;
}}
th, td {{
    padding: 12px;
    border-bottom: 1px solid #ddd;
    text-align: left;
}}
th {{
    background: #374151;
    color: white;
}}
tr:hover {{
    background: #f1f5f9;
}}
.footer {{
    margin-top: 25px;
    color: #666;
    font-size: 13px;
}}
</style>
</head>
<body>
<div class="container">
<div class="header">
<h1>Adaptive Security Research Report</h1>
<p>
AI-Driven Adaptive Evasion Research Framework
</p>
<p>
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
</p>
</div>
<div class="cards">
<div class="card">
<h2>{len(results)}</h2>
<p>Total Experiments</p>
</div>
<div class="card">
<h2>{sum(
    1 for r in results
    if r.get("execution", {}).get("status") == "COMPLETED"
)}</h2>
<p>Completed</p>
</div>
<div class="card">
<h2>{sum(
    r.get("analysis", {}).get("process_events", 0)
    for r in results
)}</h2>
<p>Process Events</p>
</div>
<div class="card">
<h2>{sum(
    r.get("analysis", {}).get("file_events", 0)
    for r in results
)}</h2>
<p>File Events</p>
</div>
<div class="card">
<h2>{sum(
    r.get("analysis", {}).get("network_events", 0)
    for r in results
)}</h2>
<p>Network Events</p>
</div>
<div class="card">
<h2>{sum(
    r.get("windows_event_count", 0)
    for r in results
)}</h2>
<p>Windows Events</p>
</div>
</div>
<h2>Experiment Results</h2>
<table>
<thead>
<tr>
<th>Experiment</th>
<th>Iteration</th>
<th>Execution</th>
<th>Total Events</th>
<th>Process</th>
<th>File</th>
<th>Network</th>
<th>Windows</th>
<th>Sysmon</th>
</tr>
</thead>
<tbody>
{rows}
</tbody>
</table>
<div class="footer">
<p>
This report contains telemetry from controlled benign
security research experiments.
</p>
<p>
The framework is intended for defensive security research,
telemetry analysis, and detection visibility testing.
</p>
</div>
</div>
</body>
</html>
"""
        output_file = (
            self.report_dir
            / "research_report.html"
        )
        output_file.write_text(
            html,
            encoding="utf-8"
        )
        return output_file
if __name__ == "__main__":
    generator = ResearchReportGenerator()
    data = generator.load_experiment_report()
    json_file = generator.generate_json_report(
        data
    )
    html_file = generator.generate_html_report(
        data
    )
    print("\n================================")
    print(" RESEARCH REPORT GENERATED")
    print("================================")
    print(f"\n[+] JSON:")
    print(f"    {json_file}")
    print(f"\n[+] HTML:")
    print(f"    {html_file}")