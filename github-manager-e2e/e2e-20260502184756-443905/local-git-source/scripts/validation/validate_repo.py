#!/usr/bin/env python3
"""Extended repository validation entrypoint for ROS2-Agent."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

REQUIRED_PATHS = [
    ROOT / "README.md",
    ROOT / "README_EN.md",
    ROOT / ".gitignore",
    ROOT / "assets" / "branding" / "ros2-agent-logo.svg",
    ROOT / "LICENSE",
    ROOT / "pytest.ini",
    ROOT / ".github" / "ISSUE_TEMPLATE" / "bug_report.md",
    ROOT / ".github" / "ISSUE_TEMPLATE" / "feature_request.md",
    ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md",
    ROOT / "docs" / "planning" / "开发总日志.md",
    ROOT / "profile" / "ros2-agent" / "SOUL.md",
    ROOT / "profile" / "ros2-agent" / "bootstrap" / "install_profile.sh",
    ROOT / "profile" / "ros2-agent" / "bootstrap" / "init_workspace.sh",
    ROOT / "skills" / "ros2-environment-bootstrap" / "SKILL.md",
    ROOT / "tools" / "ros2_env_audit.py",
    ROOT / "tools" / "ros2_workspace_inspect.py",
    ROOT / "tools" / "colcon_build_summary.py",
    ROOT / "tools" / "ros2_launch_diagnose.py",
    ROOT / "tools" / "ros2_runtime_samples.py",
    ROOT / "tools" / "ros2_graph_inspect.py",
    ROOT / "tools" / "ros2_controller_diagnose.py",
    ROOT / "tools" / "ros2_tf_diagnose.py",
    ROOT / "benchmarks" / "scoring.py",
    ROOT / "tests" / "tools" / "test_ros2_env_audit.py",
    ROOT / "tests" / "tools" / "test_ros2_workspace_inspect.py",
    ROOT / "tests" / "tools" / "test_colcon_build_summary.py",
    ROOT / "tests" / "tools" / "test_ros2_launch_diagnose.py",
    ROOT / "tests" / "tools" / "test_ros2_graph_inspect.py",
    ROOT / "tests" / "tools" / "test_ros2_controller_diagnose.py",
    ROOT / "tests" / "tools" / "test_ros2_tf_diagnose.py",
    ROOT / "tests" / "workflows" / "test_runtime_extended_fixtures.py",
    ROOT / "tests" / "workflows" / "test_demo_assets.py",
    ROOT / "tests" / "workflows" / "test_benchmark_fixtures.py",
    ROOT / "tests" / "workflows" / "test_launch_fixtures.py",
    ROOT / "tests" / "workflows" / "test_scoring_and_reporting.py",
    ROOT / "benchmarks" / "fixtures" / "sample_colcon_failure.log",
    ROOT / "benchmarks" / "fixtures" / "sample_colcon_success.log",
    ROOT / "benchmarks" / "fixtures" / "sample_colcon_dependency_failure.log",
    ROOT / "benchmarks" / "fixtures" / "sample_colcon_interface_failure.log",
    ROOT / "benchmarks" / "fixtures" / "runtime_graph_sample.json",
    ROOT / "benchmarks" / "fixtures" / "runtime_health_sample.json",
    ROOT / "benchmarks" / "fixtures" / "tf_chain_missing.json",
    ROOT / "benchmarks" / "fixtures" / "controller_unconfigured.json",
    ROOT / "benchmarks" / "fixtures" / "launch_missing_params" / "README.md",
    ROOT / "benchmarks" / "fixtures" / "launch_missing_launch_file" / "README.md",
    ROOT / "benchmarks" / "fixtures" / "launch_complete" / "README.md",
    ROOT / "benchmarks" / "fixtures" / "launch_missing_asset" / "README.md",
    ROOT / "benchmarks" / "fixtures" / "launch_runtime_failure_hint" / "README.md",
    ROOT / "examples" / "demo_workspace" / "demo_ws" / "src" / "demo_nodes" / "package.xml",
    ROOT / "examples" / "broken_cases" / "broken_ws_missing_package_xml" / "src" / "broken_nodes" / "setup.py",
    ROOT / "scripts" / "validation" / "run_phase2_validation.sh",
    ROOT / "scripts" / "validation" / "run_demo_pipeline.sh",
    ROOT / "scripts" / "validation" / "generate_benchmark_report.py",
    ROOT / "scripts" / "validation" / "run_reporting_pipeline.sh",
    ROOT / "scripts" / "validation" / "export_latest_report.sh",
    ROOT / "scripts" / "validation" / "run_full_quality_gate.sh",
    ROOT / "examples" / "transcripts" / "transcript_011_profile_bootstrap_install.md",
    ROOT / "tests" / "workflows" / "test_bootstrap_workspace.py",
    ROOT / "tests" / "workflows" / "test_profile_install.py",
    ROOT / "profile" / "ros2-agent" / "bootstrap" / "README.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / "CODE_OF_CONDUCT.md",
    ROOT / "SECURITY.md",
    ROOT / "SUPPORT.md",
    ROOT / "pyproject.toml",
    ROOT / "requirements-dev.txt",
    ROOT / ".pre-commit-config.yaml",
    ROOT / "Makefile",
    ROOT / "CODEOWNERS",
    ROOT / ".github" / "workflows" / "ci.yml",
    ROOT / ".github" / "workflows" / "release-readiness.yml",
    ROOT / ".github" / "dependabot.yml",
    ROOT / "docs" / "00_overview" / "quickstart.md",
    ROOT / "docs" / "00_overview" / "developer-setup.md",
    ROOT / "docs" / "00_overview" / "versioning-and-compatibility.md",
    ROOT / "docs" / "00_overview" / "faq.md",
    ROOT / "docs" / "00_overview" / "github_upload_final_checklist.md",
    ROOT / "docs" / "01_architecture" / "hermes_integration_contract.md",
    ROOT / "docs" / "02_product" / "capability_matrix.md",
    ROOT / "docs" / "02_product" / "teaching_capability_strategy.md",
    ROOT / "docs" / "04_benchmarks" / "benchmark_evaluation_protocol.md",
    ROOT / "docs" / "05_roadmap" / "ros2_learning_track.md",
    ROOT / "docs" / "planning" / "NEXT_STAGE_DEVELOPMENT_BLUEPRINT.md",
    ROOT / "benchmarks" / "reports" / "benchmark_scorecard_template.md",
    ROOT / "examples" / "transcripts" / "transcript_012_hermes_profile_first_run.md",
    ROOT / "examples" / "transcripts" / "transcript_013_ros2_workspace_diagnose_session.md",
    ROOT / "examples" / "transcripts" / "transcript_014_launch_debug_session.md",
    ROOT / "skills" / "ros2-runtime-debug-teaching" / "SKILL.md",
    ROOT / "skills" / "ros2-launch-reasoning-coach" / "SKILL.md",
    ROOT / "scripts" / "validation" / "render_markdown_report.py",
    ROOT / "Dockerfile",
    ROOT / ".devcontainer" / "devcontainer.json",
]


def main() -> None:
    missing = [str(p) for p in REQUIRED_PATHS if not p.exists()]
    if missing:
        print("Missing required paths:")
        for item in missing:
            print(f"- {item}")
        raise SystemExit(1)
    print("ROS2-Agent repository validation passed.")


if __name__ == "__main__":
    main()
