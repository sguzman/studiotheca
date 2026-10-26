#!/usr/bin/env python3
"""Validate optional Studiotheca studio identity JSON documents without dependencies."""

import json
import re
from pathlib import Path


def validate(root: Path, path: str, expected_studio_id: str):
    errors = []
    try:
        model = json.loads((root / path).read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        return [f"identity {expected_studio_id}: unreadable: {exc}"]

    if model.get("schema") != "studiotheca.studio-identity.v1":
        errors.append("identity: invalid schema")
    if model.get("id") != expected_studio_id:
        errors.append("identity: mismatched studio id")
    if not isinstance(model.get("name"), str) or not model["name"].strip():
        errors.append("identity: missing display name")

    entities = model.get("entities", [])
    if not isinstance(entities, list) or not entities:
        return errors + ["identity: missing symbols"]
    ids = [e.get("id") for e in entities if isinstance(e, dict)]
    if len(ids) != len(entities) or any(not isinstance(i, str) or not i for i in ids):
        errors.append("identity: invalid symbol id")
    if len(ids) != len(set(ids)):
        errors.append("identity: duplicate symbol")
    allowed = set(ids) | {expected_studio_id}

    relations = model.get("relations", [])
    if not isinstance(relations, list) or not relations:
        errors.append("identity: missing relationships")
    else:
        for index, rel in enumerate(relations):
            if not isinstance(rel, dict):
                errors.append(f"identity: relationship {index} not an object")
            elif rel.get("subject") not in allowed or rel.get("object") not in allowed:
                errors.append(f"identity: relationship {index} has unknown endpoint")
            elif not isinstance(rel.get("predicate"), str) or not rel["predicate"]:
                errors.append(f"identity: relationship {index} missing predicate")

    comp = model.get("canonical_composition", {})
    required = comp.get("required", []) if isinstance(comp, dict) else []
    if not isinstance(required, list) or not required or any(x not in set(ids) for x in required):
        errors.append("identity: unknown or missing required symbols")

    palette = model.get("palette", {})
    colors = palette.get("colors", []) if isinstance(palette, dict) else []
    if not isinstance(colors, list) or not colors:
        errors.append("identity: missing palette")
    else:
        for c in colors:
            if not isinstance(c, dict) or re.fullmatch(r"#[0-9A-Fa-f]{6}", str(c.get("hex", ""))) is None:
                errors.append("identity: invalid color hex")

    forms = model.get("forms", [])
    if not isinstance(forms, list) or not forms:
        errors.append("identity: missing presentation forms")
    elif any(not isinstance(f, dict) or not f.get("id") for f in forms) or len({f["id"] for f in forms if isinstance(f, dict) and f.get("id")}) != len(forms):
        errors.append("identity: duplicate/invalid presentation form")

    for key in ("asset_manifest", "decisions", "quality"):
        value = model.get(key)
        if not isinstance(value, str) or not value or ".." in Path(value).parts or Path(value).is_absolute() or not (root / value).is_file():
            errors.append(f"identity: missing or unsafe {key} path")

    return errors
