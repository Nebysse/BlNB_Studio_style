import os
import sys
import threading
import socket
from pathlib import Path
from typing import Optional

try:
    import bpy
except ImportError:
    bpy = None

from .core import venv_manager, detector, metadata, generator, npm_manager

_server_thread = None
_server_port = None
_project_state = {}

def find_free_port(start_port=5000, max_port=5100):
    for port in range(start_port, max_port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('127.0.0.1', port))
                return port
            except OSError:
                continue
    return None

def create_app():
    venv_python = venv_manager.get_venv_python()
    if not venv_python:
        return None
    
    addon_path = Path(__file__).parent
    port = find_free_port()
    if not port:
        return None
    
    app_code = f"""import os
import json
import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

sys.path.insert(0, r'{addon_path}')

app = FastAPI(title="Blender Studio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

project_state: Dict[str, Any] = {{}}

class ProjectStateUpdate(BaseModel):
    filepath: Optional[str] = None
    filename: Optional[str] = None
    project_root: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    object_count: Optional[int] = None
    scenes: Optional[List[str]] = None

class ProjectInit(BaseModel):
    base_path: str
    project_code: str
    project_type: str = "single_shot"
    author_name: str = ""
    studio: str = ""
    role: str = ""
    contact: str = ""
    copyright: str = ""

@app.get("/api/project/state")
async def get_project_state():
    return project_state

@app.post("/api/project/state")
async def update_project_state(state: ProjectStateUpdate):
    project_state.update(state.model_dump(exclude_none=True))
    return {{"status": "updated"}}

@app.get("/api/project/info")
async def get_project_info():
    try:
        if project_state.get('project_root'):
            from core import metadata
            project_root = Path(project_state['project_root'])
            project_meta = metadata.read_project_metadata(project_root)
            return {{
                "project_root": str(project_root),
                "metadata": project_meta or {{}},
                "exists": True,
                **project_state
            }}
        
        from core import detector, metadata
        project_root = detector.find_project_root()
        if not project_root:
            raise HTTPException(status_code=404, detail="未找到项目根目录")
        
        project_meta = metadata.read_project_metadata(project_root)
        
        return {{
            "project_root": str(project_root),
            "metadata": project_meta or {{}},
            "exists": True
        }}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/files/list")
async def list_files(path: str = ""):
    try:
        from core import detector
        
        project_root = None
        if project_state.get('project_root'):
            project_root = Path(project_state['project_root'])
        else:
            project_root = detector.find_project_root()
        
        if not project_root:
            raise HTTPException(status_code=404, detail="未找到项目根目录")
        
        if path:
            target_path = project_root / path
            if not str(target_path.resolve()).startswith(str(project_root.resolve())):
                raise HTTPException(status_code=403, detail="路径超出项目范围")
        else:
            target_path = project_root
        
        if not target_path.exists():
            raise HTTPException(status_code=404, detail="路径不存在")
        
        files = []
        for item in sorted(target_path.iterdir()):
            try:
                rel_path = item.relative_to(project_root)
                files.append({{
                    "name": item.name,
                    "path": str(rel_path),
                    "is_dir": item.is_dir(),
                    "size": item.stat().st_size if item.is_file() else 0
                }})
            except:
                continue
        
        return {{
            "path": str(target_path.relative_to(project_root)) if target_path != project_root else "",
            "files": files
        }}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/blend/info")
async def get_blend_info():
    try:
        try:
            import bpy
            if bpy and bpy.data.filepath:
                file_path = Path(bpy.data.filepath)
                return {{
                    "filepath": str(file_path),
                    "filename": file_path.name,
                    "exists": file_path.exists(),
                    "size": file_path.stat().st_size if file_path.exists() else 0
                }}
        except:
            pass
        
        raise HTTPException(status_code=404, detail="未打开文件或无法访问Blender")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/project/init")
async def init_project(init_data: ProjectInit):
    try:
        from core import generator, metadata
        
        if not init_data.base_path or not init_data.project_code:
            raise HTTPException(status_code=400, detail="缺少必要参数")
        
        success, result = generator.create_project(
            init_data.base_path, 
            init_data.project_code, 
            init_data.project_type
        )
        
        if success:
            project_root = Path(result)
            metadata.write_project_metadata(
                project_root=project_root,
                author_name=init_data.author_name,
                studio=init_data.studio,
                role=init_data.role,
                contact=init_data.contact,
                project_code=init_data.project_code,
                project_type=init_data.project_type,
                copyright=init_data.copyright
            )
            return {{
                "success": True,
                "project_root": result
            }}
        else:
            raise HTTPException(status_code=400, detail=result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    port = {port}
    print(f"FastAPI服务器启动在 http://127.0.0.1:{{port}}")
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="info")
"""
    
    script_path = addon_path / ".web_server.py"
    script_path.write_text(app_code, encoding='utf-8')
    
    return venv_python, script_path, port

def start_server():
    global _server_thread, _server_port
    
    if _server_thread and _server_thread.is_alive():
        return _server_port
    
    if not venv_manager.ensure_dependencies():
        return None
    
    result = create_app()
    if not result:
        return None
    
    venv_python, script_path, port = result
    
    _server_port = port
    
    def run_server():
        import subprocess
        env = os.environ.copy()
        env['PYTHONPATH'] = str(Path(__file__).parent)
        subprocess.run([str(venv_python), str(script_path)], env=env)
    
    _server_thread = threading.Thread(target=run_server, daemon=True)
    _server_thread.start()
    
    web_path = Path(__file__).parent / "web"
    if (web_path / "package.json").exists():
        def run_nextjs():
            import subprocess
            import time
            time.sleep(3)
            
            npm_cmd = npm_manager.ensure_npm()
            if not npm_cmd:
                print("警告: 未找到npm命令，跳过Next.js启动")
                print("提示: 请安装Node.js后重启插件: https://nodejs.org/")
                return
            
            env = os.environ.copy()
            env['API_BASE'] = f'http://127.0.0.1:{port}'
            
            web_path_str = str(web_path.resolve())
            
            if not (web_path / "node_modules").exists():
                print("安装Next.js依赖...")
                result = subprocess.run(
                    [npm_cmd, "install"],
                    cwd=web_path_str,
                    env=env,
                    shell=True,
                    timeout=300
                )
                if result.returncode != 0:
                    print("依赖安装失败，请检查网络连接")
                    return
            
            print("启动Next.js开发服务器...")
            subprocess.run(
                [npm_cmd, "run", "dev"],
                cwd=web_path_str,
                env=env,
                shell=True
            )
        
        nextjs_thread = threading.Thread(target=run_nextjs, daemon=True)
        nextjs_thread.start()
    
    import time
    time.sleep(2)
    
    return port

def stop_server():
    global _server_thread
    _server_thread = None

def get_server_port():
    return _server_port

def update_project_state(state):
    import requests
    port = get_server_port()
    if port:
        try:
            requests.post(f"http://127.0.0.1:{port}/api/project/state", json=state, timeout=1)
        except:
            pass
