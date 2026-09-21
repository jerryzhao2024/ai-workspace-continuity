#!/usr/bin/env python3
"""Audit a project workspace for durable, model-agnostic AI continuity."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "dist",
    "build",
    "target",
}

SECRET_NAMES = {
    ".env",
    ".npmrc",
    ".pypirc",
    "credentials",
    "credentials.json",
    "id_dsa",
    "id_ecdsa",
    "id_ed25519",
    "id_rsa",
    "kubeconfig",
    "secrets.json",
    "secrets.yaml",
    "secrets.yml",
}

SECRET_SUFFIXES = {
    ".key",
    ".p12",
    ".pfx",
    ".pem",
    ".tfstate",
}

PUBLIC_CERT_NAMES = {
    "cacert.pem",
    "ca-bundle.pem",
    "certifi.pem",
}



def run_git(root: Path, *args: str) -> tuple[bool, str]:
    try:
        proc = subprocess.run(
            ["git", "-C", str(root), *args],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except FileNotFoundError:
        return False, "git executable not found"
    output = (proc.stdout or proc.stderr).strip()
    return proc.returncode == 0, output


def is_secret_candidate(name: str) -> bool:
    lowered = name.lower()
    if lowered in PUBLIC_CERT_NAMES:
        return False
    if lowered in SECRET_NAMES:
        return True
    if lowered.startswith(".env.") and lowered != ".env.example":
        return True
    return Path(lowered).suffix in SECRET_SUFFIXES


def inspect_files(root: Path, large_bytes: int, max_files: int) -> dict[str, Any]:
    secret_paths: list[str] = []
    large_files: list[dict[str, Any]] = []
    scanned = 0
    truncated = False

    for current, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            if scanned >= max_files:
                truncated = True
                break
            scanned += 1
            path = Path(current) / name
            try:
                rel = path.relative_to(root).as_posix()
            except ValueError:
                rel = str(path)
            if is_secret_candidate(name):
                if len(secret_paths) < 100:
                    secret_paths.append(rel)
            try:
                size = path.stat().st_size
            except OSError:
                continue
            if size >= large_bytes:
                large_files.append({"path": rel, "bytes": size})
        if truncated:
            break

    large_files.sort(key=lambda item: item["bytes"], reverse=True)
    return {
        "scanned_files": scanned,
        "scan_truncated": truncated,
        "secret_candidate_count": len(secret_paths),
        "secret_candidates": secret_paths,
        "large_file_count": len(large_files),
        "large_files": large_files[:30],
    }


def audit(root: Path, large_mb: float, max_files: int) -> dict[str, Any]:
    if not root.exists():
        raise FileNotFoundError(f"Workspace does not exist: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"Workspace is not a directory: {root}")

    expected = {
        "README.md": (root / "README.md").is_file(),
        "AGENTS.md": (root / "AGENTS.md").is_file(),
        "CLAUDE.md": (root / "CLAUDE.md").is_file(),
        "AI_History/": (root / "AI_History").is_dir(),
        ".gitignore": (root / ".gitignore").is_file(),
        "docs/": (root / "docs").is_dir(),
    }

    git_ok, git_output = run_git(root, "rev-parse", "--show-toplevel")
    git_status = "not_repository"
    git_root = None
    if git_ok:
        git_status = "ok"
        git_root = git_output
    elif (root / ".git").exists() and (root / ".git").is_dir():
        if not (root / ".git" / "HEAD").exists():
            git_status = "broken_or_empty_git_dir"

    history_dir = root / "AI_History"
    record_count = 0
    if history_dir.is_dir():
        record_count = sum(
            1
            for path in history_dir.glob("*.md")
            if path.name.lower() != "readme.md"
        )

    claude_path = root / "CLAUDE.md"
    claude_mentions_agents = False
    if claude_path.is_file():
        try:
            text = claude_path.read_text(encoding="utf-8", errors="replace")
            claude_mentions_agents = "AGENTS.md" in text
        except OSError:
            pass

    file_scan = inspect_files(root, int(large_mb * 1024 * 1024), max_files)

    recommendations: list[str] = []
    if git_status == "broken_or_empty_git_dir":
        recommendations.append(
            "The root .git directory is empty or malformed. Verify it contains no usable history before removing or repairing it; do not initialize a new repository over the whole root until the repository boundary and sensitive-data rules are decided."
        )
    elif git_status == "not_repository":
        recommendations.append(
            "This directory is not a Git repository. Choose a code/knowledge repository boundary first; do not initialize one repository over a data-heavy mixed-purpose root by default."
        )

    labels = {
        "README.md": "Create a human entry point describing purpose, status, structure, run steps, and unresolved issues.",
        "AGENTS.md": "Create canonical agent instructions covering scope, constraints, tests, data rules, and forbidden changes.",
        ".gitignore": "Create ignore rules for secrets, local session state, generated artifacts, and intentionally external data.",
        "AI_History/": "Create a decision-record location when the first durable decision or non-obvious problem is resolved.",
    }
    for key, message in labels.items():
        if not expected[key]:
            recommendations.append(message)

    if expected["CLAUDE.md"] and not claude_mentions_agents:
        recommendations.append(
            "CLAUDE.md exists but does not point to AGENTS.md. Prefer one canonical instructions file and make the other a short pointer to avoid drift."
        )
    if expected["AI_History/"] and record_count == 0:
        recommendations.append(
            "AI_History/ has no records yet. Add one after a meaningful decision or debugging resolution; do not create empty records merely to improve a checklist."
        )
    if file_scan["secret_candidate_count"]:
        recommendations.append(
            "Potential secret-bearing files were found. Confirm they are excluded from Git and external uploads before any commit, push, or model call."
        )
    if file_scan["large_file_count"]:
        recommendations.append(
            "Large files were found. Decide whether they belong in Git, an external asset store, or a generated-output policy; record the storage decision."
        )

    severity = "ok"
    if git_status != "ok" or file_scan["secret_candidate_count"]:
        severity = "high"
    elif not all(expected[key] for key in ("README.md", "AGENTS.md", ".gitignore", "AI_History/")):
        severity = "medium"
    elif recommendations:
        severity = "low"

    return {
        "workspace": str(root),
        "severity": severity,
        "git": {
            "status": git_status,
            "root": git_root,
        },
        "expected": expected,
        "ai_history_record_count": record_count,
        "claude_mentions_agents": claude_mentions_agents,
        "file_scan": file_scan,
        "recommendations": recommendations,
    }


def print_human(result: dict[str, Any]) -> None:
    print(f"Workspace: {result['workspace']}")
    print(f"Severity: {result['severity']}")
    print(f"Git: {result['git']['status']}")
    print("Expected:")
    for name, present in result["expected"].items():
        print(f"  {'OK' if present else 'MISSING':<7} {name}")
    print(f"AI_History records: {result['ai_history_record_count']}")
    scan = result["file_scan"]
    print(f"Files scanned: {scan['scanned_files']}")
    print(f"Secret candidates: {scan['secret_candidate_count']}")
    print(f"Large files: {scan['large_file_count']}")
    if result["recommendations"]:
        print("Recommendations:")
        for item in result["recommendations"]:
            print(f"  - {item}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default=".", help="Workspace root")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    parser.add_argument(
        "--large-mb",
        type=float,
        default=100.0,
        help="Report files at or above this size in MiB (default: 100)",
    )
    parser.add_argument(
        "--max-files",
        type=int,
        default=20000,
        help="Maximum files to inspect before stopping the scan",
    )
    parser.add_argument(
        "--fail-on-high",
        action="store_true",
        help="Exit with status 2 when severity is high",
    )
    args = parser.parse_args()

    try:
        result = audit(Path(args.path).expanduser().resolve(), args.large_mb, args.max_files)
    except (FileNotFoundError, NotADirectoryError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(result, ensure_ascii=True, indent=2))
    else:
        print_human(result)

    if args.fail_on_high and result["severity"] == "high":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
