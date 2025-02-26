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

# 添加智能分段过滤器
@app.template_filter('smart_paragraphs')
def smart_paragraphs(text):
    if not text:
        return ''
    
    # 处理原始文本中的换行
    paragraphs = text.split('\n')
    
    # 过滤空白段落并添加适当的HTML标签
    formatted_paragraphs = []
    for p in paragraphs:
        p = p.strip()
        if p:  # 只处理非空段落
            # 为段落添加<p>标签
            formatted_p = f'<p>{p}</p>'
            formatted_paragraphs.append(formatted_p)
    
    # 将所有段落连接起来
    return '\n'.join(formatted_paragraphs)

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

@app.route('/')
def index():
    posts = get_bitable_records()
    logger.info(f"获取到的数据结构：{posts}")
    # 根据发布时间对文章进行排序
    sorted_posts = sorted(posts, key=lambda x: x.get('fields', {}).get('发布时间', ''), reverse=True)
    return render_template('index.html', posts=sorted_posts)

@app.route('/post/<record_id>')
def post_detail(record_id):
    posts = get_bitable_records()
    post = next((post for post in posts if post.get('record_id') == record_id), None)
    if post is None:
        return '文章不存在', 404
    return render_template('detail.html', post=post)

@app.route('/works')
def works():
    return render_template('works.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

if __name__ == '__main__':
    app.run(debug=True)