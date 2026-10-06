import json
from pathlib import Path
from html import escape


INPUT_FILE = Path("reports/final_research_report.json")
OUTPUT_FILE = Path("reports/research_dashboard.html")


def load_report():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Final report not found: {INPUT_FILE}"
        )

    return json.loads(
        INPUT_FILE.read_text(encoding="utf-8")
    )


def progress_bar(value):
    value = float(value or 0)

    return f"""
    <div class="progress">
        <div class="progress-fill"
             style="width:{min(value, 100)}%">
        </div>
    </div>

    <span>{value:.1f}%</span>
    """


def badge(value):
    if value:
        return '<span class="badge observed">Observed</span>'

    return '<span class="badge not-observed">Not Observed</span>'


def build_experiment_rows(experiments):

    rows = []

    for experiment in experiments:

        telemetry = experiment.get(
            "telemetry",
            {}
        )

        rows.append(f"""
        <tr>

            <td class="mono">
                {escape(str(
                    experiment.get(
                        "experiment_id",
                        "UNKNOWN"
                    )
                ))}
            </td>

            <td>
                {telemetry.get(
                    "total_events",
                    0
                )}
            </td>

            <td>
                {telemetry.get(
                    "process_events",
                    0
                )}
            </td>

            <td>
                {telemetry.get(
                    "file_events",
                    0
                )}
            </td>

            <td>
                {telemetry.get(
                    "network_events",
                    0
                )}
            </td>

            <td>
                {telemetry.get(
                    "dns_events",
                    0
                )}
            </td>

            <td>
                {progress_bar(
                    experiment.get(
                        "expected_behavior_visibility",
                        0
                    )
                )}
            </td>

            <td>
                {progress_bar(
                    experiment.get(
                        "telemetry_category_coverage",
                        0
                    )
                )}
            </td>

        </tr>
        """)

    return "".join(rows)


def build_details(experiments):

    sections = []

    for experiment in experiments:

        expected = experiment.get(
            "expected_behavior",
            {}
        )

        observed = experiment.get(
            "observed_behavior",
            {}
        )

        missing = experiment.get(
            "missing_expected_categories",
            []
        )

        expected_rows = ""

        for category, value in expected.items():

            expected_rows += f"""
            <div class="behavior-row">
                <span>{category}</span>
                {badge(value)}
            </div>
            """

        observed_rows = ""

        for category, value in observed.items():

            observed_rows += f"""
            <div class="behavior-row">
                <span>{category}</span>
                {badge(value)}
            </div>
            """

        sections.append(f"""

        <div class="detail-card">

            <div class="detail-header">

                <span class="mono">
                    {escape(str(
                        experiment.get(
                            "experiment_id",
                            "UNKNOWN"
                        )
                    ))}
                </span>

                <strong>
                    Expected Visibility:
                    {experiment.get(
                        "expected_behavior_visibility",
                        0
                    )}%
                </strong>

            </div>


            <div class="behavior-grid">

                <div>

                    <h3>
                        Expected Behavior
                    </h3>

                    {expected_rows}

                </div>


                <div>

                    <h3>
                        Observed Behavior
                    </h3>

                    {observed_rows}

                </div>

            </div>


            <div class="missing">

                <strong>
                    Missing Expected Categories:
                </strong>

                {
                    ", ".join(missing)
                    if missing
                    else "None"
                }

            </div>

        </div>

        """)

    return "".join(sections)


def build_dashboard(report):

    summary = report.get(
        "summary",
        {}
    )

    experiments = report.get(
        "experiments",
        []
    )

    observed_categories = set(
        summary.get(
            "categories_observed",
            []
        )
    )

    categories = [
        "PROCESS",
        "FILE",
        "NETWORK",
        "DNS",
        "REGISTRY"
    ]

    category_cards = ""

    for category in categories:

        category_cards += f"""

        <div class="category-card">

            <div class="category-name">
                {category}
            </div>

            {badge(
                category in observed_categories
            )}

        </div>

        """

    rows = build_experiment_rows(
        experiments
    )

    details = build_details(
        experiments
    )

    return f"""<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>
Adaptive Security Research Dashboard
</title>


<style>

* {{
    box-sizing: border-box;
}}


body {{

    margin: 0;

    background:
        #0b1020;

    color:
        #e8edf7;

    font-family:
        Arial,
        Helvetica,
        sans-serif;

}}


.container {{

    max-width:
        1400px;

    margin:
        auto;

    padding:
        32px;

}}


header {{

    margin-bottom:
        30px;

}}


h1 {{

    margin:
        0 0 8px;

    font-size:
        34px;

}}


.subtitle {{

    color:
        #9aa8c2;

    line-height:
        1.6;

}}


.summary-grid {{

    display:
        grid;

    grid-template-columns:
        repeat(
            auto-fit,
            minmax(200px, 1fr)
        );

    gap:
        16px;

}}


.card {{

    background:
        #121a2e;

    border:
        1px solid #293653;

    border-radius:
        14px;

    padding:
        22px;

}}


.card-label {{

    color:
        #9aa8c2;

    font-size:
        13px;

    margin-bottom:
        10px;

}}


.card-value {{

    font-size:
        30px;

    font-weight:
        bold;

}}


.section {{

    margin-top:
        35px;

}}


.section h2 {{

    margin-bottom:
        15px;

}}


.category-grid {{

    display:
        grid;

    grid-template-columns:
        repeat(
            auto-fit,
            minmax(160px, 1fr)
        );

    gap:
        14px;

}}


.category-card {{

    background:
        #121a2e;

    border:
        1px solid #293653;

    border-radius:
        12px;

    padding:
        18px;

}}


.category-name {{

    font-weight:
        bold;

    margin-bottom:
        12px;

}}


.badge {{

    display:
        inline-block;

    padding:
        5px 10px;

    border-radius:
        20px;

    font-size:
        11px;

}}


.observed {{

    background:
        rgba(72, 213, 151, .15);

    color:
        #48d597;

}}


.not-observed {{

    background:
        rgba(154, 168, 194, .12);

    color:
        #9aa8c2;

}}


.table-container {{

    background:
        #121a2e;

    border:
        1px solid #293653;

    border-radius:
        14px;

    overflow:
        auto;

}}


table {{

    width:
        100%;

    border-collapse:
        collapse;

}}


th,
td {{

    padding:
        14px;

    text-align:
        left;

    border-bottom:
        1px solid #293653;

    white-space:
        nowrap;

}}


th {{

    color:
        #9aa8c2;

    font-size:
        12px;

    text-transform:
        uppercase;

}}


tr:hover {{

    background:
        #18233b;

}}


.mono {{

    font-family:
        Consolas,
        monospace;

}}


.progress {{

    display:
        inline-block;

    width:
        90px;

    height:
        7px;

    background:
        #27334d;

    border-radius:
        10px;

    overflow:
        hidden;

    vertical-align:
        middle;

    margin-right:
        7px;

}}


.progress-fill {{

    height:
        100%;

    background:
        #6ea8fe;

}}


.details {{

    display:
        grid;

    gap:
        16px;

}}


.detail-card {{

    background:
        #121a2e;

    border:
        1px solid #293653;

    border-radius:
        14px;

    padding:
        22px;

}}


.detail-header {{

    display:
        flex;

    justify-content:
        space-between;

    margin-bottom:
        20px;

}}


.behavior-grid {{

    display:
        grid;

    grid-template-columns:
        repeat(
            auto-fit,
            minmax(280px, 1fr)
        );

    gap:
        30px;

}}


.behavior-row {{

    display:
        flex;

    justify-content:
        space-between;

    padding:
        9px 0;

    border-bottom:
        1px solid #293653;

}}


.missing {{

    margin-top:
        18px;

    padding:
        13px;

    background:
        #18233b;

    border-radius:
        8px;

    color:
        #9aa8c2;

}}


footer {{

    margin-top:
        40px;

    padding-top:
        20px;

    border-top:
        1px solid #293653;

    color:
        #9aa8c2;

    font-size:
        12px;

}}
.charts {{
    display: grid;
    gap: 18px;
}}

.chart-card {{
    background: #121a2e;
    border: 1px solid #293653;
    border-radius: 14px;
    padding: 20px;
}}

.chart-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 22px;
}}

.chart {{
    display: grid;
    gap: 12px;
}}

.chart-row {{
    display: grid;
    grid-template-columns: 90px 1fr 50px;
    gap: 10px;
    align-items: center;
}}

.chart-label {{
    font-size: 12px;
}}

.chart-track {{
    height: 10px;
    background: #27334d;
    border-radius: 10px;
    overflow: hidden;
}}

.chart-bar {{
    height: 100%;
}}

.chart-value {{
    font-size: 12px;
    text-align: right;
}}

.process {{
    background: #6ea8fe;
}}

.file {{
    background: #48d597;
}}

.network {{
    background: #f3c969;
}}

.dns {{
    background: #ef7b8f;
}}

.registry {{
    background: #b58cff;
}}

details {{
    margin-top: 22px;
}}

summary {{
    cursor: pointer;
    color: #9aa8c2;
    padding: 10px 0;
}}

.timeline-table {{
    margin-top: 12px;
    overflow-x: auto;
}}

.empty-chart {{
    background: #121a2e;
    border: 1px solid #293653;
    border-radius: 14px;
    padding: 25px;
    color: #9aa8c2;
}}
</style>

</head>


<body>

<div class="container">


<header>

<h1>
Adaptive Security Research Dashboard
</h1>

<div class="subtitle">

Defensive telemetry visibility analysis
for controlled benign security experiments.

</div>

</header>


<div class="summary-grid">


<div class="card">

<div class="card-label">
Total Experiments
</div>

<div class="card-value">
{summary.get(
    "total_experiments",
    0
)}
</div>

</div>


<div class="card">

<div class="card-label">
Average Behavior Visibility
</div>

<div class="card-value">
{summary.get(
    "average_behavior_visibility",
    0
)}%
</div>

</div>


<div class="card">

<div class="card-label">
Fully Visible
</div>

<div class="card-value">
{summary.get(
    "fully_visible_experiments",
    0
)}
</div>

</div>


<div class="card">

<div class="card-label">
Average Telemetry Coverage
</div>

<div class="card-value">
{summary.get(
    "average_telemetry_coverage",
    0
)}%
</div>

</div>


</div>


<section class="section">

<h2>
Telemetry Categories
</h2>
<div class="category-grid">
{category_cards}
</div>
</section>
<section class="section">
<h2>
Experiment Overview
</h2>
<div class="table-container"
<table>
<thead>
<tr>
<th>Experiment</th>
<th>Total</th>
<th>Process</th>
<th>File</th>
<th>Network</th>
<th>DNS</th>
<th>Expected Visibility</th>
<th>Category Coverage</th>
</tr>
</thead>
<tbody>
{rows}
</tbody>
</table>
</div>
</section>
<section class="section">
<h2>
Experiment Details
</h2>
<div class="details">
{details}
</div>
</section>
<footer>
Generated from
final_research_report.json.
Defensive telemetry and visibility
research dashboard.
</footer>
</div>
</body>
</html>
"""
def load_timeline():

    timeline_file = Path(
        "reports/timeline_data.json"
    )

    if not timeline_file.exists():
        return {
            "experiments": []
        }

    return json.loads(
        timeline_file.read_text(
            encoding="utf-8"
        )
    )


def build_chart_section(timeline_data):

    experiments = timeline_data.get(
        "experiments",
        []
    )

    if not experiments:
        return """
        <div class="empty-chart">
            No timeline data available.
        </div>
        """

    html = ""

    for experiment in experiments:

        counts = experiment.get(
            "category_counts",
            {}
        )

        total = max(
            experiment.get(
                "event_count",
                0
            ),
            1
        )

        categories = [
            ("PROCESS", "process"),
            ("FILE", "file"),
            ("NETWORK", "network"),
            ("DNS", "dns"),
            ("REGISTRY", "registry")
        ]

        bars = ""

        for category, css_class in categories:

            count = counts.get(
                category,
                0
            )

            width = (
                count / total
            ) * 100

            bars += f"""
            <div class="chart-row">

                <div class="chart-label">
                    {category}
                </div>

                <div class="chart-track">

                    <div
                        class="chart-bar {css_class}"
                        style="width:{width}%">
                    </div>

                </div>

                <div class="chart-value">
                    {count}
                </div>

            </div>
            """

        timeline_rows = ""

        for event in experiment.get(
            "timeline",
            []
        ):

            timeline_rows += f"""
            <tr>

                <td class="mono">
                    {escape(
                        str(
                            event.get(
                                "timestamp",
                                ""
                            )
                        )
                    )}
                </td>

                <td>
                    {escape(
                        str(
                            event.get(
                                "category",
                                "OTHER"
                            )
                        )
                    )}
                </td>

                <td>
                    {escape(
                        str(
                            event.get(
                                "event_type",
                                "UNKNOWN"
                            )
                        )
                    )}
                </td>

                <td>
                    {escape(
                        str(
                            event.get(
                                "source",
                                ""
                            )
                        )
                    )}
                </td>

            </tr>
            """

        html += f"""

        <div class="chart-card">

            <div class="chart-header">

                <span class="mono">
                    {escape(
                        str(
                            experiment.get(
                                "experiment_id",
                                "UNKNOWN"
                            )
                        )
                    )}
                </span>

                <span>
                    Events:
                    {experiment.get(
                        "event_count",
                        0
                    )}
                </span>

            </div>


            <div class="chart">

                {bars}

            </div>


            <details>

                <summary>
                    View Event Timeline
                </summary>

                <div class="timeline-table">

                    <table>

                        <thead>

                            <tr>
                                <th>Timestamp</th>
                                <th>Category</th>
                                <th>Event</th>
                                <th>Source</th>
                            </tr>

                        </thead>

                        <tbody>

                            {timeline_rows}

                        </tbody>

                    </table>

                </div>

            </details>

        </div>

        """

    return html
def main():
    print()
    print("=" * 50)
    print(" RESEARCH DASHBOARD")
    print("=" * 50)
    report = load_report()
    html = build_dashboard(
        report
    )
    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )
    OUTPUT_FILE.write_text(
        html,
        encoding="utf-8"
    )
    print()
    print(
        f"[+] Dashboard created:"
    )
    print(
        f"    {OUTPUT_FILE}"
    )
if __name__ == "__main__":
    main()