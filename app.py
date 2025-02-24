import requests
import re
from flask import Flask, render_template, jsonify
from flask_caching import Cache
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
cache = Cache(app)

class FeishuAPI:
    def __init__(self):
        self.app_id = app.config['FEISHU_APP_ID']
        self.app_secret = app.config['FEISHU_APP_SECRET']
        self.base_id = app.config['BASE_ID']
        self.table_id = app.config['TABLE_ID']
        self.access_token = None

    def get_access_token(self):
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        headers = {"Content-Type": "application/json"}
        data = {"app_id": self.app_id, "app_secret": self.app_secret}
        response = requests.post(url, headers=headers, json=data)
        return response.json()["tenant_access_token"]

    def clean_text(self, text):
        if not text:
            return ''
        # 移除类似 [{'text': '内容', 'type': 'text'}] 的格式
        try:
            if isinstance(text, list):
                cleaned = ''
                for item in text:
                    if isinstance(item, dict) and 'text' in item:
                        cleaned += item['text']
                text = cleaned
        except:
            pass
        return text

    def get_table_records(self):
        if not self.access_token:
            self.access_token = self.get_access_token()

        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.base_id}/tables/{self.table_id}/records"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        records = response.json()["data"]["items"]
        
        # 清理每条记录中的文本
        for record in records:
            for field in record['fields']:
                record['fields'][field] = self.clean_text(record['fields'][field])
        return records

feishu_api = FeishuAPI()

@app.route('/')
@cache.cached(timeout=300)
def index():
    try:
        records = feishu_api.get_table_records()
        articles = [{
            'id': record['record_id'],
            'title': record['fields'].get('标题', '无标题'),
            'quote': record['fields'].get('金句', ''),
            'summary': record['fields'].get('摘要', '')[:100] + '...' if record['fields'].get('摘要') else ''
        } for record in records]
        return render_template('index.html', articles=articles)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/article/<record_id>')
@cache.cached(timeout=300)
def article(record_id):
    try:
        records = feishu_api.get_table_records()
        article = next(({
            'title': record['fields'].get('标题', '无标题'),
            'quote': record['fields'].get('金句', ''),
            'summary': record['fields'].get('摘要', ''),
            'content': record['fields'].get('内容', '')
        } for record in records if record['record_id'] == record_id), None)
        
        if article:
            return render_template('detail.html', article=article)
        return '文章未找到', 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)