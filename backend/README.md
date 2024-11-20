### 后端
![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-009688?style=flat-square&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=flat-square&logo=python)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?style=flat-square&logo=mysql)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-D71F00?style=flat-square)

## 数据库迁移

1. 初始化数据库
```bash
mysql -u root -p < scripts/init_db.sql
```

2. 使用 Alembic 进行迁移
```bash
alembic revision --autogenerate -m "initial"
alembic upgrade head
``` 