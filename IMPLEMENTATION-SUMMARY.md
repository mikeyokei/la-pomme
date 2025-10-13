# OTF Export Download Feature - Implementation Summary

## Overview
Successfully implemented a feature to display OTF export versions alongside TTF versions in the font tester site, with timestamps based on file modification dates.

## What Was Implemented

### 1. OTF Manifest Generator Script (`generate-otf-manifest.py`)
- **Purpose**: Scans the `src/` directory for OTF files and generates a JSON manifest
- **Output**: `build/otf-exports.json`
- **Features**:
  - Detects all `.otf` files in the `src/` directory
  - Extracts file modification timestamps
  - Formats timestamps in a user-friendly format (e.g., "Oct 13, 2025 10:07 AM")
  - Maps font files to display names (Leafeon, Jardin Regular, Jardin Italic, Pommie)
  - Generates JSON manifest similar to `versions.json` structure

### 2. Build Script Integration (`build-from-glyphs.py`)
- **Changes**: Added automatic OTF manifest generation in post-build tasks
- **Location**: After `generate_versions_json()` call
- **Behavior**:
  - Automatically runs `generate-otf-manifest.py` after successful builds
  - Gracefully handles errors if script is missing or fails
  - Ensures OTF manifest is always up-to-date after builds

### 3. Font Tester HTML (`font-tester.html`)
- **Changes**: Updated download section to display both TTF and OTF categories
- **Features**:
  - Loads both `versions.json` (TTF) and `otf-exports.json` (OTF)
  - Displays two separate sections:
    - **TTF VERSION (LATEST)**: Shows latest timestamped TTF builds
    - **EXPORT VERSION (OTF)**: Shows OTF files with modification timestamps
  - Only displays OTF section if OTF files exist
  - Maintains consistent visual style with existing UI
  - Shows modification timestamp in button text and tooltip
  - Preserves all existing functionality (version selector, etc.)

## How It Works

### Build Time
1. User runs `build-from-glyphs.py`
2. Script builds TTF fonts from `.glyphs` sources
3. Script generates `versions.json` with TTF version history
4. Script automatically calls `generate-otf-manifest.py`
5. OTF manifest generator scans `src/` for `.otf` files
6. Generates `build/otf-exports.json` with file metadata

### Runtime (Font Tester)
1. User opens `font-tester.html` in browser
2. JavaScript fetches both `versions.json` and `otf-exports.json`
3. Download section renders:
   - **TTF VERSION**: Shows all available TTF fonts (latest builds)
   - **EXPORT VERSION (OTF)**: Shows only fonts with OTF files available
4. Each OTF download button displays:
   - Font name (e.g., "Leafeon")
   - Modification timestamp (e.g., "Oct 13, 2025 10:07 AM")
   - Tooltip with full timestamp on hover

## Current Status

### Fonts with OTF Exports
- ✅ **Leafeon** - OTF available in `src/Leafeon-Regular.otf`

### Fonts without OTF Exports (currently)
- ❌ Jardin Regular (DarumaPomme-Regular)
- ❌ Jardin Italic (DarumaPomme-Italic)
- ❌ Pommie (Pommiedemo2-Medium)

**Note**: The system automatically detects which fonts have OTF versions. When new OTF files are added to the `src/` directory, they will automatically appear in the download section after running the build script.

## File Structure

```
la-pomme/
├── src/
│   └── Leafeon-Regular.otf          # OTF export files
├── build/
│   ├── versions.json                 # TTF version history
│   ├── otf-exports.json             # OTF exports manifest
│   └── instance_ttf/                # Built TTF files
├── generate-otf-manifest.py         # NEW: OTF manifest generator
├── build-from-glyphs.py             # MODIFIED: Now calls OTF generator
└── font-tester.html                 # MODIFIED: Shows TTF + OTF downloads
```

## Example Output

### build/otf-exports.json
```json
{
  "Leafeon-Regular": [
    {
      "timestamp": "2025-10-13-100727",
      "path": "src/Leafeon-Regular.otf",
      "date": "Oct 13, 2025 10:07 AM",
      "filename": "Leafeon-Regular.otf",
      "display_name": "Leafeon"
    }
  ]
}
```

### Font Tester UI
```
DOWNLOAD FONTS [▼]
├─ TTF VERSION (LATEST):
│  ├─ ↓ Leafeon
│  ├─ ↓ Jardin Regular
│  ├─ ↓ Jardin Italic
│  └─ ↓ Pommie
│
└─ EXPORT VERSION (OTF):
   └─ ↓ Leafeon (Oct 13, 2025 10:07 AM)
```

## Testing

To test the implementation:

1. **Run the OTF manifest generator manually**:
   ```bash
   python3 generate-otf-manifest.py
   ```

2. **Run the full build process**:
   ```bash
   python3 build-from-glyphs.py
   ```

3. **Open the font tester**:
   - Open `font-tester.html` in a web browser
   - Expand the "DOWNLOAD FONTS" section
   - Verify both TTF and OTF sections appear
   - Verify OTF buttons show timestamp

## Future Enhancements

To add more OTF exports:
1. Place `.otf` files in the `src/` directory
2. Name them according to the convention:
   - `Leafeon-Regular.otf`
   - `DarumaPomme-Regular.otf`
   - `DarumaPomme-Italic.otf`
   - `Pommiedemo2-Medium.otf`
3. Run `python3 generate-otf-manifest.py` (or build script)
4. The font tester will automatically display them

## Maintenance

The OTF manifest is automatically regenerated:
- ✅ Every time `build-from-glyphs.py` is run
- ✅ When manually running `generate-otf-manifest.py`
- ✅ Timestamps always reflect actual file modification times

No manual updates to `otf-exports.json` are needed!

