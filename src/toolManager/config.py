#!/usr/bin/env python3
"""
Configuration and State Management for eSim Tool Manager.
Standardizes access to information.json and other settings.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Optional, Any
from datetime import datetime

# Import local paths helper with robust fallback

def get_install_state_path():
    return Path(__file__).resolve().parent / "information.json"

logger = logging.getLogger(__name__)


class ConfigManager:
    """
    Handles persistence of tool installation states and manager settings.
    """

    def __init__(self, config_path: Optional[Path] = None, autosave: bool = True):
        self.config_path = config_path or get_install_state_path()
        self.autosave = autosave
        self._data: Dict[str, Any] = self._load_defaults()
        self.load()

    def _load_defaults(self) -> Dict[str, Any]:
        """Returns the default schema for the configuration file."""
        return {
            "important_packages": [],
            "settings": {
                "last_update_check": None,
                "preferred_category": "analog",
                "auto_refresh": True
            },
            "metadata": {
                "schema_version": "1.0.0",
                "created_at": datetime.now().isoformat(),
                "last_modified": datetime.now().isoformat()
            }
        }

    def load(self) -> bool:
        """Loads configuration from the JSON file."""
        if not self.config_path.exists():
            return False
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)
                # Basic merge to ensure schema consistency
                if isinstance(loaded_data, dict):
                    self._data.update(loaded_data)
                return True
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Failed to load config from {self.config_path}: {e}")
            return False

    def save(self) -> bool:
        """Saves current state to the JSON file atomically."""
        try:
            # Update metadata
            if "metadata" not in self._data:
                self._data["metadata"] = {}
            self._data["metadata"]["last_modified"] = datetime.now().isoformat()

            # Ensure directory exists
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write to a temporary file first for atomicity
            temp_path = self.config_path.with_suffix(".tmp")
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(self._data, f, indent=4)
            
            # Replace original file with temporary one
            # On Windows, replace() can fail if destination is open, but this is 
            # the standard way for atomic-like writes in Python.
            temp_path.replace(self.config_path)
            return True
        except IOError as e:
            logger.error(f"Failed to save config to {self.config_path}: {e}")
            return False

    def get_tool_state(self, tool_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves the installation state for a specific tool."""
        packages = self._data.get("important_packages", [])
        for pkg in packages:
            if pkg.get("package_name") == tool_id:
                return pkg
        return None

    def update_tool_state(self, tool_id: str, version: str, status: str = "installed") -> None:
        """Updates or adds an entry for a tool's installation state."""
        packages = self._data.get("important_packages", [])
        found = False
        
        for pkg in packages:
            if pkg.get("package_name") == tool_id:
                pkg["version"] = version
                pkg["status"] = status
                pkg["installed_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                found = True
                break
        
        if not found:
            packages.append({
                "package_name": tool_id,
                "version": version,
                "status": status,
                "installed_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        
        self._data["important_packages"] = packages
        if self.autosave:
            self.save()

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Retrieves a specific setting from the manager configuration."""
        return self._data.get("settings", {}).get(key, default)

    def set_setting(self, key: str, value: Any) -> None:
        """Updates a manager setting."""
        if "settings" not in self._data:
            self._data["settings"] = {}
        self._data["settings"][key] = value
        if self.autosave:
            self.save()

    @property
    def data(self) -> Dict[str, Any]:
        """Returns the raw configuration data."""
        return self._data
