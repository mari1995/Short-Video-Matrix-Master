import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.db.base import SessionLocal
from app.db.models.user import User
from app.core.security import get_password_hash
from loguru import logger

def change_admin_password(new_password: str):
    db = SessionLocal()
    try:
        # 查找admin用户
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            logger.error("Admin user not found")
            return False
        
        # 获取原密码哈希（用于日志）
        old_hash = admin.hashed_password
        
        # 更新密码
        admin.hashed_password = get_password_hash(new_password)
        db.commit()
        
        # 验证更新是否成功
        admin = db.query(User).filter(User.username == "admin").first()
        if admin.hashed_password != old_hash:
            logger.success(f"Successfully changed admin password")
            return True
        else:
            logger.error("Password update failed - hash didn't change")
            return False
    
    except Exception as e:
        logger.error(f"Error changing password: {str(e)}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    try:
        # 忽略 bcrypt 版本警告
        import warnings
        warnings.filterwarnings("ignore", category=UserWarning)
        
        success = change_admin_password("qwer")
        if success:
            print("Password changed successfully!")
            sys.exit(0)
        else:
            print("Failed to change password!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1) 