# 飞书应用凭证
from dotenv import load_dotenv
import os

# 加载.env文件中的配置
load_dotenv()

# 从环境变量中获取配置
APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")
BASE_ID = os.getenv("BASE_ID")
TABLE_ID = os.getenv("TABLE_ID")

# 飞书API接口
FEISHU_HOST = "https://open.feishu.cn"
TENANT_ACCESS_TOKEN_URI = "/open-apis/auth/v3/tenant_access_token/internal"
BITABLE_URI = "/open-apis/bitable/v1/apps/{}/tables/{}/records"