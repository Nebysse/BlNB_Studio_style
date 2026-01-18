import os
import sys
import subprocess
import threading
from pathlib import Path
from typing import Optional

def get_addon_path() -> Path:
    try:
        import addon_utils
        package_name = __package__.split('.')[0] if '.' in __package__ else __package__ if __package__ else "Blender Studio-Style"
        for mod in addon_utils.modules():
            if mod.__name__ == package_name:
                return Path(mod.__file__).parent
    except:
        pass
    return Path(__file__).parent.parent

def get_venv_path() -> Path:
    addon_path = get_addon_path()
    return addon_path / ".venv"

def create_venv() -> bool:
    venv_path = get_venv_path()
    if venv_path.exists():
        return True
    
    try:
        python_exe = sys.executable
        subprocess.run([python_exe, "-m", "venv", str(venv_path)], check=True, capture_output=True)
        return True
    except Exception:
        return False

def get_venv_python() -> Optional[Path]:
    venv_path = get_venv_path()
    if sys.platform == "win32":
        python_exe = venv_path / "Scripts" / "python.exe"
    else:
        python_exe = venv_path / "bin" / "python"
    
    if python_exe.exists():
        return python_exe
    return None

def install_package(package: str) -> bool:
    venv_python = get_venv_python()
    if not venv_python:
        return False
    
    try:
        subprocess.run([str(venv_python), "-m", "pip", "install", package], 
                      check=True, capture_output=True, timeout=60)
        return True
    except Exception:
        return False

def ensure_dependencies():
    venv_python = get_venv_python()
    if not venv_python:
        if not create_venv():
            return False
        venv_python = get_venv_python()
        if not venv_python:
            return False
    
    packages = ["fastapi", "uvicorn[standard]", "pydantic"]
    for package in packages:
        try:
            subprocess.run([str(venv_python), "-m", "pip", "show", package], 
                          check=True, capture_output=True)
        except subprocess.CalledProcessError:
            install_package(package)
    
    return True
