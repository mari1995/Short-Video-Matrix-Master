from fastapi import APIRouter, HTTPException
from typing import List, Dict
import os
from pathlib import Path

router = APIRouter()

def get_file_info(path: Path) -> Dict:
    """获取文件信息"""
    stat = path.stat()
    return {
        "name": path.name,
        "path": str(path),
        "size": stat.st_size,
        "is_dir": path.is_dir(),
        "modified_time": stat.st_mtime,
        "created_time": stat.st_ctime
    }

@router.get("/list")
async def list_files(path: str = "static"):
    """列出目录内容"""
    try:
        base_path = Path(path)
        if not base_path.exists():
            raise HTTPException(status_code=404, detail="Path not found")
        
        items = []
        for item in base_path.iterdir():
            try:
                items.append(get_file_info(item))
            except Exception as e:
                continue  # 跳过无法访问的文件
        
        # 按类型和名称排序
        items.sort(key=lambda x: (not x["is_dir"], x["name"].lower()))
        
        return {
            "current_path": str(base_path),
            "parent_path": str(base_path.parent) if str(base_path.parent).startswith("static") else None,
            "items": items
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/delete")
async def delete_file(path: str):
    """删除文件或目录"""
    try:
        file_path = Path(path)
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        if not str(file_path).startswith("static"):
            raise HTTPException(status_code=403, detail="Access denied")
        
        if file_path.is_dir():
            import shutil
            shutil.rmtree(str(file_path))
        else:
            file_path.unlink()
        
        return {"message": "Deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 