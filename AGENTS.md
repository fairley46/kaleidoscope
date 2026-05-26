# AGENTS.md

Agent contract for `kaleidoscope`. Follows the agentskills.io standard.

## What this repo is

Public local-first pre-decision review tool for engineering leaders. Markdown in, markdown out. Pressure-tests judgment via multiple lenses; never automates the decision itself.

## Tasks welcomed

- New lens definitions (with Brad's approval on which lens taxonomy bucket)
- Decision-artifact template improvements
- Bug fixes in lens-rotation flow
- Documentation in `docs/`
- Test additions

## Tasks refused (hard constraints)

- **Never commit secrets** — block `.env*`, `*.key`, `*.pem`.
- **Never make the tool produce binary outputs** ("just do X"). Kaleidoscope produces structured-uncertainty artifacts; the call stays with the leader.
- **Never add cloud dependencies.** Local-first is a product constraint, not a phase-1 limit.
- **Never push to `main` directly** — PR-only.
- **Never force-push.**
- **Never replace lens content with shorter / "punchier" versions** — Kaleidoscope is for slow thinking; brevity is anti-product.
- **Stop on uncertainty.** Especially around new lens additions — wrong lens framings can mislead future users.

## Test command

```bash
# Adapt to whatever the repo actually uses (check package.json or pyproject.toml)
npm test || pytest -v
```

## Lint / format command

```bash
npm run lint || ruff check .
```

## How to ship a change

1. Branch from `main` as `<your-id>/<short-feature>`
2. Test the lens or template against a real (or realistic) decision before the PR
3. PR to `main`
4. Wait for human approval before merge

## Pre-commit hooks (run automatically)

- detect-secrets
- check-added-large-files
- check-yaml
- end-of-file-fixer, trailing-whitespace
- detect-private-key
- check-merge-conflict
