import asyncio
import websockets
import json
import time

async def test_weather_command():
    """测试@天气命令的全面功能"""
    # 连接到WebSocket服务器
    uri = "ws://localhost:9876"
    print(f"正在连接到服务器: {uri}")
    
    try:
        async with websockets.connect(uri) as websocket:
            print("连接到服务器成功")
            
            # 登录到服务器（使用已存在的用户名'111'）
            login_data = {
                "type": "login",
                "username": "111",
                "nickname": "111",
                "server_address": "ws://localhost:9876"
            }
            await websocket.send(json.dumps(login_data))
            print("发送登录请求")
            
            # 接收登录响应
            login_response = await websocket.recv()
            print(f"登录响应: {login_response}")
            login_data = json.loads(login_response)
            
            if login_data["success"]:
                print("登录成功")
                
                # 测试城市列表
                test_cities = ["北京", "上海", "广州", "深圳", "杭州", "成都", "重庆", "西安", "武汉", "南京", "雅安"]
                
                for city in test_cities:
                    # 发送@天气命令
                    weather_command = {
                        "type": "message",
                        "content": f"@天气 {city}",
                        "username": "111",
                        "timestamp": time.strftime("%H:%M:%S"),
                        "color": "#000000",
                        "is_system": False
                    }
                    await websocket.send(json.dumps(weather_command))
                    print(f"发送@天气 {city} 命令")
                    
                    # 接收并处理服务器响应
                    response = await websocket.recv()
                    print(f"服务器响应: {response}")
                    response_data = json.loads(response)
                    
                    # 检查响应是否包含天气信息
                    if response_data["type"] == "command" and response_data["command_type"] == "weather":
                        print(f"成功获取{city}的天气信息")
                    else:
                        print(f"获取{city}的天气信息失败")
                    
                    # 等待一段时间，避免请求过于频繁
                    await asyncio.sleep(1)
            else:
                print("登录失败")
                
    except Exception as e:
        print(f"测试过程中出现错误: {e}")

if __name__ == "__main__":
    asyncio.run(test_weather_command())
