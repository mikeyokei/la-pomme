#!/bin/bash

# Watch and build script for Sleek Font development
# Monitors the .glyphs file and automatically rebuilds when changes are detected

GLYPHS_FILE="src/sleek0910.glyphs"
BUILD_SCRIPT="./build-private.sh"

echo "👀 Starting font watcher..."
echo "📂 Monitoring: $GLYPHS_FILE"
echo "🛑 Press Ctrl+C to stop"
echo ""

# Check if fswatch is available (macOS)
if command -v fswatch &> /dev/null; then
    echo "✅ Using fswatch for file monitoring"
    echo ""
    
    # Use fswatch to monitor the file
    fswatch -o "$GLYPHS_FILE" | while read -r change; do
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "🔄 Change detected at $(date '+%H:%M:%S')"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        $BUILD_SCRIPT
        echo ""
        echo "✨ Waiting for next change..."
        echo ""
    done
else
    echo "⚠️  fswatch not found. Installing via Homebrew..."
    echo "   (If you don't have Homebrew, install it from https://brew.sh)"
    
    if command -v brew &> /dev/null; then
        brew install fswatch
        echo "✅ fswatch installed! Starting watcher..."
        echo ""
        
        fswatch -o "$GLYPHS_FILE" | while read -r change; do
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "🔄 Change detected at $(date '+%H:%M:%S')"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            $BUILD_SCRIPT
            echo ""
            echo "✨ Waiting for next change..."
            echo ""
        done
    else
        echo "❌ Homebrew not found. Please install fswatch manually or use Homebrew."
        echo ""
        echo "Alternative: Install fswatch via Homebrew:"
        echo "  /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        echo "  brew install fswatch"
        exit 1
    fi
fi

