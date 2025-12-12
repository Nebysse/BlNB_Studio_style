import re
from pathlib import Path
from typing import Tuple, Optional, List

ASSET_STAGES = {
    "model": "模型阶段",
    "rig": "绑定阶段",
    "texture": "贴图阶段",
    "shader": "材质阶段",
    "setup": "设置阶段",
}

ASSET_TASKS = {
    "model": "模型",
    "rig": "绑定",
    "texture": "贴图",
    "shader": "材质",
    "setup": "设置",
}

SHOT_STAGES = {
    "layout": "布局阶段",
    "anim": "动画阶段",
    "lighting": "灯光阶段",
    "comp": "合成阶段",
    "fx": "特效阶段",
}

SHOT_TASKS = {
    "layout": "布局",
    "anim": "动画",
    "lighting": "灯光",
    "comp": "合成",
    "fx": "特效",
}

FORBIDDEN_ASSET_TASKS = {"layout", "anim", "lighting", "comp"}

def parse_filename(filename: str) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str], Optional[str]]:
    name = Path(filename).stem
    pattern_with_task = r"^([a-z_]+)_([a-z_]+)_([a-z_]+)_v(\d+)$"
    pattern_without_task = r"^([a-z_]+)_v(\d+)$"
    
    match_with_task = re.match(pattern_with_task, name)
    if match_with_task:
        scope = match_with_task.group(1)
        subject = match_with_task.group(2)
        task = match_with_task.group(3)
        version = match_with_task.group(4)
        return scope, subject, task, version, None
    
    match_without_task = re.match(pattern_without_task, name)
    if match_without_task:
        subject = match_without_task.group(1)
        version = match_without_task.group(2)
        return None, subject, None, version, None
    
    return None, None, None, None, f"文件名格式无效: {filename}"

def validate_asset_filename(filename: str) -> Tuple[bool, Optional[str]]:
    scope, subject, task, version, error = parse_filename(filename)
    if error:
        return False, error
    
    if not subject:
        return False, "文件名缺少 subject 部分"
    
    if task in FORBIDDEN_ASSET_TASKS:
        return False, f"Asset 文件禁止使用 task '{task}'，该 task 仅用于 Shot 文件"
    
    if task and task not in ASSET_TASKS:
        return False, f"未知的 Asset task: '{task}'，允许的 task: {', '.join(ASSET_TASKS.keys())}"
    
    return True, None

def validate_shot_filename(filename: str) -> Tuple[bool, Optional[str]]:
    scope, subject, task, version, error = parse_filename(filename)
    if error:
        return False, error
    
    if not scope or scope != "shot":
        return False, f"Shot 文件名必须以 'shot' 开头，当前 scope: {scope}"
    
    if not task:
        return False, "Shot 文件必须包含 task（stage），格式: shot_{shot_id}_{task}_v###.blend"
    
    if task not in SHOT_TASKS:
        return False, f"未知的 Shot task: '{task}'，允许的 task: {', '.join(SHOT_TASKS.keys())}"
    
    return True, None

def generate_asset_filename(asset_id: str, task: Optional[str] = None, version: int = 1) -> str:
    if task:
        if task in FORBIDDEN_ASSET_TASKS:
            raise ValueError(f"Asset 文件禁止使用 task '{task}'")
        if task not in ASSET_TASKS:
            raise ValueError(f"未知的 Asset task: '{task}'")
        return f"{asset_id}_{task}_v{version:03d}.blend"
    return f"{asset_id}_v{version:03d}.blend"

def generate_shot_filename(shot_id: str, task: str, version: int = 1) -> str:
    if task not in SHOT_TASKS:
        raise ValueError(f"未知的 Shot task: '{task}'，允许的 task: {', '.join(SHOT_TASKS.keys())}")
    return f"shot_{shot_id}_{task}_v{version:03d}.blend"

def detect_domain_from_path(file_path: Path) -> Optional[str]:
    path_str = str(file_path).replace("\\", "/")
    if "/01_assets/" in path_str:
        return "asset"
    elif "/02_shots/" in path_str:
        return "shot"
    return None

def validate_filename_by_domain(filename: str, domain: Optional[str] = None, file_path: Optional[Path] = None) -> Tuple[bool, Optional[str]]:
    if domain is None:
        if file_path:
            domain = detect_domain_from_path(file_path)
        else:
            return False, "无法确定文件域，请提供 domain 或 file_path"
    
    if domain == "asset":
        return validate_asset_filename(filename)
    elif domain == "shot":
        return validate_shot_filename(filename)
    else:
        return False, f"未知的域: {domain}"

