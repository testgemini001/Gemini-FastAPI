from app.main import create_app
from app.utils import setup_logging, g_config

# 初始化日志
setup_logging(level=g_config.logging.level)

# 创建应用实例
app = create_app()

# Vercel 需要的导出
def handler(event, context):
    return app 