from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt

# 配置密码哈希
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 配置密钥和算法
SECRET_KEY = "your-secret-key-here"  # 在生产环境中应该使用环境变量
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 小时

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """获取密码哈希值"""
    return pwd_context.hash(password)

def create_access_token(user_id: int, expires_delta: Optional[timedelta] = None):
    """
    创建访问令牌
    :param user_id: 用户ID
    :param expires_delta: 过期时间增量
    :return: 编码后的JWT令牌
    """
    to_encode = {"sub": str(user_id)}  # 使用用户ID作为subject
    
    # 设置过期时间
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
    # 添加过期时间到令牌数据
    to_encode.update({"exp": expire})
    
    # 创建JWT令牌
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def verify_token(token: str) -> Optional[int]:
    """
    验证令牌
    :param token: JWT令牌
    :return: 用户ID或None
    """
    try:
        # 解码并验证令牌
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))  # 获取用户ID
        return user_id
    except (JWTError, ValueError):
        return None