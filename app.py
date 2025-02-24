from flask import Flask, render_template
from datetime import datetime
import requests
import logging
from feishu_config import *

app = Flask(__name__)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 添加datetime过滤器
@app.template_filter('datetime')
def format_datetime(value):
    if not value:
        return ''
    if isinstance(value, dict):
        value = value.get('value', '')
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            try:
                value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S+08:00')
            except ValueError:
                return value
    return value.strftime('%Y-%m-%d %H:%M')

def get_tenant_access_token():
    url = FEISHU_HOST + TENANT_ACCESS_TOKEN_URI
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "app_id": APP_ID,
        "app_secret": APP_SECRET
    }
    try:
        logger.info(f"正在获取tenant_access_token，使用APP_ID: {APP_ID}")
        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()
        if 'tenant_access_token' not in response_data:
            logger.error(f"获取tenant_access_token失败：{response_data}")
            return None
        logger.info("成功获取tenant_access_token")
        return response_data["tenant_access_token"]
    except Exception as e:
        logger.error(f"获取tenant_access_token时发生错误：{str(e)}")
        return None

def get_bitable_records():
    token = get_tenant_access_token()
    if not token:
        logger.error("无法获取tenant_access_token，返回空列表")
        return []
    
    url = FEISHU_HOST + BITABLE_URI.format(BASE_ID, TABLE_ID)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    try:
        logger.info(f"正在获取多维表格数据，BASE_ID: {BASE_ID}, TABLE_ID: {TABLE_ID}")
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            items = data.get("data", {}).get("items", [])
            logger.info(f"成功获取到{len(items)}条记录")
            return items
        else:
            logger.error(f"获取多维表格数据失败，状态码：{response.status_code}，响应：{response.text}")
            return []
    except Exception as e:
        logger.error(f"获取多维表格数据时发生错误：{str(e)}")
        return []

def get_bitable_record(record_id):
    token = get_tenant_access_token()
    if not token:
        logger.error("无法获取tenant_access_token，返回None")
        return None
    
    url = FEISHU_HOST + BITABLE_URI.format(BASE_ID, TABLE_ID) + f"/{record_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    try:
        logger.info(f"正在获取文章数据，record_id: {record_id}")
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            item = data.get("data", {})
            logger.info(f"成功获取文章数据：{item}")
            return item
        else:
            logger.error(f"获取文章数据失败，状态码：{response.status_code}，响应：{response.text}")
            return None
    except Exception as e:
        logger.error(f"获取文章数据时发生错误：{str(e)}")
        return None

@app.route('/')
def index():
    posts = get_bitable_records()
    logger.info(f"获取到的数据结构：{posts}")
    return render_template('index.html', posts=posts)

@app.route('/detail/<post_id>')
def detail(post_id):
    post = get_bitable_record(post_id)
    if post is None:
        return "文章不存在", 404
    return render_template('detail.html', post=post)

@app.route('/categories')
def categories():
    posts = get_bitable_records()
    # 根据文章标签或分类字段组织分类数据
    categories_dict = {}
    for post in posts:
        category_name = post.fields.get('分类', '未分类')
        if category_name not in categories_dict:
            categories_dict[category_name] = {
                'name': category_name,
                'posts': []
            }
        categories_dict[category_name]['posts'].append(post)
    
    return render_template('categories.html', categories=list(categories_dict.values()))

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)