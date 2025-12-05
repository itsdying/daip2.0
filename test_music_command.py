#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试@音乐命令功能
"""

import asyncio
import websockets
import json
import time
import random

async def test_music_command():
    """测试@音乐命令"""
    try:
        # 连接到WebSocket服务器
        uri = "ws://localhost:9876"
        async with websockets.connect(uri) as websocket:
            print("已连接到服务器")
            
            # 生成随机用户名和密码用于测试
            test_username = f"testuser_{random.randint(1000, 9999)}"
            test_password = "test123"
            test_nickname = f"测试用户{random.randint(1000, 9999)}"
            
            # 注册新用户
            register_data = {
                "type": "register",
                "username": test_username,
                "password": test_password,
                "nickname": test_nickname,
                "server_address": "localhost"
            }
            await websocket.send(json.dumps(register_data))
            register_response = await websocket.recv()
            print(f"注册响应: {register_response}")
            
            # 注册成功后用户已经自动登录，无需再次登录
            print("用户已自动登录，开始测试@音乐命令")
            
            # 等待一下
            time.sleep(1)
            
            # 测试1: 发送@音乐命令，不带音乐名称
            music_command1 = {
                "type": "message",
                "content": "@音乐"
            }
            await websocket.send(json.dumps(music_command1))
            print("\n已发送命令: @音乐")
            
            # 接收响应
            response1 = await websocket.recv()
            response1_data = json.loads(response1)
            print(f"服务器响应: {response1_data['content']}")
            
            # 等待一下
            time.sleep(1)
            
            # 测试2: 发送@音乐命令，带预定义的音乐名称
            music_command2 = {
                "type": "message",
                "content": "@音乐 晴天"
            }
            await websocket.send(json.dumps(music_command2))
            print("\n已发送命令: @音乐 晴天")
            
            # 接收响应
            response2 = await websocket.recv()
            response2_data = json.loads(response2)
            print(f"服务器响应: {response2_data['content']}")
            
            # 等待一下
            time.sleep(1)
            
            # 测试3: 发送@音乐命令，带非预定义的音乐名称
            music_command3 = {
                "type": "message",
                "content": "@音乐 未知歌曲"
            }
            await websocket.send(json.dumps(music_command3))
            print("\n已发送命令: @音乐 未知歌曲")
            
            # 接收响应
            response3 = await websocket.recv()
            response3_data = json.loads(response3)
            print(f"服务器响应: {response3_data['content']}")
            
            # 退出登录
            logout_data = {
                "type": "logout"
            }
            await websocket.send(json.dumps(logout_data))
            logout_response = await websocket.recv()
            print(f"\n退出登录响应: {logout_response}")
            
    except Exception as e:
        print(f"测试过程中出错: {e}")

if __name__ == "__main__":
    print("开始测试@音乐命令...")
    asyncio.run(test_music_command())
    print("\n测试完成!")
