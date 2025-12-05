import asyncio
import websockets
import json

async def test_weather_command():
    """测试@天气命令"""
    uri = "ws://localhost:9876"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("连接到服务器成功")
            
            # 发送登录请求（使用已存在的用户名"111"）
            login_data = {
                "type": "login",
                "username": "111",
                "nickname": "测试用户",
                "server_address": uri
            }
            await websocket.send(json.dumps(login_data))
            print("发送登录请求")
            
            # 接收登录响应
            login_response = await websocket.recv()
            print(f"登录响应: {login_response}")
            
            # 发送@天气命令
            weather_command = {
                "type": "message",
                "username": "111",
                "nickname": "测试用户",
                "content": "@天气 北京"
            }
            await websocket.send(json.dumps(weather_command))
            print("发送@天气命令")
            
            # 接收天气信息响应
            weather_response = await websocket.recv()
            print(f"天气信息响应: {weather_response}")
            
            # 解析并显示天气信息
            response_data = json.loads(weather_response)
            if response_data["type"] == "system":
                print(f"\n天气信息:\n{response_data['content']}")
            
    except Exception as e:
        print(f"测试过程中发生错误: {e}")

if __name__ == "__main__":
    asyncio.run(test_weather_command())
