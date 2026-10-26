# Studiotheca

An independent creative archive for game-studio identities, visual experiments, and prospective games. It preserves design directions and decisions without presenting exploratory work as finished products.

## Explore

- [Dusk Raven Works](studios/dusk-raven-works/README.md) — preferred studio direction with structured identity, first visual study, and publication gates.
- [Onyx Foundry](studios/onyx-foundry/README.md) — independently preserved studio concept, with its own visual identity.
- [Studio seed ledger](studios/seed-ledger.md) — parked name-and-identity drafts, including Orivellum, Duskheron, and Morrowspindle; not selected studios.
- [Brand experiments](studios/onyx-foundry/brand/experiments/README.md) — versioned studies of an emblem, animation, typography, and palette.
- [Gallery](gallery/README.md) — actual presentation files currently checked into the repository.
- [Ontology](ontology/README.md) — machine-readable catalog of studios, experiments, and statuses.
- [Game formats](explorations/game-types.md) and [creative throughlines](explorations/throughlines.md) — exploratory research, not announced games.
- [Archive workflow](docs/workflow.md) · [Asset provenance](docs/assets.md)

## Current state

The archive contains **two developed studio identity dossiers**, **three parked name seeds**, **five experiment tracks**, and **one checked-in palette SVG**. The Dusk Raven Works PNG master is verified but **not yet uploaded to this repository**. Original emblem and animated ident media are recorded for import but are not yet part of the repository. No game is represented as released, and no studio name is represented as commercially cleared.

This is not a game-source monorepo. Implementations belong in separate repositories, which can be linked from their concept dossiers when available.

## Structure

`studios/` contains creative dossiers; `explorations/` contains cross-studio research; `ontology/catalog.json` indexes the documented identities, including optional machine-readable studio identities; and `gallery/index.json` references only media actually present. Numbered study versions preserve decisions without overwriting alternatives.

Run `python3 scripts/validate.py` to check catalog, studio-identity, and gallery integrity using only Python's standard library.

## Publication and rights

The existing [MIT license](LICENSE) is retained. Third-party font files are not distributed. Commercial studio names and possible trademarks require independent clearance; an open copyright license does not establish the right to impersonate a publisher. See the [public charter](CONSTITUTION.md) and [asset rules](docs/assets.md).

Studiotheca follows a lightweight, self-contained ontology-and-gallery architecture without assuming membership in any external registry.
