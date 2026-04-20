#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
CODEX_DIR = REPO_ROOT / ".codex"


def validate_json(path: Path) -> None:
    with path.open("r", encoding="utf-8") as handle:
        json.load(handle)


TABLE_RE = re.compile(r"^\[(?P<name>[A-Za-z0-9_.\"/\-]+)\]$")
KEY_VALUE_RE = re.compile(r"^(?P<key>[A-Za-z0-9_.\-]+)\s*=\s*(?P<value>.+)$")


def _is_quoted(value: str) -> bool:
    return len(value) >= 2 and value[0] == '"' and value[-1] == '"'


def validate_toml(path: Path) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()

    for line_number, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        if TABLE_RE.match(line):
            continue

        match = KEY_VALUE_RE.match(line)
        if not match:
            raise ValueError(f"line {line_number}: unsupported TOML syntax: {raw_line}")

        value = match.group("value").strip()
        if _is_quoted(value):
            continue
        if value in {"true", "false"}:
            continue
        if re.fullmatch(r"[0-9]+", value):
            continue
        raise ValueError(f"line {line_number}: unsupported TOML value: {value}")


def validate_hook_commands(path: Path) -> list[str]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    errors: list[str] = []
    hooks = data.get("hooks", {})
    for event_name, entries in hooks.items():
        if not isinstance(entries, list):
            errors.append(f"{event_name} must be a list")
            continue

        for entry in entries:
            for hook in entry.get("hooks", []):
                if hook.get("type") != "command":
                    continue

                command = hook.get("command", "")
                if not command:
                    errors.append(f"{event_name} contains an empty command hook")
                    continue

                tokens = command.split()
                candidate = next((token for token in tokens if token.startswith("./")), None)
                if candidate is None:
                    continue

                target = (REPO_ROOT / candidate[2:]).resolve()
                if not target.exists():
                    errors.append(f"Missing hook target: {candidate}")

    return errors


def main() -> int:
    config_path = CODEX_DIR / "config.toml"
    hooks_path = CODEX_DIR / "hooks.json"

    errors: list[str] = []

    try:
        validate_toml(config_path)
    except Exception as exc:  # pragma: no cover
        errors.append(f"Invalid TOML in {config_path}: {exc}")

    try:
        validate_json(hooks_path)
    except Exception as exc:  # pragma: no cover
        errors.append(f"Invalid JSON in {hooks_path}: {exc}")
    else:
        errors.extend(validate_hook_commands(hooks_path))

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("Codex config validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
