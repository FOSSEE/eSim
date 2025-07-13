#!/usr/bin/env python3
"""
eSim Setup and Configuration Fix
This script fixes common setup issues with eSim application including:
1. Creating missing .esim directory
2. Setting up workspace configuration
3. Creating default workspace directory
4. Fixing file permissions
"""

import os
import sys
from pathlib import Path

def create_esim_config():
    """Create the .esim configuration directory and files"""
    try:
        # Get user home directory
        if os.name == 'nt':
            # Windows path handling (as per the original code)
            user_home = os.path.join('library', 'config')
        else:
            # Unix/Linux path handling
            user_home = os.path.expanduser('~')
        
        esim_config_dir = os.path.join(user_home, '.esim')
        
        # Create .esim directory if it doesn't exist
        if not os.path.exists(esim_config_dir):
            os.makedirs(esim_config_dir, exist_ok=True)
            print(f"✓ Created .esim configuration directory: {esim_config_dir}")
        else:
            print(f"✓ .esim directory already exists: {esim_config_dir}")
        
        # Create workspace.txt file if it doesn't exist
        workspace_file = os.path.join(esim_config_dir, 'workspace.txt')
        if not os.path.exists(workspace_file):
            with open(workspace_file, 'w') as f:
                f.write('1')  # Default value indicating workspace is set
            print(f"✓ Created workspace configuration: {workspace_file}")
        else:
            print(f"✓ Workspace configuration already exists: {workspace_file}")
        
        # Create default eSim workspace directory
        default_workspace = os.path.join(user_home, 'eSim-Workspace')
        if not os.path.exists(default_workspace):
            os.makedirs(default_workspace, exist_ok=True)
            print(f"✓ Created default workspace directory: {default_workspace}")
        else:
            print(f"✓ Default workspace directory already exists: {default_workspace}")
        
        # Set proper permissions (Unix/Linux only)
        if os.name != 'nt':
            os.chmod(esim_config_dir, 0o755)
            os.chmod(workspace_file, 0o644)
            if os.path.exists(default_workspace):
                os.chmod(default_workspace, 0o755)
            print("✓ Set proper file permissions")
        
        return True
        
    except Exception as e:
        print(f"✗ Error creating eSim configuration: {e}")
        return False

def check_dependencies():
    """Check if required Python packages are available"""
    missing_packages = []
    
    try:
        import PyQt5
        print("✓ PyQt5 is available")
    except ImportError:
        missing_packages.append("PyQt5")
        print("✗ PyQt5 is missing")
    
    try:
        from PyQt5 import QtGui, QtCore, QtWidgets
        print("✓ PyQt5 components are available")
    except ImportError:
        print("✗ PyQt5 components are missing or incomplete")
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Install them using: pip install " + " ".join(missing_packages))
        return False
    
    return True

def fix_application_py():
    """Provide suggested fix for the Application.py file"""
    fix_code = '''
# Add this function to your Workspace.py file in the createWorkspace method
# Before trying to open the workspace.txt file for writing:

def ensure_config_directory():
    """Ensure .esim configuration directory exists"""
    if os.name == 'nt':
        user_home = os.path.join('library', 'config')
    else:
        user_home = os.path.expanduser('~')
    
    esim_config_dir = os.path.join(user_home, '.esim')
    
    # Create directory if it doesn't exist
    if not os.path.exists(esim_config_dir):
        os.makedirs(esim_config_dir, exist_ok=True)
    
    return user_home

# Then modify your createWorkspace method to call this function first:
# user_home = ensure_config_directory()
# file = open(os.path.join(user_home, ".esim/workspace.txt"), 'w')
'''
    
    print("\n" + "="*60)
    print("SUGGESTED CODE FIX FOR WORKSPACE.PY:")
    print("="*60)
    print(fix_code)

def main():
    """Main function to run all fixes"""
    print("eSim Configuration Fix Tool")
    print("="*30)
    
    # Check Python version
    if sys.version_info < (3, 6):
        print("⚠️  Warning: Python 3.6+ recommended for eSim")
    
    # Check dependencies
    print("\n1. Checking dependencies...")
    deps_ok = check_dependencies()
    
    # Create configuration
    print("\n2. Setting up eSim configuration...")
    config_ok = create_esim_config()
    
    # Provide code fix suggestions
    print("\n3. Code fix suggestions...")
    fix_application_py()
    
    # Summary
    print("\n" + "="*60)
    print("SETUP SUMMARY:")
    print("="*60)
    
    if config_ok:
        print("✓ Configuration setup completed successfully")
        print("✓ You can now try running eSim again")
        
        if not deps_ok:
            print("⚠️  Some dependencies are missing - install them first")
        
        print("\nNext steps:")
        print("1. Apply the suggested code fix to Workspace.py")
        print("2. Run: python Application.py")
        
    else:
        print("✗ Configuration setup failed")
        print("Please check file permissions and try again")
    
    print("\nIf you still encounter issues:")
    print("- Check file permissions in your home directory")
    print("- Make sure you have write access to ~/.esim/")
    print("- Verify all Python dependencies are installed")

if __name__ == "__main__":
    main()
