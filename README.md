# La Pomme Font

La Pomme is a modern typeface collection featuring three distinct variants: Jardin, Leafeon, and Pommie.

## 🎨 Font Tester

**🌐 Deploy to Netlify:** 
1. Go to [netlify.com](https://netlify.com)
2. Click "Add new site" → "Import an existing project"
3. Connect your GitHub account and select this repository
4. Click "Deploy" (no configuration needed - `netlify.toml` is already set up)
5. Your tester will be live at: `https://your-site-name.netlify.app`

**💻 Local Testing:**
```bash
# Simply open the tester - it uses OTF files directly from src/
open font-tester.html
```

> **Note:** The font tester now loads OTF files directly from the `src/` directory. No build step required for preview!

**Features:**
- Master selector (switch between Jardin, Leafeon, Pommie)
- **Upload & test fonts** - drag & drop or click to upload any font file (TTF, OTF, WOFF, WOFF2)
- Size, spacing, and line height controls
- Custom text, samples, and character grid views
- **OpenType Features** - toggle ligatures, contextual alternates, swashes, small caps, and more
- **Stylistic Sets** - select text and apply stylistic sets (ss01-ss20) to specific characters
- **Download fonts** - automatically detects available OTF files from `src/` directory
- Brutalist minimal design

## Installation

Download the latest release from the [Releases](https://github.com/YOUR_USERNAME/la-pomme-font/releases) page and install the font files on your system.

## Building from Source

To build the font from source, you'll need to have `fontmake` and `fontbakery` installed.

```bash
pip install fontmake fontbakery
```

Then, run the build script:

```bash
python3 build-from-glyphs.py
```

This will build all three La Pomme variants from the glyphs files in the `src/` directory:
- **Jardin** (from `jardin.glyphs`) → DarumaPomme-Regular.ttf, DarumaPomme-Italic.ttf
- **Leafeon** (from `leafeon.glyphs`) → Leafeon-Regular.ttf
- **Pommie** (from `pommie.glyphs`) → Pommiedemo2-Medium.ttf

The generated fonts will be in `build/instance_ttf/`.

## Upload & Test Fonts

You can upload and test any font file directly in the browser without needing to place files in directories:

1. Open `font-tester.html`
2. Look for the "UPLOAD & TEST FONT" section
3. Either:
   - **Click** the upload area and select font files
   - **Drag & drop** font files directly onto the dashed box
4. The font will automatically load and switch to it for testing
5. Supports: TTF, OTF, WOFF, WOFF2 formats
6. Upload multiple fonts at once!

Uploaded fonts appear in the MASTER dropdown with a 📤 icon.

## OpenType Features

The font tester includes comprehensive OpenType feature controls:

### Global Features (Apply to all text)
Toggle these features on/off to see their effect across all text:
- **Ligatures (liga)** - Common ligatures (fi, fl, etc.)
- **Contextual Alternates (calt)** - Context-aware character substitutions
- **Discretionary Ligatures (dlig)** - Optional decorative ligatures
- **Swash (swsh)** - Decorative flourishes
- **Small Caps (smcp)** - Small capital letters
- **Old Style Figures (onum)** - Old-style numbers

### Stylistic Sets (Apply to selected text only)
**To Apply:**
1. **Select text** in the custom text editor
2. **Click a stylistic set button** (SS01-SS20)
3. The stylistic set will be applied **only to your selection**
4. Different parts of your text can have different stylistic sets!

**To Remove:**
- **Method 1:** Select the styled text (hover shows gray background), then click any SS button
- **Method 2:** Click directly on the styled text to remove it
- **Method 3:** Click "Clear All SS" button to remove all stylistic sets at once

**Example workflow:**
- Type "Hello World"
- Select "Hello", click "SS01" (applies first stylistic set)
- Select "World", click "SS02" (applies different set)
- To remove: Click on "Hello" text OR select it and click any SS button

## Font Distribution

The font tester includes an automatic download feature that detects available font files:

**TTF Files** (auto-generated):
- Built fonts are automatically available for download from `build/instance_ttf/`

**OTF Files** (manual export):
- Export OTF fonts from your design software and place them in the `src/` directory
- The tester will automatically detect and display download buttons for:
  - `src/jardin.otf`
  - `src/leafeon.otf`
  - `src/pommie.otf`
  - Or any matching font name variants (e.g., `DarumaPomme-Regular.otf`, `Leafeon-Medium.otf`)

The download buttons update automatically based on which files are present.
