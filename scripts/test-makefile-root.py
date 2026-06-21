#!/usr/bin/env python3
"""Exercise Makefile root resolution against hostile variable overrides."""

from pathlib import Path
import os
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
TARGETS = (
    "build",
    "check",
    "lint",
    "root-test",
    "settings-test",
    "static-check",
    "test",
    "url-test",
    "verify",
)
ATTACKER_ROOT = "/tmp/playlist-attacker-root"


def run_make(makefile, target, *arguments, environment=None):
    command = [
        "make",
        "--no-print-directory",
        "--dry-run",
        "--file",
        str(makefile),
        *arguments,
        target,
    ]
    return subprocess.run(
        command,
        cwd=makefile.parent.parent,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )


def assert_safe_plan(result, expected_root, scenario, target):
    output = result.stdout + result.stderr
    if result.returncode != 0:
        raise AssertionError(
            f"{scenario} {target} failed with {result.returncode}:\n{output}"
        )
    if str(expected_root) not in output:
        raise AssertionError(
            f"{scenario} {target} did not use {expected_root}:\n{output}"
        )
    if ATTACKER_ROOT in output:
        raise AssertionError(
            f"{scenario} {target} accepted attacker root: {output}"
        )


def main():
    with tempfile.TemporaryDirectory(prefix="Playlist's [quality gate] ") as temp:
        checkout = Path(temp) / "exact head"
        checkout.mkdir()
        makefile = checkout / "Makefile"
        shutil.copy2(ROOT / "Makefile", makefile)

        scenarios = (
            ("default", (), None),
            ("command override", (f"REPO_ROOT={ATTACKER_ROOT}",), None),
            (
                "environment override",
                (),
                {**os.environ, "REPO_ROOT": ATTACKER_ROOT},
            ),
        )
        for scenario, arguments, environment in scenarios:
            for target in TARGETS:
                result = run_make(
                    makefile,
                    target,
                    *arguments,
                    environment=environment,
                )
                assert_safe_plan(result, checkout.resolve(), scenario, target)

        for scenario, arguments, environment in (
            ("command MAKEFILE_LIST override", ("MAKEFILE_LIST=/tmp/untrusted",), None),
            (
                "environment MAKEFILE_LIST override",
                ("--environment-overrides",),
                {**os.environ, "MAKEFILE_LIST": "/tmp/untrusted"},
            ),
        ):
            result = run_make(
                makefile,
                "check",
                *arguments,
                environment=environment,
            )
            output = result.stdout + result.stderr
            if (
                result.returncode == 0
                or "MAKEFILE_LIST must not be overridden" not in output
            ):
                raise AssertionError(f"{scenario} did not fail closed:\n{output}")

    print(
        "Makefile root tests passed: 27 target/override cases and "
        "2 MAKEFILE_LIST rejection cases"
    )


if __name__ == "__main__":
    main()
