# Assets, versions, and presentations

## Layout inside an experiment

```text
experiments/<slug>/
  README.md                     # Hypothesis, index, status, decisions
  versions/
    v001/
      README.md                 # Fixed record for this version
      source/                   # Editable originals if available (SVG, Krita, etc.)
      exports/                  # PNG, WebP, GIF, MP4
      presentation/             # Contact sheet or preview (optional)
    v002/
      ...
```

Directories are materialized only when they contain files.

## Rules

- **Preserve the original.** AI-generated raster output is a source artifact if no editable vector file exists. Never claim a generated image is an editable vector master.
- **Non-destructive.** New variant = new version or new experiment. Never replace older assets in place to change their meaning.
- **Presentation versus master.** `source/` stores the originating file; `exports/` stores rendered files; `presentation/` stores a visual comparison or preview. Link back to the source.
- **Stable naming.** `onyx-of-steampunk-v001-master.png`, `onyx-of-steampunk-v001-preview.webp`, `onyx-pixel-v001-loop.webp`. Use media extensions reflecting actual formats.
- **Record provenance.** Creator/tool, approximate date, prompt or method when relevant, license/rights, source chat/file if known, and whether the file was manually verified.
- **Avoid huge duplication.** Commit necessary source assets; use compact WebP previews. If binary history becomes unwieldy, assess Git LFS separately rather than silently enabling it.
- **GitHub Markdown galleries.** Use relative images in `README.md` once they exist. Do not leave misleading broken-image embeds.
- **Fonts.** Store the typeface name and terms; don't commit third-party font files without confirming redistribution rights.

## Rights and distribution

This is a **private** archive. Existing `LICENSE` is the MIT software license supplied when the repo was initialized and **has not been changed**. Do not assume that private sketches, generated art, studio names, trademarks, or third-party fonts all share one simple redistribution license. Review the repository's license and each asset's provenance **before** inviting collaborators, mirroring the repository, or publishing assets.

Private repository access is separate from IP ownership and trademark clearance.
