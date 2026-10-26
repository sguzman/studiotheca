# Brand acceptance and verification

These are gates for future assets, not a claim that the outputs already exist.

| Gate | Objective evidence | Current state |
| --- | --- | --- |
| Identity model | Stable canonical identifiers, valid relations, consistent paths | Authored; repository validation required |
| Name semantics | Dusk, raven and works meanings recorded without genre lock-in | Authored |
| Original provenance | Exact generator record, PNG dimensions, SHA-256, source location | Verified in working conversation; GitHub binary absent |
| Commercial naming | Official US/MX search and common-law conflict review | Unresolved |
| Primary scene | Raven clearly perched before gigantic moon in purple night | Visual candidate positively received |
| Emblem | Raven + moon + branch readable at 32, 48, 128, 512px | Not produced |
| Wordmark | Correct full name, readability, two-background comparison | Not produced |
| Avatar and banner | Circle crop, square crop, wide safe area | Not produced |
| Accessible reduced-color mark | Silhouette and contrast checks, one-color fallback | Not produced |
| Animation ident | Verified motion and static-equivalent export | Not produced |
| Public deployment | Organization, storefront, media, games, cross-links | Not done |

Before accepting a logo, conduct direct visual checks on actual rendered pixels at target sizes; file existence, AI description and successful scripts are not substitutes for visual QA. Do not mark the studio *released* just because its ontology is documented.

## Repository validation

The [Studiotheca validator](../../scripts/validate.py) should verify this studio's catalog references. The structured identity document must also have no duplicate symbols, undefined relationship targets or invalid required composition references. A failing CI runner cannot count as passing QA.
