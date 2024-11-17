#!/bin/bash

# 创建虚拟环境
python3.10 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install --upgrade pip
pip install -r requirements.txt

# 创建必要的目录
mkdir -p app/static
mkdir -p app/logs

# 初始化数据库
alembic upgrade head 