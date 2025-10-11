# Font Versioning System - Implementation Summary

## Overview
Implemented automatic font versioning system that creates timestamped font files, maintains version history, and provides version selection in the download UI.

## What Was Implemented

### 1. Build Script (`build-from-glyphs.py`)
- **Timestamp Generation**: Adds timestamps in format `YYYY-MM-DD-HHMMSS` to all font files
- **Versioned Filenames**: Creates files like `DarumaPomme-Regular-2025-10-12-010454.ttf`
- **Latest Copies**: Creates non-timestamped "latest" copies for backward compatibility
- **Version Cleanup**: Automatically keeps only the 3 most recent versions per font
- **Metadata Generation**: Creates `versions.json` with version information

### 2. Dependencies (`requirements.txt`)
- glyphsLib>=6.0.0
- fontmake>=3.0.0
- fontTools>=4.0.0
- ufo2ft>=2.0.0

### 3. Netlify Configuration (`netlify.toml`)
- Updated build command to: `pip install -r requirements.txt && python3 build-from-glyphs.py`
- Fonts are now built automatically on each deployment

### 4. Font Tester UI (`font-tester.html`)
- **Latest Downloads**: Quick download buttons for the latest version of each font
- **Version Selector**: Dropdown menus to select and download specific versions
- **Human-Readable Dates**: Shows version dates like "Oct 12, 2025 01:04 AM"
- **Fallback Support**: Falls back to simple mode if versions.json is not available

## How It Works

### Build Flow
1. When you save a `.glyphs` file and push to git, Netlify detects the change
2. Netlify installs Python dependencies from `requirements.txt`
3. Runs `build-from-glyphs.py` which:
   - Builds fonts from each `.glyphs` file
   - Adds timestamps to filenames
   - Creates "latest" copies without timestamps
   - Deletes old versions (keeps 3 most recent per font)
   - Generates `versions.json` with metadata
4. Deploys the site with updated fonts

### Version Storage
- **Versioned files**: `DarumaPomme-Regular-2025-10-12-010454.ttf`
- **Latest files**: `DarumaPomme-Regular.ttf` (always points to most recent)
- **Metadata**: `build/versions.json` tracks all versions

### versions.json Format
```json
{
  "DarumaPomme-Regular": [
    {
      "timestamp": "2025-10-12-010454",
      "path": "build/instance_ttf/DarumaPomme-Regular-2025-10-12-010454.ttf",
      "date": "Oct 12, 2025 01:04 AM",
      "filename": "DarumaPomme-Regular-2025-10-12-010454.ttf"
    },
    ... (up to 3 versions)
  ]
}
```

## Font Variants Supported
1. **Jardin Regular** (DarumaPomme-Regular)
2. **Jardin Italic** (DarumaPomme-Italic)
3. **Leafeon** (Leafeon-Regular)
4. **Pommie** (Pommiedemo2-Medium)

## Usage

### For Developers
- Edit `.glyphs` files in the `src/` directory
- Push changes to git
- Netlify automatically builds and versions the fonts

### For Users
- **Quick Download**: Click the download button under "LATEST VERSIONS"
- **Version Selection**: Use the "VERSION SELECTOR" section to choose specific versions

## Testing Results
✅ Build script creates versioned files with timestamps
✅ Latest copies are created for backward compatibility
✅ Version cleanup maintains exactly 3 versions per font
✅ versions.json is generated with correct metadata
✅ HTML UI loads and displays version information correctly

## Notes
- Each font variant maintains its own version history
- Versions are identified by the date/time the `.glyphs` file was built
- The system automatically cleans up old versions to save space
- Existing @font-face declarations continue to work (using latest copies)

