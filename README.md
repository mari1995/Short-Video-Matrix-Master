# 通用管理后台系统

基于 Vue + Element UI + FastAPI + SQLite 的现代化管理后台系统。

## 技术栈

### 前端
- Vue.js 2.x
- Element UI
- Axios
- Vue Router
- Vuex

### 后端
- FastAPI
- SQLite
- SQLAlchemy
- JWT认证
- Pydantic

## 项目结构
```
project/
├── frontend/ # 前端项目目录
│ ├── src/
│ │ ├── api/ # API 接口
│ │ ├── assets/ # 静态资源
│ │ ├── components/ # 公共组件
│ │ ├── layout/ # 布局组件
│ │ ├── router/ # 路由配置
│ │ ├── store/ # Vuex状态管理
│ │ ├── utils/ # 工具函数
│ │ ├── views/ # 页面视图
│ │ ├── App.vue # 根组件
│ │ └── main.js # 入口文件
│ └── package.json
│
├── backend/ # 后端项目目录
│ ├── app/
│ │ ├── api/ # API路由
│ │ ├── core/ # 核心配置
│ │ ├── crud/ # CRUD操作
│ │ ├── db/ # 数据库模型
│ │ ├── schemas/ # Pydantic模型
│ │ └── utils/ # 工具函数
│ ├── tests/ # 测试文件
│ ├── alembic/ # 数据库迁���
│ └── requirements.txt # 依赖包
│
└── README.md # 项目说明文档 
```

## 主要功能

### 1. 用户认证
- 登录/登出
- JWT token认证
- 权限控制

### 2. 用户管理
- 用户列表
- 用户添加/编辑/删除
- 角色分配

### 3. 系统监控
- 系统大盘数据
- 访问统计
- 操作日志

### 4. 个人中心
- 个人信息查看
- 密码修改
- 基本设置

## 开发环境搭建

### 前端
```bash
进入前端目录
cd frontend
安装依赖
npm install
启动开发服务器
npm run serve
```


### 后端
```bash
进入后端目录
cd backend
创建虚拟环境
python -m venv venv
激活虚拟环境
source venv/bin/activate # Linux/Mac
venv\Scripts\activate # Windows
安装依赖
pip install -r requirements.txt
启动服务器
uvicorn app.main:app --reload
```


## API文档
启动后端服务后，访问 http://localhost:8000/docs 查看Swagger API文档。

## 数据库
系统使用SQLite作为数据库，数据文件位于 `backend/app.db`。

## 贡献指南
1. Fork 本仓库
2. 创建新的分支
3. 提交更改
4. 发起 Pull Request

## 许可证
MIT License#   S h o r t - V i d e o - M a t r i x - M a s t e r  
 