import asyncio
import websockets
import json
import random

async def test_news_command():
    # 连接到服务器
    async with websockets.connect('ws://localhost:9876') as websocket:
        print("已连接到服务器")
        
        # 生成随机用户名
        random_id = random.randint(1000, 9999)
        username = f"testuser_{random_id}"
        password = "123456"
        nickname = f"测试用户{random_id}"
        
        # 注册用户
        register_data = {
            'type': 'register',
            'username': username,
            'password': password,
            'nickname': nickname
        }
        await websocket.send(json.dumps(register_data))
        register_response = await websocket.recv()
        print(f"注册响应: {register_response}")
        
        # 登录用户
        login_data = {
            'type': 'login',
            'username': username,
            'password': password
        }
        await websocket.send(json.dumps(login_data))
        login_response = await websocket.recv()
        print(f"登录响应: {login_response}")
        
        # 测试@新闻命令
        print("\n测试@新闻命令:")
        news_command = {
            'type': 'message',
            'content': '@新闻',
            'timestamp': 'test',
            'sender': username
        }
        await websocket.send(json.dumps(news_command))
        
        # 接收响应
        while True:
            response = await websocket.recv()
            response_data = json.loads(response)
            
            # 只处理来自服务器的消息
            if response_data.get('type') == 'command' and response_data.get('sender') == '新闻助手':
                print(f"新闻助手响应: {response_data['content']}")
                break
        
        # 退出登录
        logout_data = {
            'type': 'logout'
        }
        await websocket.send(json.dumps(logout_data))
        logout_response = await websocket.recv()
        print(f"退出响应: {logout_response}")

if __name__ == "__main__":
    asyncio.run(test_news_command())