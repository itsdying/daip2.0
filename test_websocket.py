import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://localhost:9876"
    try:
        print(f"尝试连接到 {uri}")
        async with websockets.connect(uri) as websocket:
            print("WebSocket连接成功！")
            
            # 发送登录消息，使用与客户端相同的格式
            login_message = {"type": "login", "nickname": "test_user", "server_address": uri}
            await websocket.send(json.dumps(login_message))
            print("已发送登录消息")
            
            # 等待响应
            response = await websocket.recv()
            print(f"收到响应: {response}")
            
            # 解析响应
            data = json.loads(response)
            if data.get("type") == "login_response" and data.get("success"):
                print("登录成功！")
            else:
                print(f"登录失败: {data.get('message', '未知错误')}")
                
    except ConnectionRefusedError:
        print("连接被拒绝，请检查服务器是否正在运行")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    asyncio.run(test_websocket())