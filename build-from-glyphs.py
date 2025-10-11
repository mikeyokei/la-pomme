#!/usr/bin/env python3
"""
Build fonts directly from .glyphs file, removing problematic corner components
"""
import sys
from pathlib import Path
from glyphsLib import GSFont
from fontmake.font_project import FontProject
import ufo2ft

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

def build_masters(glyphs_path, output_dir):
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
        
        # Clean up
        Path(tmp_path).unlink()
        
        print(f"✅ Fonts built successfully in {output_path}")
        print(f"📁 Built files:")
        for font_file in output_path.glob('*.ttf'):
            print(f"   - {font_file.name}")
        
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
    
    all_success = True
    for glyphs_file, variant_name in glyphs_files:
        print(f"\n{'='*60}")
        print(f"Building La Pomme - {variant_name}")
        print(f"{'='*60}")
        success = build_masters(glyphs_file, output_dir)
        all_success = all_success and success
    
    print(f"\n{'='*60}")
    if all_success:
        print("✅ All La Pomme variants built successfully!")
    else:
        print("❌ Some variants failed to build")
    print(f"{'='*60}")
    
    sys.exit(0 if all_success else 1)

