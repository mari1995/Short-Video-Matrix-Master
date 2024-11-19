from fastapi import APIRouter, HTTPException, Depends, Request, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.db.models.draft import Draft
from typing import List
from datetime import datetime
import shutil
from pathlib import Path

router = APIRouter()

DRAFTS_UPLOAD_DIR = Path("static/uploads/drafts")

def ensure_dirs():
    """确保必要的目录存在"""
    DRAFTS_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload")
async def upload_draft(
    request: Request,
    file: UploadFile = File(...),
    title: str = None,
    description: str = None,
    db: Session = Depends(get_db)
):
    """上传草稿"""
    ensure_dirs()
    
    try:
        # 生成文件名
        file_ext = file.filename.split('.')[-1]
        file_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file_ext}"
        file_path = DRAFTS_UPLOAD_DIR / file_name
        
        # 保存文件
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 生成完整URL
        file_url = f"http://127.0.0.1:8000/static/uploads/drafts/{file_name}"
        
        # 创建草稿记录
        draft = Draft(
            title=title or file.filename,
            file_url=file_url,  # 存储完整URL
            file_type='image',
            description=description
        )
        db.add(draft)
        db.commit()
        db.refresh(draft)
        
        return draft.serialize()
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/list")
async def list_drafts(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """获取草稿箱列表"""
    total = db.query(Draft).count()
    drafts = db.query(Draft)\
        .order_by(Draft.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    return {
        "total": total,
        "items": [item.serialize() for item in drafts]
    }

@router.delete("/{draft_id}")
async def delete_draft(draft_id: int, db: Session = Depends(get_db)):
    """删除草稿"""
    draft = db.query(Draft).get(draft_id)
    if not draft:
        raise HTTPException(status_code=404, detail="Draft not found")
        
    # 从URL中提取文件名并删除文件
    try:
        file_name = draft.file_url.split('/')[-1]
        file_path = DRAFTS_UPLOAD_DIR / file_name
        file_path.unlink(missing_ok=True)
    except Exception as e:
        print(f"Error deleting file: {e}")
    
    db.delete(draft)
    db.commit()
    return {"message": "Draft deleted successfully"}

@router.post("/add-by-url")
async def add_draft_by_url(
    request: Request,
    source_url: str = Form(...),
    title: str = Form(...),
    description: str = Form(None),
    db: Session = Depends(get_db)
):
    """通过URL添加到草稿箱"""
    try:
        # 创建草稿记录
        draft = Draft(
            title=title,
            source_url=source_url,  # 原始URL
            file_url=source_url,    # 直接使用原始URL
            file_type='image',
            description=description
        )
        db.add(draft)
        db.commit()
        db.refresh(draft)
        
        return draft.serialize()
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 