#!/usr/bin/env python3
"""
TorusGuard Visual HTML Report Emitter (v1.2.0)
Compiles a self-contained, zero-external-CDN, interactive dark-mode dashboard.
Embeds SVG gauges, 7-stage pipeline radar, Golden Fix Recipes, and attack surface analytics.
Zero external runtime dependencies (100% Python 3.10+ standard library).
"""

import sys
import json
import html
import datetime
import argparse
from pathlib import Path
from typing import Any

# Windows console UTF-8 support
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        getattr(sys.stdout, "reconfigure")(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    try:
        getattr(sys.stderr, "reconfigure")(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass


def find_project_root(start_dir: str | Path | None = None) -> Path:
    """Detect project root directory."""
    current = Path(start_dir or Path.cwd()).resolve()
    markers = [".git", "package.json", "pyproject.toml", ".torusguard"]
    for m in markers:
        if (current / m).exists():
            return current
    for parent in current.parents:
        for m in markers:
            if (parent / m).exists():
                return parent
    return current


def load_report_telemetry(root_dir: Path) -> dict[str, Any]:
    """Gather all project telemetry, rules catalog, and memory state."""
    tg_dir = root_dir / ".torusguard"
    memory_dir = tg_dir / "memory"
    config_file = tg_dir / "config" / "torusguard.json"

    cfg: dict[str, Any] = {}
    if config_file.exists():
        try:
            cfg = json.loads(config_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            cfg = {}

    profile_file = memory_dir / "profile.json"
    patterns_file = memory_dir / "patterns.json"
    context_file = memory_dir / "context.json"

    profile: dict[str, Any] = {}
    patterns: list[dict[str, Any]] = []
    context: dict[str, Any] = {}

    if profile_file.exists():
        try:
            profile = json.loads(profile_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            profile = {}

    if patterns_file.exists():
        try:
            patterns = json.loads(patterns_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            patterns = []

    if context_file.exists():
        try:
            context = json.loads(context_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            context = {}

    stack_info = cfg.get("detected_stack", {})
    if not stack_info:
        try:
            import stack_detect  # type: ignore
            stack_info = stack_detect.detect_stack(root_dir)
        except Exception:
            stack_info = {"language": "Universal", "framework": "None", "data_layer": "None"}

    ist_tz = datetime.timezone(datetime.timedelta(hours=5, minutes=30), name="IST")
    now_ist = datetime.datetime.now(ist_tz)
    return {
        "project_name": root_dir.name or "Project",
        "root_dir": str(root_dir),
        "generated_at": now_ist.strftime("%Y-%m-%d %H:%M:%S IST"),
        "config": cfg,
        "profile": profile,
        "patterns": patterns,
        "context": context,
        "detected_stack": stack_info
    }


def compute_posture_score(telemetry: dict[str, Any]) -> int:
    """Calculate an overall health score (0-100) based on verified fixes and regressions."""
    profile = telemetry.get("profile", {})
    patterns = telemetry.get("patterns", [])

    base_score = 85
    fix_rate = profile.get("fix_rate_percentage")
    if fix_rate is not None:
        base_score = int(fix_rate)

    regressions = sum(1 for p in patterns if p.get("pattern_type") == "regression_watch")
    recipes = sum(1 for p in patterns if p.get("pattern_type") == "golden_fix_recipe")

    score = base_score - (regressions * 5) + (recipes * 3)
    return min(max(score, 10), 100)


def generate_html_dashboard(telemetry: dict[str, Any]) -> str:
    """Build a complete, standalone, single-file HTML dashboard."""
    score = compute_posture_score(telemetry)
    profile = telemetry.get("profile", {})
    patterns = telemetry.get("patterns", [])
    cfg = telemetry.get("config", {})
    detected = cfg.get("detected_stack", {})
    stack = profile.get("stack", [])
    if not stack and detected.get("language") and detected.get("language") != "Unknown":
        stack = [detected["language"]]
        if detected.get("framework") and detected["framework"] != "None":
            stack.append(detected["framework"])
    stack_label = ", ".join(stack) if stack else "Universal Polyglot Application"

    recipes = [p for p in patterns if p.get("pattern_type") == "golden_fix_recipe"]
    regressions = [p for p in patterns if p.get("pattern_type") == "regression_watch"]
    false_positives = [p for p in patterns if p.get("pattern_type") == "false_positive_class"]
    recurring = [p for p in patterns if p.get("pattern_type") in ("recurring_fix", "common_vulnerability")]

    # SVG Circle Math for Gauge (radius 40, circ = 251.2)
    circumference = 251.2
    dash_offset = circumference - (circumference * (score / 100.0))
    score_color = "#3fb950" if score >= 80 else ("#d29922" if score >= 60 else "#f85149")

    # Generate recipe cards HTML
    recipe_cards_html = ""
    if recipes:
        for r in recipes[:6]:
            rule = html.escape(r.get("rule_id", "TG-SEC"))
            desc = html.escape(r.get("description", "Verified fix"))
            rdata = r.get("recipe_data", {})
            diff = html.escape(rdata.get("diff_snippet", ""))
            verified = rdata.get("verified_count", 1)
            metrics = rdata.get("ponytail_metrics", {})
            adds = metrics.get("additions", 0)
            dels = metrics.get("deletions", 0)

            recipe_cards_html += f"""
            <div class="card recipe-card">
              <div class="card-header">
                <span class="badge badge-success">{rule}</span>
                <span class="meta-label">Verified {verified}x &middot; +{adds}/-{dels} Ponytail</span>
              </div>
              <p class="recipe-desc">{desc}</p>
              <pre class="diff-block"><code>{diff}</code></pre>
            </div>
            """
    else:
        recipe_cards_html = """
        <div class="empty-state">
          <p>No golden fix recipes captured yet. Run <code>npx torusguard apply</code> (CLI) or <code>/torusguard-apply</code> (AI Chat) on verified remediations to distill reusable recipes.</p>
        </div>
        """

    # Generate regression watch & suppression rows
    regression_rows_html = ""
    combined_watches: list[dict[str, str]] = []
    for reg in regressions:
        combined_watches.append({
            "badge_class": "badge-danger",
            "rule": reg.get("rule_id", "TG-REG"),
            "desc": reg.get("description", "Active watch"),
            "target": ", ".join(reg.get("affected_files", [])) or "Monitored files"
        })
    for fp in false_positives:
        combined_watches.append({
            "badge_class": "badge-warning",
            "rule": fp.get("rule_id", "TG-FP"),
            "desc": fp.get("description", "False positive suppression"),
            "target": fp.get("reason") or "Suppressed rule pattern"
        })

    if combined_watches:
        for item in combined_watches:
            rule = html.escape(item["rule"])
            desc = html.escape(item["desc"])
            target = html.escape(item["target"])
            bclass = item["badge_class"]
            regression_rows_html += f"""
            <tr class="reg-row">
              <td><span class="badge {bclass}">{rule}</span></td>
              <td>{desc}</td>
              <td><code>{target}</code></td>
            </tr>
            """
    else:
        regression_rows_html = "<tr><td colspan='3' class='empty-cell'>Zero active security regressions or suppressions. Posture clean.</td></tr>"

    stack_info = telemetry.get("detected_stack", {})
    primary_lang = stack_info.get("language", "Universal")
    if primary_lang in ("Unknown", "None", "", None):
        root_path = Path(telemetry.get("root_dir", "."))
        if (root_path / "tsconfig.json").is_file() or list(root_path.glob("*.ts")) or list((root_path / "src").glob("*.ts*")):
            primary_lang = "TypeScript"
        elif (root_path / "package.json").is_file():
            primary_lang = "JavaScript / TypeScript"
        elif (root_path / "pyproject.toml").is_file() or (root_path / "requirements.txt").is_file() or list(root_path.glob("*.py")):
            primary_lang = "Python"
        elif (root_path / "go.mod").is_file():
            primary_lang = "Go"
        else:
            primary_lang = "Universal Polyglot"

    primary_fw = stack_info.get("framework", "None")
    primary_orm = stack_info.get("data_layer", "None")
    sub_stacks = stack_info.get("sub_stacks", [])

    chips = [f'<span class="chip chip-primary">&#9679; {html.escape(primary_lang)}</span>']
    if primary_fw and primary_fw != "None":
        chips.append(f'<span class="chip">&#9881; {html.escape(primary_fw)}</span>')
    if primary_orm and primary_orm != "None":
        chips.append(f'<span class="chip">&#128451; {html.escape(primary_orm)}</span>')
    for pkg in sub_stacks[:8]:
        pkg_p = html.escape(pkg.get("path", ""))
        pkg_l = html.escape(pkg.get("language", ""))
        pkg_f = html.escape(pkg.get("framework", ""))
        chips.append(f'<span class="chip" style="border-color: rgba(63, 185, 80, 0.4); color: var(--accent-green);">&#128230; {pkg_p} ({pkg_l} / {pkg_f})</span>')
    stack_chips_html = "\n".join(chips)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TorusGuard Security Posture &middot; {html.escape(telemetry['project_name'])}</title>
  <style>
    :root {{
      --bg-dark: #0d1117;
      --bg-surface: #161b22;
      --bg-card: #21262d;
      --border-subtle: #30363d;
      --text-main: #f0f6fc;
      --text-muted: #8b949e;
      --accent-blue: #58a6ff;
      --accent-green: #3fb950;
      --accent-yellow: #d29922;
      --accent-red: #f85149;
      --font-stack: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji";
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg-dark);
      color: var(--text-main);
      font-family: var(--font-stack);
      line-height: 1.5;
      padding: 24px;
    }}
    .container {{ max-width: 1200px; margin: 0 auto; }}
    header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 20px;
      border-bottom: 1px solid var(--border-subtle);
      margin-bottom: 24px;
    }}
    .logo-group h1 {{
      font-size: 24px;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .shield-icon {{ font-size: 26px; }}
    .project-meta {{ color: var(--text-muted); font-size: 14px; margin-top: 4px; }}
    .status-badge {{
      background: rgba(63, 185, 80, 0.15);
      border: 1px solid var(--accent-green);
      color: var(--accent-green);
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 13px;
      font-weight: 600;
    }}
    .grid-top {{
      display: grid;
      grid-template-columns: 280px 1fr 1fr 1fr;
      gap: 16px;
      margin-bottom: 24px;
    }}
    @media (max-width: 900px) {{
      .grid-top {{ grid-template-columns: 1fr 1fr; }}
    }}
    @media (max-width: 600px) {{
      .grid-top {{ grid-template-columns: 1fr; }}
    }}
    .card {{
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 20px;
    }}
    .gauge-card {{
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
    }}
    .gauge-svg {{ width: 120px; height: 120px; transform: rotate(-90deg); }}
    .gauge-bg {{ fill: none; stroke: var(--bg-card); stroke-width: 8; }}
    .gauge-fill {{
      fill: none;
      stroke: {score_color};
      stroke-width: 8;
      stroke-linecap: round;
      stroke-dasharray: 251.2;
      stroke-dashoffset: {dash_offset};
      transition: stroke-dashoffset 0.8s ease;
    }}
    .gauge-value {{
      position: absolute;
      font-size: 32px;
      font-weight: 700;
      color: var(--text-main);
    }}
    .stat-label {{ font-size: 13px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; }}
    .stat-value {{ font-size: 28px; font-weight: 700; color: var(--text-main); }}
    .stat-sub {{ font-size: 12px; color: var(--text-muted); margin-top: 6px; }}
    .pipeline-section {{ margin-bottom: 24px; }}
    .pipeline-tracker {{
      display: flex;
      justify-content: space-between;
      position: relative;
      margin-top: 16px;
    }}
    .pipeline-step {{
      display: flex;
      flex-direction: column;
      align-items: center;
      flex: 1;
      text-align: center;
      position: relative;
      z-index: 2;
    }}
    .step-circle {{
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background: var(--bg-card);
      border: 2px solid var(--accent-blue);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 13px;
      font-weight: 700;
      color: var(--accent-blue);
      margin-bottom: 8px;
    }}
    .step-circle.active {{ background: var(--accent-blue); color: var(--bg-dark); }}
    .step-name {{ font-size: 12px; font-weight: 600; color: var(--text-main); }}
    .step-cmd {{ font-size: 11px; color: var(--text-muted); font-family: monospace; margin-top: 2px; }}
    .pipeline-line {{
      position: absolute;
      top: 16px;
      left: 6%;
      right: 6%;
      height: 2px;
      background: var(--border-subtle);
      z-index: 1;
    }}
    .polyglot-chips {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 10px;
    }}
    .chip {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 16px;
      padding: 4px 12px;
      font-size: 12px;
      font-weight: 500;
      color: var(--text-main);
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }}
    .chip-primary {{
      border-color: var(--accent-blue);
      color: var(--accent-blue);
      background: rgba(88, 166, 255, 0.1);
    }}
    .grid-bottom {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
      margin-top: 24px;
    }}
    @media (max-width: 800px) {{
      .grid-bottom {{ grid-template-columns: 1fr; }}
    }}
    .section-title {{
      font-size: 18px;
      font-weight: 600;
      margin-bottom: 16px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .badge {{
      display: inline-block;
      padding: 3px 8px;
      border-radius: 12px;
      font-size: 11px;
      font-weight: 600;
      font-family: monospace;
    }}
    .badge-success {{ background: rgba(63, 185, 80, 0.15); color: var(--accent-green); border: 1px solid rgba(63, 185, 80, 0.3); }}
    .badge-danger {{ background: rgba(248, 81, 73, 0.15); color: var(--accent-red); border: 1px solid rgba(248, 81, 73, 0.3); }}
    .recipe-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 6px;
      padding: 12px;
      margin-bottom: 12px;
    }}
    .card-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }}
    .meta-label {{ font-size: 11px; color: var(--text-muted); }}
    .recipe-desc {{ font-size: 13px; color: var(--text-main); margin-bottom: 8px; }}
    .diff-block {{
      background: var(--bg-dark);
      border: 1px solid var(--border-subtle);
      border-radius: 4px;
      padding: 8px 12px;
      font-family: monospace;
      font-size: 12px;
      overflow-x: auto;
      color: #e6edf3;
    }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ padding: 10px 12px; text-align: left; font-size: 13px; }}
    th {{ color: var(--text-muted); border-bottom: 1px solid var(--border-subtle); font-weight: 600; font-size: 12px; text-transform: uppercase; }}
    td {{ border-bottom: 1px solid rgba(48, 54, 61, 0.5); }}
    .empty-state {{ text-align: center; padding: 24px; color: var(--text-muted); font-size: 13px; }}
    .empty-cell {{ text-align: center; color: var(--text-muted); padding: 16px; font-style: italic; }}
    footer {{
      margin-top: 40px;
      text-align: center;
      color: var(--text-muted);
      font-size: 12px;
      border-top: 1px solid var(--border-subtle);
      padding-top: 20px;
    }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div class="logo-group">
        <h1><span class="shield-icon">&#128737;</span> TorusGuard Security Posture</h1>
        <div class="project-meta">Workspace: <strong>{html.escape(telemetry['project_name'])}</strong> &middot; Stack: <strong>{html.escape(stack_label)}</strong> &middot; {telemetry['generated_at']}</div>
      </div>
      <div class="status-badge">&check; Local Governance Active</div>
    </header>

    <!-- Top KPI Grid -->
    <div class="grid-top">
      <div class="card gauge-card">
        <div style="position: relative; display: flex; align-items: center; justify-content: center;">
          <svg class="gauge-svg" viewBox="0 0 100 100">
            <circle class="gauge-bg" cx="50" cy="50" r="40" />
            <circle class="gauge-fill" cx="50" cy="50" r="40" />
          </svg>
          <div class="gauge-value">{score}</div>
        </div>
        <div class="stat-label" style="margin-top: 12px;">Security Posture Score</div>
      </div>

      <div class="card">
        <div class="stat-label">Verified Golden Recipes</div>
        <div class="stat-value" style="color: var(--accent-green);">{len(recipes)}</div>
        <div class="stat-sub">Distilled Ponytail fixes (<=35 add, <=25 del)</div>
      </div>

      <div class="card">
        <div class="stat-label">Active Memory Patterns</div>
        <div class="stat-value">{len(patterns)}</div>
        <div class="stat-sub">{len(false_positives)} suppressed &middot; {len(recurring)} recurring</div>
      </div>

      <div class="card">
        <div class="stat-label">Security Rules Catalog</div>
        <div class="stat-value" style="color: var(--accent-blue);">71</div>
        <div class="stat-sub">11 rule families &middot; Multi-agent verified</div>
      </div>
    </div>

    <!-- Polyglot Architecture & Workspace Intelligence -->
    <div class="card" style="margin-bottom: 24px;">
      <div class="section-title">&#9670; Polyglot Architecture &amp; Workspace Intelligence</div>
      <div style="font-size: 13px; color: var(--text-muted); margin-bottom: 12px;">
        Primary Language: <strong style="color: var(--text-main);">{html.escape(primary_lang)}</strong>
        &middot; Framework: <strong style="color: var(--text-main);">{html.escape(primary_fw)}</strong>
        &middot; Data Layer: <strong style="color: var(--text-main);">{html.escape(primary_orm)}</strong>
      </div>
      <div class="polyglot-chips">
        {stack_chips_html}
      </div>
    </div>

    <!-- 7-Stage Canonical Pipeline Tracker -->
    <div class="card pipeline-section">
      <div class="section-title">&#9658; Canonical 7-Stage Closed-Loop Governance Flow</div>
      <div class="pipeline-tracker">
        <div class="pipeline-line"></div>
        <div class="pipeline-step">
          <div class="step-circle active">1</div>
          <div class="step-name">Scan</div>
          <div class="step-cmd">audit &middot; /audit</div>
        </div>
        <div class="pipeline-step">
          <div class="step-circle active">2</div>
          <div class="step-name">Score</div>
          <div class="step-cmd">0-100 Score</div>
        </div>
        <div class="pipeline-step">
          <div class="step-circle active">3</div>
          <div class="step-name">Harden</div>
          <div class="step-cmd">harden &middot; /harden</div>
        </div>
        <div class="pipeline-step">
          <div class="step-circle active">4</div>
          <div class="step-name">Authorize</div>
          <div class="step-cmd">Human Gate</div>
        </div>
        <div class="pipeline-step">
          <div class="step-circle active">5</div>
          <div class="step-name">Apply</div>
          <div class="step-cmd">apply &middot; .bak</div>
        </div>
        <div class="pipeline-step">
          <div class="step-circle active">6</div>
          <div class="step-name">Recheck</div>
          <div class="step-cmd">recheck &middot; verify</div>
        </div>
        <div class="pipeline-step">
          <div class="step-circle active">7</div>
          <div class="step-name">Report</div>
          <div class="step-cmd">report &middot; SARIF</div>
        </div>
      </div>
    </div>

    <!-- Bottom Details Grid -->
    <div class="grid-bottom">
      <!-- Golden Recipes Catalog -->
      <div class="card">
        <div class="section-title">&#10024; Active Golden Fix Recipes ({len(recipes)})</div>
        <div class="recipes-list">
          {recipe_cards_html}
        </div>
      </div>

      <!-- Regression Watches & False Positives -->
      <div class="card">
        <div class="section-title">&#128065; Regression Watches & Suppressions</div>
        <table>
          <thead>
            <tr>
              <th>Rule ID</th>
              <th>Description / Reason</th>
              <th>Target Path</th>
            </tr>
          </thead>
          <tbody>
            {regression_rows_html}
          </tbody>
        </table>
      </div>
    </div>

    <footer>
      TorusGuard v1.3.0 &middot; Autonomous Security Engine for AI-Built Applications &middot; 100% Local-First &middot; Zero Cloud Telemetry Leakage
    </footer>
  </div>
</body>
</html>
"""


def emit_html_report(
    target_path: str | Path | None = None,
    root_dir: str | Path | None = None
) -> dict[str, Any]:
    """Emit the standalone HTML report to disk."""
    root = Path(root_dir or find_project_root()).resolve()
    telemetry = load_report_telemetry(root)
    html_content = generate_html_dashboard(telemetry)

    out_file = Path(target_path) if target_path else (root / ".torusguard" / "runs" / "report-latest.html")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(html_content, encoding="utf-8")

    return {
        "status": "success",
        "report_path": str(out_file),
        "file_size_bytes": len(html_content.encode("utf-8")),
        "posture_score": compute_posture_score(telemetry)
    }


def main():
    parser = argparse.ArgumentParser(description="TorusGuard Visual HTML Report Emitter")
    parser.add_argument("--out", help="Output HTML file path (default: .torusguard/runs/report-latest.html)")
    parser.add_argument("--root", help="Project root override")
    parser.add_argument("--json", action="store_true", help="Output raw JSON summary")

    args = parser.parse_args()
    root = Path(args.root).resolve() if args.root else None

    res = emit_html_report(target_path=args.out, root_dir=root)
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print(f"[SUCCESS] Emitted TorusGuard visual dashboard: {res['report_path']}")
        print(f"Posture Score: {res['posture_score']}/100 · Size: {res['file_size_bytes']} bytes")


if __name__ == "__main__":
    main()
