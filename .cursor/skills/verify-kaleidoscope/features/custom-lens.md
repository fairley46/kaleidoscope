# Custom lens load

Custom lens load lets a user add a markdown file under `lenses/` and have the next run include that perspective without code changes.

## Sub-features

- `custom-drop` loads any `lenses/*.md` file that is not dot-prefixed.
- `custom-review` writes a matching `*_Review.md` for the new lens.
- `custom-generic` uses the generic heuristic path when the lens name has no specialized handler.

## How to get to it (user POV)

- Copy `templates/Lens_Template.md` into `lenses/` under a new name.
- Fill the template sections, especially Lens Name and Purpose.
- Run kaleidoscope again with the same problem flow.

## Driving it with verify-kaleidoscope

Preconditions:

- `scripts/doctor.sh` exits 0.
- Use a disposable copy of the lenses directory or create a temp lenses dir passed with `--lenses-dir` when extending the helper. The stock `run-isolated.sh` uses the repo `lenses/` dir, so prefer a throwaway file name and delete it in cleanup for this feature only.

- **Add lens.** Write `lenses/Security_Lens.md` from the template with Lens Name `Security Lens`.
- **Run explore.** Drive `explore-problem` once. The generated reports list includes `Security_Review.md`.
- **Proof.** Copy `Security_Review.md` into the artifact dir and confirm stdout lists that path.
- **Cleanup lens file.** Remove `lenses/Security_Lens.md` after copying proof. Do not leave a temporary lens in the branch unless the change is intentional.

## Gotchas

- Sorted glob order means new lenses appear alphabetically among reviews.
- The first token found in the lens name selects the handler. Token order is company, team, culture, strategy, roadmap, technical, operational, financial, user. A later token in the same name does not override an earlier one.
- Never commit a throwaway verification lens.
