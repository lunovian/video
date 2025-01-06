import os
import subprocess
from pathlib import Path

def render_animations():
    # Get the animations folder path
    animations_dir = Path(__file__).parent / 'animations'
    
    # Find all Python files in the animations directory
    animation_files = list(animations_dir.glob('*.py'))
    
    if not animation_files:
        print("No animation files found in the animations directory!")
        return
    
    print(f"Found {len(animation_files)} animation files to render.")
    
    # Process each animation file
    for file in animation_files:
        print(f"\nRendering {file.name}...")
        try:
            # Run manim command for each file
            result = subprocess.run([
                'manim',
                str(file),
                '-qh'  # High quality render
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✓ Successfully rendered {file.name}")
            else:
                print(f"✗ Failed to render {file.name}")
                print("Error:", result.stderr)
        except Exception as e:
            print(f"✗ Error processing {file.name}:", str(e))

if __name__ == "__main__":
    print("Starting animation rendering process...")
    render_animations()
    print("\nRendering process completed!")
