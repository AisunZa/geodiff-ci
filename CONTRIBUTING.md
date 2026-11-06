# Contributing to GeoDiff CI

Thank you for your interest in improving **GeoDiff CI**! Contributions that make geospatial data validation more reliable, understandable, and easier to use are welcome.

GeoDiff CI is a Python command-line tool for detecting changes in geospatial datasets, including feature counts, schemas, coordinate reference systems (CRS), geometry validity, and bounding-box coverage.

## Ways to contribute

- Report a reproducible bug or confusing error message.
- Improve documentation, examples, or installation instructions.
- Add tests for edge cases, especially geometry, CRS, and data-quality checks.
- Propose a focused improvement to the CLI or regression reports.

For a first contribution, check the repository's [Issues](https://github.com/AisunZa/geodiff-ci/issues) for tasks labeled `good first issue` or `help wanted`.

## Before opening an issue

Please check the [README](README.md) and existing issues first. When reporting a bug, include:

1. The command you ran and what you expected to happen.
2. What actually happened, including error output when relevant.
3. Your Python version, operating system, and relevant package versions.
4. A **small synthetic or publicly shareable dataset** that reproduces the problem, if possible. Do not upload private or sensitive geospatial data.

For feature requests, explain the use case, the intended behavior, and any compatibility concerns. For larger changes, open an issue to discuss the approach before writing code.

## Local development setup

GeoDiff CI requires **Python 3.11 or newer**. Fork the repository using GitHub, then clone your fork:

```bash
git clone https://github.com/YOUR-USERNAME/geodiff-ci.git
cd geodiff-ci
python -m venv .venv
```

Activate the environment:

**Linux/macOS**

```bash
source .venv/bin/activate
```

**Windows PowerShell**

```powershell
.venv\Scripts\Activate.ps1
```

Install the package with development dependencies:

```bash
python -m pip install -e ".[dev]"
```

Run the tests and CLI smoke checks:

```bash
pytest -v
geodiff version
geodiff compare examples/baseline.geojson examples/candidate.geojson --max-feature-loss 50
```

**Note:** The sample candidate dataset deliberately loses 50% of the baseline features. The default comparison, *without* `--max-feature-loss 50`, is expected to report a regression and exit with status `1`.

## Making a change

1. Create a branch in your fork, for example `docs/improve-examples` or `fix/crs-edge-case`.
2. Make one focused change per pull request where practical.
3. Add or update tests in `tests/` when changing behavior. Keep test datasets small and reproducible.
4. Update the README or examples when behavior, flags, or supported usage changes.
5. Run `pytest -v` before submitting. Check that relevant CLI examples still work.
6. Do not add credentials, sensitive data, or large generated files to the repository.

## Opening a pull request

Open a pull request from your fork's branch into `AisunZa/geodiff-ci` on `main`.

In the description, include:

- **Why** the change is useful and what it does.
- Any related issue number (for example, `Closes #123` only when the PR fully resolves it).
- How you tested it, including commands and results.
- Notes about changed behavior, limitations, or documentation.

GitHub Actions runs the project's tests on Python **3.11, 3.12, and 3.13**. Please address relevant failed checks and review comments before the PR is merged. A pull request is not guaranteed to be merged; changes are reviewed for project fit, correctness, and maintainability.

## Collaboration

Be respectful and constructive in issue discussions, reviews, and pull requests. Assume good intent, focus feedback on the work, and give others time to respond. Do not post private information or security credentials in public issues.

Thank you for helping improve geospatial data quality tooling!
