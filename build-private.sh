#!/bin/bash

# Private build script for Sleek Font development
# This script is for internal development and version management

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔧 Building Sleek Font for private development..."
echo "⏰ Build started at $(date '+%Y-%m-%d %H:%M:%S')"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check if fontmake is installed
if ! command -v fontmake &> /dev/null; then
    echo "❌ fontmake not found. Installing dependencies..."
    pip install fontmake fontbakery
fi

# Create build directory if it doesn't exist
mkdir -p build/

# Build the font - export each master separately
echo "📦 Building static fonts for each master..."
# Use Python script to handle corner components properly
python3 build-from-glyphs.py

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "✅ Font built successfully!"
    
    # List built files
    echo "📁 Built files:"
    ls -la build/
    
    # Run quality checks if fontbakery is available
    if command -v fontbakery &> /dev/null; then
        echo "🔍 Running quality checks..."
        fontbakery check-googlefonts build/*.ttf
    else
        echo "⚠️  fontbakery not found. Skipping quality checks."
    fi
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🎉 Private build complete!"
    echo "⏰ Build finished at $(date '+%Y-%m-%d %H:%M:%S')"
    echo "📁 Files are ready in build/ directory."
    echo "💡 Refresh your browser to see changes in the font tester."
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
else
    echo "❌ Build failed. Check the error messages above."
    exit 1
fi
