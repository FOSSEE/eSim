#!/usr/bin/env python3
"""
eSim Configuration File Fix
This script fixes the configuration file format issue in Appconfig.py
The error occurs when the workspace configuration file doesn't have the expected format.
"""

import os
import sys
from pathlib import Path

def diagnose_config_files():
    """Diagnose the current state of eSim configuration files"""
    print("Diagnosing eSim Configuration Files")
    print("=" * 40)
    
    # Determine user home directory
    if os.name == 'nt':
        user_home = os.path.join('library', 'config')
    else:
        user_home = os.path.expanduser('~')
    
    esim_config_dir = os.path.join(user_home, '.esim')
    workspace_file = os.path.join(esim_config_dir, 'workspace.txt')
    
    print(f"User home: {user_home}")
    print(f"Config directory: {esim_config_dir}")
    print(f"Workspace file: {workspace_file}")
    
    # Check if directory exists
    if not os.path.exists(esim_config_dir):
        print("✗ .esim directory does not exist")
        return False, esim_config_dir, workspace_file
    else:
        print("✓ .esim directory exists")
    
    # Check if workspace.txt exists
    if not os.path.exists(workspace_file):
        print("✗ workspace.txt does not exist")
        return False, esim_config_dir, workspace_file
    else:
        print("✓ workspace.txt exists")
    
    # Read and analyze workspace.txt content
    print("\nAnalyzing workspace.txt content:")
    try:
        with open(workspace_file, 'r') as f:
            content = f.read()
            lines = content.strip().split('\n')
            
        print(f"File content: '{content}'")
        print(f"Number of lines: {len(lines)}")
        
        if lines:
            first_line = lines[0].strip()
            print(f"First line: '{first_line}'")
            
            # Check if first line has space-separated values
            parts = first_line.split(' ')
            print(f"Parts when split by space: {parts} (count: {len(parts)})")
            
            if len(parts) < 2:
                print("✗ First line doesn't have expected format (workspace_check home_path)")
                return False, esim_config_dir, workspace_file
            else:
                print("✓ First line has correct format")
        
    except Exception as e:
        print(f"✗ Error reading workspace.txt: {e}")
        return False, esim_config_dir, workspace_file
    
    return True, esim_config_dir, workspace_file

def create_proper_workspace_config(esim_config_dir, workspace_file):
    """Create a properly formatted workspace configuration"""
    try:
        # Ensure directory exists
        os.makedirs(esim_config_dir, exist_ok=True)
        
        # Determine default workspace path
        if os.name == 'nt':
            user_home = os.path.join('library', 'config')
        else:
            user_home = os.path.expanduser('~')
        
        default_workspace = os.path.join(user_home, 'eSim-Workspace')
        
        # Create workspace directory if it doesn't exist
        os.makedirs(default_workspace, exist_ok=True)
        
        # Create properly formatted workspace.txt
        # Format expected by Appconfig.py: "workspace_check home_path"
        # workspace_check: 1 (workspace is set) or 0 (not set)
        # home_path: path to the workspace directory
        config_content = f"1 {default_workspace}\n"
        
        with open(workspace_file, 'w') as f:
            f.write(config_content)
        
        print(f"✓ Created proper workspace configuration:")
        print(f"  Content: '{config_content.strip()}'")
        print(f"  Workspace directory: {default_workspace}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error creating workspace configuration: {e}")
        return False

def fix_appconfig_robustness():
    """Provide suggestions for making Appconfig.py more robust"""
    
    robust_code = '''
# Suggested improvement for Appconfig.py around line 46:
# Replace the problematic line with more robust parsing:

# ORIGINAL (problematic):
# workspace_check, home = file.readline().split(' ', 1)

# IMPROVED (robust):
try:
    line = file.readline().strip()
    if line:
        parts = line.split(' ', 1)
        if len(parts) >= 2:
            workspace_check, home = parts[0], parts[1]
        elif len(parts) == 1:
            # Handle case where only workspace_check exists
            workspace_check = parts[0]
            home = os.path.join(os.path.expanduser('~'), 'eSim-Workspace')
            print(f"Warning: Using default workspace path: {home}")
        else:
            # Handle empty line
            workspace_check = '0'
            home = os.path.join(os.path.expanduser('~'), 'eSim-Workspace')
            print(f"Warning: Empty config, using defaults")
    else:
        # Handle empty file
        workspace_check = '0'
        home = os.path.join(os.path.expanduser('~'), 'eSim-Workspace')
        print(f"Warning: Empty config file, using defaults")
except Exception as e:
    # Handle any other parsing errors
    print(f"Error reading config: {e}")
    workspace_check = '0'
    home = os.path.join(os.path.expanduser('~'), 'eSim-Workspace')
    print(f"Using default configuration")
'''
    
    print("\n" + "=" * 60)
    print("SUGGESTED ROBUST CODE FIX FOR APPCONFIG.PY:")
    print("=" * 60)
    print(robust_code)

def main():
    """Main function to diagnose and fix configuration issues"""
    print("eSim Configuration Diagnostic and Fix Tool")
    print("=" * 45)
    
    # Step 1: Diagnose current state
    print("\n1. Diagnosing current configuration...")
    is_valid, config_dir, workspace_file = diagnose_config_files()
    
    # Step 2: Fix configuration if needed
    if not is_valid:
        print("\n2. Fixing configuration...")
        success = create_proper_workspace_config(config_dir, workspace_file)
        if success:
            print("✓ Configuration fixed successfully")
        else:
            print("✗ Failed to fix configuration")
            return
    else:
        print("\n2. Configuration appears to be valid")
    
    # Step 3: Provide code improvement suggestions
    print("\n3. Providing robustness improvements...")
    fix_appconfig_robustness()
    
    # Step 4: Final verification
    print("\n4. Final verification...")
    is_valid_final, _, _ = diagnose_config_files()
    
    if is_valid_final:
        print("\n" + "=" * 50)
        print("SUCCESS: Configuration is now properly set up!")
        print("=" * 50)
        print("You can now try running: python Application.py")
        print("\nIf you still get errors, consider applying the")
        print("robust code fix to Appconfig.py as shown above.")
    else:
        print("\n" + "=" * 50)
        print("ISSUE: Configuration still has problems")
        print("=" * 50)
        print("Please check file permissions and try again.")

if __name__ == "__main__":
    main()
