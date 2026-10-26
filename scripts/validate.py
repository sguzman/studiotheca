#!/usr/bin/env python3
"""Validate independent Studiotheca catalog and gallery references."""

import json
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
errors = []


def load(path):
    try:
        return json.loads((root / path).read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        errors.append(f"{path}: {exc}")
        return {}


def path_ok(path, label):
    if not isinstance(path, str) or not path:
        errors.append(f"{label}: missing path")
    elif Path(path).is_absolute() or ".." in Path(path).parts or not (root / path).is_file():
        errors.append(f"{label}: invalid/missing file {path}")


catalog = load("ontology/catalog.json")
gallery = load("gallery/index.json")
if catalog.get("schema") != "studiotheca.catalog.v1":
    errors.append("Catalog schema mismatch")
if gallery.get("schema") != "studiotheca.gallery.v1":
    errors.append("Gallery schema mismatch")

studios = catalog.get("studios", [])
experiments = catalog.get("experiments", [])
entries = gallery.get("entries", [])
if not all(isinstance(x, list) for x in (studios, experiments, entries)):
    errors.append("Expected lists for studios, experiments and entries")
    studios, experiments, entries = [], [], []

studio_ids = set()
for s in studios:
    if not s.get("id") or s["id"] in studio_ids:
        errors.append("Duplicate/missing studio ID")
    studio_ids.add(s.get("id"))
    for key in ("dossier", "brand", "games"):
        path_ok(s.get(key), f"studio {s.get('id')} {key}")

seen = set()
for e in experiments:
    if not e.get("id") or e["id"] in seen:
        errors.append("Duplicate/missing experiment ID")
    seen.add(e.get("id"))
    if e.get("studio_id") not in studio_ids:
        errors.append("Experiment references unknown studio")
    path_ok(e.get("dossier"), f"experiment {e.get('id')}")

seen.clear()
for e in entries:
    if not e.get("id") or e["id"] in seen:
        errors.append("Duplicate/missing gallery ID")
    seen.add(e.get("id"))
    if e.get("studio_id") not in studio_ids:
        errors.append("Gallery references unknown studio")
    for key in ("asset", "dossier"):
        path_ok(e.get(key), f"gallery {e.get('id')} {key}")

for required in ("README.md", "LICENSE", "CONSTITUTION.md", "AGENTS.md",
                 "TARIUM.md", "ontology/README.md", "gallery/README.md"):
    path_ok(required, "required")

if errors:
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    sys.exit(1)
print(f"OK: {len(studios)} studio, {len(experiments)} experiments, {len(entries)} gallery assets")
