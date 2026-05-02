import json
from pathlib import Path

from benchmarks.scoring import (
    score_expected_value,
    score_next_actions,
    score_required_strings,
    score_weighted_sections,
)
from tools.colcon_build_summary import summarize_build_log_file
from tools.ros2_launch_diagnose import diagnose_launch
from tools.ros2_runtime_samples import (
    ControllerSummary,
    NodeSummary,
    TfSummary,
    TopicSummary,
    build_runtime_graph_summary,
    build_runtime_health_summary,
)

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_score_required_strings_partial_match():
    result = score_required_strings("alpha beta", ["alpha", "gamma"], max_score=1.0)
    assert result["passed"] is False
    assert result["score"] == 0.5
    assert result["matched"] == ["alpha"]


def test_score_expected_value_basic():
    result = score_expected_value({"recommended_next_step": "build_workspace"}, "recommended_next_step", "build_workspace")
    assert result["passed"] is True
    assert result["score"] == 1.0


def test_score_next_actions_basic():
    result = score_next_actions(["retry_failed_packages", "recheck_environment"], ["retry_failed_packages"])
    assert result["passed"] is True
    assert result["score"] == 1.0


def test_score_weighted_sections_basic():
    result = score_weighted_sections([
        ("facts", 0.4, True),
        ("classification", 0.3, True),
        ("next_actions", 0.3, False),
    ])
    assert result["passed"] is False
    assert result["score"] == 0.7


def test_dependency_failure_fixture_classification():
    log_path = REPO_ROOT / "benchmarks" / "fixtures" / "sample_colcon_dependency_failure.log"
    result = summarize_build_log_file(str(log_path))
    assert result["failed_packages"]
    assert result["failed_packages"][0]["error_category"] in {"dependency", "cmake/configure"}


def test_launch_runtime_failure_hint_fixture():
    fixture = REPO_ROOT / "benchmarks" / "fixtures" / "launch_runtime_failure_hint"
    result = diagnose_launch(
        package_name="demo_nodes",
        launch_file="demo.launch.py",
        package_prefix=str(fixture / "install" / "demo_nodes"),
        params_files=[str(fixture / "install" / "demo_nodes" / "share" / "demo_nodes" / "config" / "demo_params.yaml")],
        referenced_assets=[str(fixture / "assets" / "demo.urdf")],
        runtime_return_code=1,
    )
    assert "runtime_probe_failed" in result["root_cause_candidates"]
    assert "collect_runtime_logs" in result["next_actions"]


def test_runtime_sample_builders():
    graph = build_runtime_graph_summary(
        nodes=[NodeSummary(name="talker", namespace="/demo", publishers=1, subscribers=0)],
        topics=[TopicSummary(name="/chatter", msg_type="std_msgs/msg/String", publisher_count=1, subscriber_count=1)],
        next_actions=["inspect_runtime_health"],
    )
    health = build_runtime_health_summary(
        controllers=[ControllerSummary(name="arm_controller", state="inactive", claimed_interfaces=6)],
        tf=TfSummary(frame_count=4, stale_frames=["tool0"]),
        next_actions=["inspect_controller_manager"],
    )
    assert graph["nodes"][0]["name"] == "talker"
    assert health["controllers"][0]["state"] == "inactive"
    assert health["tf"]["stale_frames"] == ["tool0"]
