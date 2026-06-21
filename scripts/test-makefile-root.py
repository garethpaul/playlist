#!/usr/bin/env python3
"""Exercise Makefile root resolution and caller-controlled authority inputs."""

from pathlib import Path
import os
import shlex
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
PYTHON_STUBS = (
    "scripts/check-baseline.py",
    "scripts/test-makefile-root.py",
    "test_settings_security.py",
    "test_views_normalization.py",
    "test_url_patterns.py",
)


def run_make(
    makefile,
    target,
    *arguments,
    environment=None,
    earlier_makefiles=(),
):
    command = ["make", "--no-print-directory"]
    for earlier_makefile in earlier_makefiles:
        command.extend(("--file", str(earlier_makefile)))
    command.extend(("--file", str(makefile), *arguments, target))
    return subprocess.run(
        command,
        cwd=makefile.parent.parent,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )


def write_python_stub(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "from pathlib import Path\nprint(Path(__file__).resolve())\n",
        encoding="utf-8",
    )


def prepare_checkout(checkout):
    checkout.mkdir()
    makefile = checkout / "Makefile"
    shutil.copy2(ROOT / "Makefile", makefile)
    for relative_path in PYTHON_STUBS:
        write_python_stub(checkout / relative_path)
    return makefile


def assert_safe_execution(
    result,
    expected_root,
    scenario,
    target,
    forbidden_values=(),
):
    output = result.stdout + result.stderr
    if result.returncode != 0:
        raise AssertionError(
            f"{scenario} {target} failed with {result.returncode}:\n{output}"
        )
    if str(expected_root) not in output:
        raise AssertionError(
            f"{scenario} {target} did not execute from {expected_root}:\n{output}"
        )
    for forbidden_value in (ATTACKER_ROOT, *forbidden_values):
        if forbidden_value in output:
            raise AssertionError(
                f"{scenario} {target} accepted {forbidden_value}:\n{output}"
            )


def assert_rejected(result, scenario, expected_message):
    output = result.stdout + result.stderr
    if result.returncode == 0 or expected_message not in output:
        raise AssertionError(f"{scenario} did not fail closed:\n{output}")


def main():
    with tempfile.TemporaryDirectory(prefix="Playlist's [quality gate] ") as temp:
        temp_root = Path(temp)
        checkout = temp_root / 'exact  head [x] "double" `touch make-root-injected`'
        makefile = prepare_checkout(checkout)
        fake_shell = temp_root / "attacker-shell"
        shell_marker = temp_root / "shell-ran"
        fake_shell.write_text(
            "#!/bin/sh\n"
            f"/usr/bin/touch {shlex.quote(str(shell_marker))}\n"
            'exec /bin/sh "$@"\n',
            encoding="utf-8",
        )
        fake_shell.chmod(0o755)
        fake_python = temp_root / "attacker-python"
        python_marker = temp_root / "python-ran"
        fake_python.write_text(
            "#!/bin/sh\n"
            f"/usr/bin/touch {shlex.quote(str(python_marker))}\n"
            "exit 97\n",
            encoding="utf-8",
        )
        fake_python.chmod(0o755)

        scenarios = (
            ("default", (), None, ()),
            ("command ROOT override", (f"REPO_ROOT={ATTACKER_ROOT}",), None, ()),
            (
                "environment ROOT override",
                ("--environment-overrides",),
                {**os.environ, "REPO_ROOT": ATTACKER_ROOT},
                (),
            ),
            (
                "command SHELL override",
                (f"SHELL={fake_shell}",),
                None,
                (str(fake_shell),),
            ),
            (
                "environment SHELL override",
                ("--environment-overrides",),
                {**os.environ, "SHELL": str(fake_shell)},
                (str(fake_shell),),
            ),
            (
                "command shell flags override",
                (".SHELLFLAGS=--invalid",),
                None,
                ("--invalid",),
            ),
            (
                "environment shell flags override",
                ("--environment-overrides",),
                {**os.environ, ".SHELLFLAGS": "--invalid"},
                ("--invalid",),
            ),
            (
                "command PYTHON override",
                (f"PYTHON={fake_python}",),
                None,
                (str(fake_python),),
            ),
            (
                "environment PYTHON override",
                ("--environment-overrides",),
                {**os.environ, "PYTHON": str(fake_python)},
                (str(fake_python),),
            ),
        )
        for scenario, arguments, environment, forbidden_values in scenarios:
            for target in TARGETS:
                result = run_make(
                    makefile,
                    target,
                    *arguments,
                    environment=environment,
                )
                assert_safe_execution(
                    result,
                    checkout.resolve(),
                    scenario,
                    target,
                    forbidden_values,
                )

        if shell_marker.exists() or python_marker.exists():
            raise AssertionError("caller-controlled shell or Python executed")
        if (temp_root / "make-root-injected").exists():
            raise AssertionError("backticks in the checkout path executed")

        for scenario, arguments, environment in (
            ("command MAKEFILE_LIST override", ("MAKEFILE_LIST=/tmp/untrusted",), None),
            (
                "environment MAKEFILE_LIST override",
                ("--environment-overrides",),
                {**os.environ, "MAKEFILE_LIST": "/tmp/untrusted"},
            ),
        ):
            assert_rejected(
                run_make(makefile, "check", *arguments, environment=environment),
                scenario,
                "MAKEFILE_LIST must not be overridden",
            )

        preload = temp_root / "preload.mk"
        preload.write_text("PRELOADED := yes\n", encoding="utf-8")
        for scenario, arguments, environment in (
            ("command MAKEFILES override", (f"MAKEFILES={preload}",), None),
            (
                "environment MAKEFILES override",
                ("--environment-overrides",),
                {**os.environ, "MAKEFILES": str(preload)},
            ),
        ):
            assert_rejected(
                run_make(makefile, "check", *arguments, environment=environment),
                scenario,
                "MAKEFILES must not be set",
            )

        earlier_makefile = temp_root / "earlier.mk"
        earlier_makefile.write_text("EARLIER_MAKEFILE := yes\n", encoding="utf-8")
        result = run_make(
            makefile,
            "check",
            earlier_makefiles=(earlier_makefile,),
        )
        assert_safe_execution(
            result,
            checkout.resolve(),
            "earlier explicit Makefile",
            "check",
        )

    print(
        "Makefile root tests passed: 81 executable target/override cases, "
        "4 rejected automatic-variable/preload cases, and 1 earlier-Makefile case"
    )


if __name__ == "__main__":
    main()
