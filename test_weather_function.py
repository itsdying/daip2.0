import asyncio
import sys
import logging

# 添加项目根目录到路径
sys.path.append('C:\\Users\\Lenovo\\Desktop\\python项目\\DaiP_ChatRoom')

# 设置日志级别为DEBUG
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 导入get_weather_info函数
from server.server import get_weather_info

async def test_weather_function():
    """测试get_weather_info函数"""
    try:
        logger.info("开始测试get_weather_info函数")
        
        # 直接调用天气获取函数
        weather_info = await get_weather_info("雅安")
        
        logger.info(f"天气信息获取结果: {weather_info}")
    except Exception as e:
        logger.error(f"测试过程中发生错误: {e}", exc_info=True)

if __name__ == "__main__":
    # 运行测试
    asyncio.run(test_weather_function())
