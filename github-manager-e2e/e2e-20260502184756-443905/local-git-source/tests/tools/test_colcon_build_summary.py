import json
from pathlib import Path

from tools.colcon_build_summary import FailedPackage, build_colcon_summary_result, summarize_build_log


def test_build_colcon_summary_result_failure_case():
    result = build_colcon_summary_result(
        workspace_root="/tmp/ws",
        command="colcon build",
        return_code=1,
        packages_total=2,
        packages_succeeded=1,
        failed_packages=[
            FailedPackage(
                package="bad_pkg",
                stage="compile",
                error_category="dependency",
                headline="missing include",
                evidence_lines=["fatal error: x.hpp"],
                suggested_fix="check dependency declarations",
            )
        ],
    )
    assert result["success"] is False
    assert result["packages_failed"] == 1
    assert result["failed_packages"][0]["package"] == "bad_pkg"
    json.dumps(result)


def test_summarize_build_log_detects_failed_package_and_actions():
    log_text = """
Starting >>> ok_pkg
Finished <<< ok_pkg [0.50s]
Starting >>> bad_pkg
/path/file.cpp:1:10: fatal error: missing.hpp: No such file or directory
Failed   << bad_pkg [1.23s, exited with code 1]
"""
    result = summarize_build_log(log_text, workspace_root="/tmp/ws")
    assert result["packages_failed"] == 1
    assert result["failed_packages"][0]["package"] == "bad_pkg"
    assert result["failed_packages"][0]["error_category"] in {"compile/cpp", "dependency"}
    assert "retry_failed_packages" in result["next_actions"]
