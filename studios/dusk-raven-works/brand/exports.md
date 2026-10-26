# Dusk Raven Works — reproducible artwork exports

The original v001 raster is preserved by its source checksum in [media-import.json](media-import.json). It is not included in this public Git repository yet; the [96px faithful preview](experiments/violet-moon/versions/v001/README.md) is checked in.

## Available export profiles

| Profile | Size | Format | Status |
| --- | --- | --- | --- |
| Square avatars | 512×512, 256×256 | PNG | Draft candidates (512px is below 1 MB in the verified run) |
| Reduced avatars | 128×128, 64×64, 32×32 | WebP | Draft candidates, not proven legible at every size |
| Wide banner | 1600×900 | WebP | Draft, blur-extended sides |
| Social header | 1500×500 | WebP | Draft, cropped foreground and blur-extended sides |

The exact original 1254×1254 image was used to generate these candidate exports and a local proof sheet; the complete asset-kit ZIP was handed off in the associated session. This public repository holds the export recipe and the miniature gallery preview, **not** the full ZIP.

## Reproduction and safety

Requires Python and Pillow. Supply the exact original binary and an export destination:

`python3 scripts/export_dusk_raven.py path/to/raven_beneath_the_violet_moon.png path/to/exports/`

The exporter verifies the original SHA-256 and dimensions, refuses the wrong source, never changes the source, and emits SHA-256 provenance for every derived output in `MANIFEST.json`. The bypass switch is only for synthetic test fixtures.

GitHub Actions tests the export algorithm using synthetic images; it does **not** imply that the original image was uploaded to GitHub, or that a particular icon/wordmark/banner has been commercially or visually approved.

## Visual sign-off still needed

Review circle crops and legibility at 32/48/128 pixels, compare the silhouette with the approved composition, decide whether the horizon belongs in storefront graphics, and select an actual typeface before announcing canonical branding. No result is automatically approved merely because an export exists.
