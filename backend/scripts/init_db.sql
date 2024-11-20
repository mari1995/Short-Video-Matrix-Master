-- 创建数据库
CREATE DATABASE IF NOT EXISTS shorts CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE shorts;

-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 创建视频分析表
CREATE TABLE IF NOT EXISTS video_analyses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    file_name VARCHAR(255),
    file_url VARCHAR(1024),
    status VARCHAR(50),
    duration FLOAT,
    frame_count INT,
    fps FLOAT,
    resolution VARCHAR(50),
    frames_data JSON,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 创建草稿箱表
CREATE TABLE IF NOT EXISTS drafts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(255),
    source_url VARCHAR(1024),
    file_url VARCHAR(1024),
    file_type VARCHAR(50),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 创建YouTube下载历史表
CREATE TABLE IF NOT EXISTS youtube_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    url VARCHAR(1024),
    title VARCHAR(255),
    author VARCHAR(255),
    duration INT,
    views BIGINT,
    thumbnail_url VARCHAR(1024),
    description TEXT,
    file_url VARCHAR(1024),
    file_size BIGINT,
    status VARCHAR(50) DEFAULT 'pending',
    error_message TEXT,
    is_shorts BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 创建视频生成表
CREATE TABLE IF NOT EXISTS video_generations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(255),
    status VARCHAR(50),
    duration FLOAT,
    transition VARCHAR(50),
    output_url VARCHAR(1024),
    error_message TEXT,
    source_images JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 创建操作日志表
CREATE TABLE IF NOT EXISTS operation_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    action VARCHAR(50),
    path VARCHAR(255),
    method VARCHAR(10),
    params TEXT,
    status_code INT,
    response TEXT,
    ip_address VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建系统配置表
CREATE TABLE IF NOT EXISTS system_configs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    config_key VARCHAR(255) NOT NULL UNIQUE,
    config_value TEXT,
    description TEXT,
    is_secret BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 插入默认管理员用户
INSERT INTO users (username, email, hashed_password, is_active, is_superuser)
VALUES ('admin', 'admin@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', TRUE, TRUE)
,('a', 'a@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', TRUE, TRUE);


-- 插入默认系统配置
INSERT INTO system_configs (user_id, config_key, config_value, description, is_secret)
VALUES 
    (1, 'openapi_base_url', 'https://api.cinfohubs.buzz', 'API基础URL', FALSE)
;

INSERT INTO system_configs (user_id, config_key, config_value, description, is_secret)
VALUES 
    (1, 'openapi_api_key', 'sk-qiRbJ62llvdWtFPF74B4C398B0D049A4A5B001E9B1C18e4f', 'API密钥', FALSE)
;