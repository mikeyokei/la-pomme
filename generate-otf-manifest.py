#!/usr/bin/env python3
"""
Generate manifest of OTF export files with modification timestamps
"""
import json
from datetime import datetime
from pathlib import Path


def generate_otf_manifest(src_dir='src', output_dir='build'):
    """Scan src directory for OTF files and generate manifest with timestamps"""
    print("📝 Generating OTF exports manifest...")
    
    src_path = Path(src_dir)
    otf_exports = {}
    
    if not src_path.exists():
        print(f"   ⚠️ Source directory {src_dir} not found")
        return
    
    # Map OTF filenames to display names and base names
    font_mapping = {
        'LaPomme-ExtraRough.otf': {
            'display_name': 'La Pomme Extra Rough',
            'base_name': 'LaPomme-ExtraRough'
        },
        'LaPomme-Roughen.otf': {
            'display_name': 'La Pomme Roughen',
            'base_name': 'LaPomme-Roughen'
        },
        'LaPomme-Italic.otf': {
            'display_name': 'La Pomme Italic',
            'base_name': 'LaPomme-Italic'
        },
        'LaPomme-Rounded.otf': {
            'display_name': 'La Pomme Rounded',
            'base_name': 'LaPomme-Rounded'
        },
        'Leafeon-Regular.otf': {
            'display_name': 'Leafeon',
            'base_name': 'Leafeon-Regular'
        },
        'Leafeon01-Regular.otf': {
            'display_name': 'Leafeon 01',
            'base_name': 'Leafeon01-Regular'
        },
        'CCC-Croissant-Regular.otf': {
            'display_name': 'Croissant',
            'base_name': 'CCC-Croissant-Regular'
        }
    }
    
    # Scan for OTF files
    otf_files = list(src_path.glob('*.otf'))
    
    if not otf_files:
        print(f"   ℹ️ No OTF files found in {src_dir}")
    else:
        print(f"   Found {len(otf_files)} OTF file(s)")
    
    for otf_file in sorted(otf_files):
        # Get file modification time
        mtime = otf_file.stat().st_mtime
        mod_datetime = datetime.fromtimestamp(mtime)
        
        # Format timestamp similar to build script format
        timestamp_str = mod_datetime.strftime('%Y-%m-%d-%H%M%S')
        human_date = mod_datetime.strftime('%b %d, %Y %I:%M %p')
        
        # Get font info from mapping or use filename
        font_info = font_mapping.get(otf_file.name, {
            'display_name': otf_file.stem,
            'base_name': otf_file.stem
        })
        
        base_name = font_info['base_name']
        
        if base_name not in otf_exports:
            otf_exports[base_name] = []
        
        otf_exports[base_name].append({
            'timestamp': timestamp_str,
            'path': f'src/{otf_file.name}',
            'date': human_date,
            'filename': otf_file.name,
            'display_name': font_info['display_name']
        })
        
        print(f"   ✓ {otf_file.name} - {human_date}")
    
    # Write manifest file
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    manifest_file = output_path / 'otf-exports.json'
    with open(manifest_file, 'w') as f:
        json.dump(otf_exports, f, indent=2)
    
    print(f"   Created {manifest_file}")
    print(f"   Tracked {sum(len(v) for v in otf_exports.values())} OTF export(s)")


if __name__ == '__main__':
    generate_otf_manifest()

