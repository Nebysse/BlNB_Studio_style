import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path
from typing import Optional

def find_npm() -> Optional[str]:
    npm_path = shutil.which("npm")
    if npm_path:
        return npm_path
    
    if platform.system() == "Windows":
        common_paths = [
            Path(os.environ.get("ProgramFiles", "")) / "nodejs" / "npm.cmd",
            Path(os.environ.get("ProgramFiles(x86)", "")) / "nodejs" / "npm.cmd",
            Path.home() / "AppData" / "Roaming" / "npm" / "npm.cmd",
        ]
        for path in common_paths:
            if path.exists():
                return str(path)
    
    return None

def check_nodejs_installed() -> bool:
    try:
        result = subprocess.run(
            ["node", "--version"],
            capture_output=True,
            timeout=5,
            shell=True
        )
        return result.returncode == 0
    except:
        return False

def install_nodejs_windows() -> bool:
    try:
        import urllib.request
        import tempfile
        
        node_version = "20.11.0"
        arch = "x64" if platform.machine().endswith('64') else "x86"
        url = f"https://nodejs.org/dist/v{node_version}/node-v{node_version}-win-{arch}.msi"
        
        print(f"正在下载Node.js v{node_version}...")
        temp_dir = tempfile.gettempdir()
        msi_path = Path(temp_dir) / f"nodejs-{node_version}.msi"
        
        urllib.request.urlretrieve(url, str(msi_path))
        
        print("正在安装Node.js（静默模式）...")
        result = subprocess.run(
            [
                "msiexec",
                "/i", str(msi_path),
                "/quiet",
                "/norestart",
                "ADDLOCAL=ALL"
            ],
            timeout=300,
            shell=True
        )
        
        if result.returncode == 0:
            print("Node.js安装成功")
            msi_path.unlink(missing_ok=True)
            
            import time
            time.sleep(2)
            
            npm_path = find_npm()
            if npm_path:
                return True
        
        return False
    except Exception as e:
        print(f"安装Node.js失败: {e}")
        return False

def ensure_npm() -> Optional[str]:
    npm_path = find_npm()
    if npm_path:
        return npm_path
    
    if platform.system() == "Windows":
        if not check_nodejs_installed():
            print("未检测到Node.js，尝试自动安装...")
            if install_nodejs_windows():
                npm_path = find_npm()
                if npm_path:
                    return npm_path
        
        print("警告: 未找到npm，请手动安装Node.js: https://nodejs.org/")
        return None
    else:
        print("警告: 未找到npm，请手动安装Node.js: https://nodejs.org/")
        return None
