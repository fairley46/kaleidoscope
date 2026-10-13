# Report files on disk

Report files on disk are the durable output of a run. Each lens gets a review file. The master report joins perspectives into one markdown document under the chosen reports directory.

## Sub-features

- `report-per-lens` writes one `*_Review.md` per loaded lens.
- `report-master` writes `Kaleidoscope_Report.md`.
- `report-dir` honors `--reports-dir`.

## How to get to it (user POV)

- Complete any explore run.
- Open the path printed under `Generated reports` in stdout.
- Pass `--reports-dir` to choose where files land.

## Driving it with verify-kaleidoscope

Preconditions:

- `scripts/doctor.sh` exits 0.

- **Run explore.** Use `scripts/run-isolated.sh reports-1 "<problem>"` with piped answers. Exit code is `0`.
- **List reviews.** Confirm the disposable reports dir contains one `*_Review.md` per lens file plus `Kaleidoscope_Report.md`.
- **Confirm isolation.** Confirm nothing new was written under the tracked repo `reports/` directory for this run.
- **Proof.** Copy the master report and at least one lens review into the artifact root.

## Gotchas

- Tracked `reports/` is gitignored for generated content. Proof still belongs under the artifact root, not only in `/tmp`.
- Cleanup removes `/tmp/ks-verify-<run-id>` only. Re-copy anything you still need into artifacts before cleanup.
