from sqlalchemy.orm import Session
from app.core.security import get_password_hash
from app.db.models.user import User
from app.core.config import settings

def init_db(db: Session) -> None:
    user = db.query(User).filter(User.username == "admin").first()
    if not user:
        user = User(
            username="admin",
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            full_name="Administrator",
            is_superuser=True,
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user) 