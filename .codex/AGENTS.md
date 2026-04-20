# Codex Working Rules For `assemble-x`

This repository is a Godot 4.6 project. Treat `project.godot` as the source of truth for engine version and rendering settings.

## Scope

These rules apply to the entire repository unless a deeper `AGENTS.md` overrides them.

## Project Intent

- Keep the project lightweight and easy to iterate on.
- Prefer changes that preserve a clean Godot project structure over quick one-off hacks.
- Do not introduce external tooling unless the repository already needs it.

## File And Folder Conventions

- Use `snake_case` for Godot file names such as `.gd`, `.tscn`, `.tres`, and `.res`.
- Keep reusable gameplay code grouped by feature or domain, not by broad file type alone.
- Reserve `autoload/` for true global singletons.
- Use `addons/` only for editor or plugin style integrations.
- Keep third-party code isolated under `third_party/`.
- Put temporary experiments in `tests/` or a clearly named prototype scene instead of mixing them into production paths.

## Preferred Folder Structure

Use the structure described in `setting.md` as the default architectural target for new work.

- `autoload/`: global managers that must persist across scenes such as game, audio, save, or routing.
- `core/`: shared foundation code that should stay gameplay-agnostic, including constants, utilities, base classes, systems, and reusable resources.
- `features/`: domain-oriented gameplay modules such as player, combat, enemies, robot parts, progression, stages, and UI.
- `scenes/`: top-level composition and entry scenes such as `main/`, `bootstrap/`, and explicit test scenes.
- `assets/`: imported art, audio, fonts, and VFX kept separate from gameplay logic.
- `data/`: balance data, localization, JSON, and save-related content.
- `tests/`: isolated experiments, test scenes, or automation-related fixtures.
- `docs/`: design notes and technical documentation.
- `third_party/`: vendor or external code that should remain isolated from first-party gameplay code.

## Placement Guidance

- Prefer `features/<feature_name>/` when code belongs to one gameplay domain and may contain its own scenes, scripts, states, and data.
- Prefer `core/` only for code that is intentionally reusable across multiple features.
- Prefer `scenes/` for orchestration scenes, not as a catch-all replacement for feature-local scenes.
- Prefer `Resource` files for structured gameplay data such as stats, item definitions, weapons, enemies, dialogue, or mission config.
- Prefer feature-local assets or data references when ownership is clear, but keep large shared raw assets under `assets/` and shared config under `data/`.

## Editing Rules

- Prefer small, explicit patches over broad refactors.
- Do not manually rewrite `project.godot` unless the task specifically requires engine or project setting changes.
- When adding gameplay code, favor typed GDScript where it improves clarity.
- Avoid creating hidden dependencies between scenes through hard-coded node paths when exported references or composition would be clearer.
- Do not add placeholder assets just to satisfy structure changes unless they are required by the task.

## Validation

- If you change `.codex/` config files, keep `config.toml` valid TOML and `hooks.json` valid JSON.
- If you add or change hook commands, ensure referenced script paths exist inside the repository.
- If you add GDScript or scenes, prefer a targeted syntax or loadability check when a local Godot binary is available.

## Communication

- Summaries should mention user-visible project impact first, then validation status, then any remaining manual checks.
