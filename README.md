# reGeo - 批量地理编码工具

基于高德地图API开发的经纬度逆向地理编码工具，支持批量坐标解析为结构化地址信息。

## 功能特性
- 🗺️ 批量处理经纬度坐标（支持50+组/次）
- 🔑 本地存储API密钥（通过<mcsymbol name="saveApiKey" filename="index.html" path="/Users/huxingwang/WorkSpace/reGeo/templates/index.html" startline="54" type="function"></mcsymbol>实现安全存储）
- 🛡️ 自动过滤无效坐标（通过<mcsymbol name="geocode" filename="app.py" path="/Users/huxingwang/WorkSpace/reGeo/app.py" startline="79" type="function"></mcsymbol>的空行过滤）
- 📊 结构化展示解析结果（省/市/区三级地址信息）

## 技术栈
- 前端：HTML5 / CSS3 / JavaScript
- 后端：Python Flask
- 地图服务：高德地图Web服务API

## 快速开始

- 根目录下
- # 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 运行
python3 app.py
