#!/usr/bin/env python3
"""
Build fonts directly from .glyphs file, removing problematic corner components
"""
import sys
import json
import re
from datetime import datetime
from pathlib import Path
from glyphsLib import GSFont
from fontmake.font_project import FontProject
import ufo2ft

def get_timestamp():
    """Generate timestamp for versioning"""
    return datetime.now().strftime('%Y-%m-%d-%H%M%S')

def get_base_font_name(filename):
    """Extract base font name without timestamp"""
    # Remove timestamp pattern: -YYYY-MM-DD-HHMMSS.ttf
    pattern = r'-\d{4}-\d{2}-\d{2}-\d{6}\.ttf$'
    base_name = re.sub(pattern, '', filename)
    return base_name

def cleanup_old_versions(output_dir, max_versions=3):
    """Keep only the most recent versions of each font"""
    print(f"🧹 Cleaning up old versions (keeping {max_versions} most recent)...")
    
    output_path = Path(output_dir) / "instance_ttf"
    if not output_path.exists():
        return
    
    # Group files by base font name
    font_versions = {}
    for font_file in output_path.glob('*.ttf'):
        base_name = get_base_font_name(font_file.name)
        if base_name not in font_versions:
            font_versions[base_name] = []
        font_versions[base_name].append(font_file)
    
    # For each font, keep only the N most recent versions
    deleted_count = 0
    for base_name, files in font_versions.items():
        if len(files) > max_versions:
            # Sort by modification time (most recent first)
            files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
            
            # Delete old versions
            for old_file in files[max_versions:]:
                print(f"   Deleting old version: {old_file.name}")
                old_file.unlink()
                deleted_count += 1
    
    if deleted_count > 0:
        print(f"   Deleted {deleted_count} old version(s)")
    else:
        print(f"   No old versions to delete")

def generate_versions_json(output_dir):
    """Generate versions.json with metadata about all available fonts"""
    print("📝 Generating versions.json...")
    
    output_path = Path(output_dir) / "instance_ttf"
    versions_data = {}
    
    if output_path.exists():
        for font_file in sorted(output_path.glob('*.ttf')):
            base_name = get_base_font_name(font_file.name)
            
            # Extract timestamp from filename
            timestamp_match = re.search(r'(\d{4}-\d{2}-\d{2}-\d{6})', font_file.name)
            if timestamp_match:
                timestamp_str = timestamp_match.group(1)
                # Parse timestamp for human-readable date
                try:
                    dt = datetime.strptime(timestamp_str, '%Y-%m-%d-%H%M%S')
                    human_date = dt.strftime('%b %d, %Y %I:%M %p')
                except:
                    human_date = timestamp_str
                
                if base_name not in versions_data:
                    versions_data[base_name] = []
                
                versions_data[base_name].append({
                    'timestamp': timestamp_str,
                    'path': f'build/instance_ttf/{font_file.name}',
                    'date': human_date,
                    'filename': font_file.name
                })
    
    # Sort versions by timestamp (most recent first)
    for base_name in versions_data:
        versions_data[base_name].sort(key=lambda x: x['timestamp'], reverse=True)
    
    # Write to versions.json
    versions_file = Path(output_dir) / 'versions.json'
    with open(versions_file, 'w') as f:
        json.dump(versions_data, f, indent=2)
    
    print(f"   Created {versions_file}")
    print(f"   Tracked {sum(len(v) for v in versions_data.values())} version(s) across {len(versions_data)} font(s)")

def remove_corner_components(font):
    """Remove corner components that cause build issues"""
    print("🔧 Removing problematic corner and smart components...")
    
    removed_count = 0
    for glyph in font.glyphs:
        for layer in glyph.layers:
            # Remove hints/corner components (stored differently)
            if hasattr(layer, 'hints'):
                hints_to_remove = []
                for i, hint in enumerate(layer.hints):
                    if hasattr(hint, 'type') and hint.type in ['Corner', 'Segment']:
                        hints_to_remove.append(i)
                
                for i in reversed(hints_to_remove):
                    del layer.hints[i]
                    removed_count += 1
            
            # Also check for corner components
            if hasattr(layer, 'components'):
                components_to_remove = []
                for i, component in enumerate(layer.components):
                    if hasattr(component, 'name') and component.name and 'corner' in component.name.lower():
                        components_to_remove.append(i)
                
                for i in reversed(components_to_remove):
                    del layer.components[i]
                    removed_count += 1
    
    print(f"   Removed {removed_count} corner/smart components")
    return font

def build_masters(glyphs_path, output_dir, timestamp=None):
    """Build each master separately from a .glyphs file"""
    print(f"📖 Loading {glyphs_path}...")
    
    # Load the font
    font = GSFont(glyphs_path)
    
    # Remove problematic corner components
    font = remove_corner_components(font)
    
    print(f"✅ Found {len(font.masters)} masters")
    
    # Create output directory
    output_path = Path(output_dir) / "instance_ttf"
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Use provided timestamp or generate new one (for backward compatibility)
    if timestamp is None:
        timestamp = get_timestamp()
        print(f"⏰ Build timestamp: {timestamp}")
    else:
        print(f"⏰ Using session timestamp: {timestamp}")
    
    # Build using fontmake
    print("🔨 Building fonts...")
    try:
        # Create a temporary project
        project = FontProject()
        
        # Save to temporary location and build
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.glyphs', delete=False, mode='w') as tmp:
            tmp_path = tmp.name
        
        font.save(tmp_path)
        
        # Build TTF for each master
        from fontmake.__main__ import main as fontmake_main
        import os
        
        # Disable corner components filter via environment variable
        os.environ['SKIP_CORNER_COMPONENTS'] = '1'
        
        args = [
            '-g', tmp_path,
            '-o', 'ttf',
            '--output-dir', str(output_path),
            '--no-production-names',
        ]
        
        fontmake_main(args)
        
        # Clean up temporary file
        Path(tmp_path).unlink()
        
        # Rename built fonts to include timestamp
        print("📝 Adding version timestamps to filenames...")
        built_files = list(output_path.glob('*.ttf'))
        
        # Filter out already timestamped files
        new_files = [f for f in built_files if not re.search(r'-\d{4}-\d{2}-\d{2}-\d{6}\.ttf$', f.name)]
        
        for font_file in new_files:
            base_name = font_file.stem  # filename without extension
            new_name = f"{base_name}-{timestamp}.ttf"
            new_path = font_file.parent / new_name
            
            # Rename to versioned filename
            font_file.rename(new_path)
            print(f"   ✓ {new_name}")
            
            # Also create a "latest" copy for backward compatibility
            latest_path = font_file.parent / f"{base_name}.ttf"
            import shutil
            shutil.copy2(new_path, latest_path)
            print(f"   ✓ {base_name}.ttf (latest)")
        
        print(f"✅ Fonts built successfully in {output_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error building fonts: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    # Build all three La Pomme font variants
    glyphs_files = [
        ('src/jardin.glyphs', 'Jardin'),
        ('src/leafeon.glyphs', 'Leafeon'),
        ('src/pommie.glyphs', 'Pommie')
    ]
    output_dir = 'build'
    
    # Generate a single timestamp for this entire build session
    build_timestamp = get_timestamp()
    print(f"\n{'='*60}")
    print(f"🕐 Build Session Timestamp: {build_timestamp}")
    print(f"{'='*60}")
    
    all_success = True
    for glyphs_file, variant_name in glyphs_files:
        print(f"\n{'='*60}")
        print(f"Building La Pomme - {variant_name}")
        print(f"{'='*60}")
        success = build_masters(glyphs_file, output_dir, build_timestamp)
        all_success = all_success and success
    
    # After building all fonts, cleanup old versions and generate versions.json
    if all_success:
        print(f"\n{'='*60}")
        print("Post-build tasks")
        print(f"{'='*60}")
        cleanup_old_versions(output_dir, max_versions=3)
        generate_versions_json(output_dir)
        
        # Generate OTF exports manifest
        try:
            from pathlib import Path
            import subprocess
            manifest_script = Path(__file__).parent / 'generate-otf-manifest.py'
            if manifest_script.exists():
                subprocess.run([sys.executable, str(manifest_script)], check=True)
            else:
                print("⚠️ generate-otf-manifest.py not found, skipping OTF manifest generation")
        except Exception as e:
            print(f"⚠️ Error generating OTF manifest: {e}")
    
    print(f"\n{'='*60}")
    if all_success:
        print("✅ All La Pomme variants built successfully!")
        print("📦 Version history updated")
    else:
        print("❌ Some variants failed to build")
    print(f"{'='*60}")
    
    sys.exit(0 if all_success else 1)

