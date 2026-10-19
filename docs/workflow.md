# Creative workflow

## No Git branches for creative alternatives

Work directly on the repository's existing `main` unless explicitly requested otherwise. Parallel *concepts* are separate directories, not branches.

## Identity stages

1. **Idea** — loose sketch, question, or reference.
2. **Experiment** — one design hypothesis in `brand/experiments/<slug>/`.
3. **Version** — snapshot of one iteration in `versions/v001/`, `v002/`, etc. Never modify an older snapshot to represent a new visual choice.
4. **Candidate** — one or more versions actively being compared.
5. **Approved** — chosen for a *particular use*, e.g. a pixel-art intro; not necessarily the final studio master.
6. **Archived/rejected** — preserved with a short reason, not deleted.

Experiment README files can change to reflect status and navigation. The version folders should be append-only. A new source file with a corrected drawing goes into a new version, even if only one element moved.

A *presentation* is the curated view of versions (gallery, contact sheet, slides, or playable animation). It points to originals rather than creating another conflicting source of truth.

## To run parallel experiments

Copy [the experiment template](../templates/brand-experiment.md) into a new experiment directory. Assign a distinct slug. Write the hypothesis and keep its versions there. Update the studio's [experiment index](../studios/onyx-foundry/brand/experiments/README.md) as new ideas are created.

Avoid generic names like `final-final-2.png`. Record a status and a decision in text; do not encode approval merely by renaming an image to `final.png`.

## To record a game

Copy [the game concept template](../templates/game-concept.md) into `studios/<studio>/games/<game-slug>/README.md`. A game may begin as an idea with no implementation repo. Record mechanics and emotional objectives separately. Link the eventual game code repository rather than copying source code here.

## Simple decisions

Each experiment keeps a dated decision log: what changed, why, chosen/rejected, and the version that demonstrates it. Rejected experiments remain available for later reconsideration.
