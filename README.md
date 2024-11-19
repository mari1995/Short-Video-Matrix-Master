# Short-Video-Matrix-Master

Short-Video-Matrix-Master是一个现代化的管理平台，基于 **Vue + Element UI + FastAPI + SQLite** 构建，旨在提供高效、灵活的短视频矩阵管理解决方案。

## 技术栈

### 前端
![Vue.js](https://img.shields.io/badge/Vue.js-2.x-4FC08D?style=flat-square&logo=vue.js)
![Element UI](https://img.shields.io/badge/Element_UI-2.x-409EFF?style=flat-square&logo=element)
![Vuex](https://img.shields.io/badge/Vuex-3.x-4FC08D?style=flat-square&logo=vue.js)
![Vue Router](https://img.shields.io/badge/Vue_Router-3.x-4FC08D?style=flat-square&logo=vue.js)
![Axios](https://img.shields.io/badge/Axios-1.x-5A29E4?style=flat-square&logo=axios)
![Node.js](https://img.shields.io/badge/Node.js-v18-339933?style=flat-square&logo=node.js)
![NPM](https://img.shields.io/badge/NPM-v6+-CB3837?style=flat-square&logo=npm)

### 后端
![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-009688?style=flat-square&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=flat-square&logo=python)
![SQLite](https://img.shields.io/badge/SQLite-3.x-003B57?style=flat-square&logo=sqlite)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-D71F00?style=flat-square)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-5C3EE8?style=flat-square&logo=opencv)
![JWT](https://img.shields.io/badge/JWT-Auth-000000?style=flat-square&logo=json-web-tokens)

## 功能特点

- **视频功能**
  - YouTube视频下载：支持视频和Shorts下载
  - 视频分析：自动提取关键帧并分析
  - 视频剪辑：支持图片生成视频
  - 图片分析：支持图片内容描述生成
  
- **文件管理**
  - 文件管理器：统一管理上传的文件
  - 草稿箱：临时存储和管理素材
  - 批量操作：支持批量上传和下载
  
- **系统功能**
  - 用户认证：JWT token认证
  - 系统配置：灵活的配置管理
  - 操作日志：详细的请求响应日志
  - 跨域支持：完整的CORS配置

## 开发环境

1. 前端开发
```bash
cd frontend
npm install
npm run serve
```

2. 后端开发
```bash
cd backend
pip install -r requirements.txt
python debug.py
```

## API文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 主要功能模块

1. **视频分析** 📹
   - 关键帧提取
   - 图片内容分析
   - 视频信息统计

2. **YouTube下载** ⬇️
   - 视频信息获取
   - 下载进度显示
   - 历史记录管理

3. **文件管理** 📁
   - 文件上传下载
   - 目录浏览
   - 文件预览

4. **系统管理** ⚙️
   - 用户认证
   - 系统配置
   - 日志记录

## 开发指南

1. **环境要求** 🔧
   - Node.js >= 18
   - Python >= 3.10
   - SQLite 3

2. **配置说明** ⚙️
   - 前端配置: .env.development
   - 后端配置: app/core/config.py

3. **开发建议** 💡
   - 遵循 RESTful API 设计规范
   - 使用统一的错误处理机制
   - 保持代码风格一致

## 许可证

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)