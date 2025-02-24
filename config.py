import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # 飞书应用配置
    FEISHU_APP_ID = os.getenv('FEISHU_APP_ID', 'cli_a732c149713b101c')
    FEISHU_APP_SECRET = os.getenv('FEISHU_APP_SECRET', 'Wrgg6XTbwjrVygLqVbuqb5GVtEopsPKM')
    
    # 多维表格配置
    BASE_ID = os.getenv('BASE_ID', 'OF5PblFxva7Ip8sNTrJcnEjonQg')
    TABLE_ID = os.getenv('TABLE_ID', 'tblOTL3T7JOCUpxV')
    
    # Flask应用配置
    SECRET_KEY = os.urandom(24)
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300