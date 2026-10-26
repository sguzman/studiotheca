#!/usr/bin/env python3
"""Stdlib-only guard against swapped, missing, or misrepresented artwork."""
import hashlib
import json
from pathlib import Path


def problems(root: Path, manifest_path: str):
    errors = []
    try:
        manifest = json.loads((root / manifest_path).read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        return [f"media: unreadable manifest {manifest_path}: {exc}"]
    if manifest.get("schema") != "studiotheca.media-import.v1":
        errors.append(f"media: unsupported schema: {manifest_path}")
    for item in manifest.get("items", []):
        name = item.get("id", "unidentified")
        source = item.get("intended_repository_path")
        declared = str(item.get("sha256", ""))
        if len(declared) != 64:
            errors.append(f"media {name}: invalid original SHA-256")
        if source and (Path(source).is_absolute() or ".." in Path(source).parts):
            errors.append(f"media {name}: unsafe original path")
        if source and (root / source).is_file():
            if "not-committed" in str(item.get("status", "")):
                errors.append(f"media {name}: original exists but still marked absent")
            digest = hashlib.sha256((root / source).read_bytes()).hexdigest()
            if digest != declared:
                errors.append(f"media {name}: original SHA-256 mismatch")
            if (root / source).stat().st_size != item.get("bytes"):
                errors.append(f"media {name}: original byte count mismatch")
        for preview in item.get("derivative_previews", []):
            path = preview.get("file", "")
            if not path or Path(path).is_absolute() or ".." in Path(path).parts:
                errors.append(f"media {name}: invalid preview path")
                continue
            file = root / path
            if not file.is_file():
                errors.append(f"media {name}: preview file missing")
                continue
            data = file.read_bytes()
            if hashlib.sha256(data).hexdigest() != preview.get("sha256"):
                errors.append(f"media {name}: preview SHA-256 mismatch")
            if len(data) != preview.get("bytes"):
                errors.append(f"media {name}: preview byte count mismatch")
            if preview.get("format") == "image/jpeg" and not data.startswith(b"\xff\xd8\xff"):
                errors.append(f"media {name}: invalid JPEG signature")
    return errors
