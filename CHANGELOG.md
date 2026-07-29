# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> Note: this changelog was reconstructed from git history. Releases without
> local tag objects are inferred from release merge commits and version bumps.

## Unreleased

### Changed

- `pyproject.toml` cleanup.

### Added

- Stronger code chekers with Ruff+McCabe & Bandit

### Deprecated

- Python `3.7`, `3.8` and `3.9` no longer supported.


## [0.5.0] - 2026-05-29

### Added

- Added the reconstructed project changelog.
- Added missing Click-to-CWL type mappings for integer, float, range, date/time,
  UUID, and unprocessed string parameter types.
- Added regression tests for the supported Click parameter type mappings.
- Added Dependabot configuration for direct Python dependencies.
- Added a Taskfile entry point for shared quality checks.
- Added Hatch-managed test, development, type-checking, and coverage
  configuration.

### Changed

- Switched package version metadata to Hatch dynamic versioning through
  `src/click2cwl/__about__.py` and bumped the package to `0.5.0`.
- Reworked the package GitHub Actions workflow into branch/PR CI and tag-based
  PyPI publishing with tag/version validation.
- Added Ruff format and lint checks to CI, and applied Ruff cleanups across the
  package and tests.
- Refreshed Python package classifiers and the Hatch test matrix for Python
  3.10 through 3.14.
- Limited documentation publishing to documentation-related changes.
- Reorganized contributor metadata in the package configuration.

### Fixed

- Added an explicit error for unsupported Click parameter types instead of
  silently producing an empty CWL type.

## [0.4.0] - 2025-08-22

### Added

- Added support for positional `@click.argument()` parameters when generating
  CWL inputs.
- Added direct documentation for the available CWL exporters.
- Added pytest-based coverage for `CWLParam`, including enum serialization and
  argument handling.

### Changed

- Converted enum symbols to JSON-serializable lists in generated CWL.
- Omitted option prefixes for positional Click arguments in command-line input
  bindings.
- Updated PyPI publishing and documentation GitHub Actions to current action
  versions.
- Added Francis Charette-Migneault to the project contributors.
- Bumped package metadata to version `0.4.0`.

## [0.3.4] - 2025-07-24

### Added

- Added `pyproject.toml` packaging metadata using Hatchling.
- Added a GitHub Actions workflow for building, testing, and publishing package
  distributions.
- Added pytest regression coverage for generated CWL output.

### Changed

- Refreshed Binder, devcontainer, documentation, and test fixture paths for the
  current project layout.
- Expanded `.gitignore` entries for common Python, tooling, and environment
  artifacts.

### Fixed

- Mapped `click.Path(dir_okay=False)` to CWL `File` instead of `Directory`.

## [0.3.3] - 2023-02-07

### Changed

- Represented required enum inputs with a list-wrapped CWL enum schema.
- Deep-copied the generated CommandLineTool and Workflow graph entries to avoid
  YAML anchors in final CWL output.

## [0.3.2] - 2022-09-07

### Added

- Propagated Click default values into generated workflow parameters.
- Added test coverage for default-valued optional parameters.

## [0.3.1] - 2022-06-01

### Added

- Added Click boolean flag support by mapping `click.BoolParamType` to CWL
  `boolean`.
- Added `cwltool` to the devcontainer environment and pinned its Python version.

## [0.3.0] - 2022-01-14

### Added

- Added `--wall-time` handling that emits a CWL `ToolTimeLimit` requirement.
- Added `--cwl-version` handling for overriding the generated CWL version.

### Changed

- Automatically emits CWL `v1.1` when a wall-time limit is requested.
- Updated README usage notes for the new runtime export arguments.

## [0.2.0] - 2022-01-12

### Added

- Added Binder and devcontainer setup for interactive development.
- Added CWL stage-in/stage-out fixtures and test scripts.
- Added git-flow setup for release management.

### Changed

- Improved nullable array handling for optional `multiple=True` Click options in
  generated CommandLineTool inputs.
- Updated README Binder links and development environment documentation.

## [0.1.9] - 2021-05-10

### Added

- Added MkDocs documentation pages for installation and getting started.
- Added a documentation publishing workflow.

## [0.1.8] - 2021-03-09

### Fixed

- Fixed generated CWL for optional array CommandLineTool parameters.

## [0.1.7] - 2021-02-04

### Added

- Added support for Click options declared with `multiple=True`.

### Changed

- Applied Black-style formatting updates across the package.

## [0.1.6] - 2021-01-26

### Fixed

- Removed unwanted debug printing from CWL metadata export.

## [0.1.5] - 2021-01-25

### Added

- Added Schema.org workflow metadata support through `--metadata` arguments.
- Added generated CWL metadata fields for author, organization, and software
  version.

## [0.1.4] - 2021-01-19

### Added

- Added `--to-file` handling for writing generated CWL and parameter files.

### Changed

- Made CWL, CommandLineTool, and parameter exporters print to stdout by default.
- Updated README and example documentation for the export behavior.

## [0.1.3] - 2021-01-12

### Added

- Added conda package import tests for `click2cwl`.

### Changed

- Renamed the Python package from `cwl2click` to `click2cwl`.
- Updated conda recipe imports and build metadata for the renamed package.

## [0.1.2] - 2021-01-12

### Added

- Exported `dump` from the package top-level module.

### Changed

- Reset conda build numbering for the `0.1.2` release.

## [0.1.1] - 2021-01-12

### Fixed

- Fixed `dump()` behavior so generation only runs when `--dump` exports are
  requested.

### Removed

- Removed the legacy `vegetation_index` application module from the package.

## [0.1.0] - 2021-01-12

### Added

- Added the initial Click context to CWL conversion package.
- Added exporters for CWL Workflow documents, CWL CommandLineTool documents, and
  CWL parameter templates.
- Added support for Click `Path`, `File`, string, enum, optional enum, resource,
  Docker, environment variable, and scatter-related metadata when generating CWL.
- Added sample CWL/YAML files, examples, setup metadata, a conda recipe, and CI
  configuration.

### Changed

- Converted the early standalone application work into a reusable Python module.

### Removed

- Removed early Docker and standalone vegetation-index scaffolding that was no
  longer part of the packaged converter.
