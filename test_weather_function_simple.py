import asyncio
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'DaiP_ChatRoom', 'server')))

# 导入get_weather_info函数
from server import get_weather_info

async def test_weather_function():
    """直接测试get_weather_info函数"""
    print("开始测试get_weather_info函数")
    
    # 测试获取北京的天气信息
    print("\n测试获取北京的天气信息：")
    beijing_weather = await get_weather_info("北京")
    print(beijing_weather)
    
    # 测试获取上海的天气信息
    print("\n测试获取上海的天气信息：")
    shanghai_weather = await get_weather_info("上海")
    print(shanghai_weather)
    
    # 测试获取广州的天气信息
    print("\n测试获取广州的天气信息：")
    guangzhou_weather = await get_weather_info("广州")
    print(guangzhou_weather)
    
    # 测试获取成都的天气信息
    print("\n测试获取成都的天气信息：")
    chengdu_weather = await get_weather_info("成都")
    print(chengdu_weather)
    
    # 测试获取雅安的天气信息（非预定义城市）
    print("\n测试获取雅安的天气信息（非预定义城市）：")
    yaan_weather = await get_weather_info("雅安")
    print(yaan_weather)

if __name__ == "__main__":
    asyncio.run(test_weather_function())
