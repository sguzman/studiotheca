# Lightweight archive profile

Studiotheca uses a minimal, self-contained public collection architecture:

| Layer | Location | Function |
| --- | --- | --- |
| Overview | `README.md` | Scope and status |
| Studies | `studios/`, `explorations/` | Original creative decisions and independently versioned experiments |
| Ontology | `ontology/catalog.json` | Stable identifiers, relationships, status, and dossier paths |
| Gallery | `gallery/index.json` | Manifest of verified presentation assets |
| Provenance | `docs/assets.md`, experiment dossiers | Rights, source tracking, and import policy |
| Validation | `scripts/validate.py` | Lightweight checks, no external dependencies |
| Stewardship | `CONSTITUTION.md`, `AGENTS.md` | Public-information and editing rules |

This describes repository organization only. It does not confer membership in any external project registry.
