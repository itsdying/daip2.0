import asyncio
import websockets

async def test_simple_connect():
    uri = "ws://localhost:9876"
    try:
        print(f"尝试连接到 {uri}")
        async with websockets.connect(uri) as websocket:
            print("WebSocket连接成功！")
            print("保持连接5秒钟...")
            await asyncio.sleep(5)
            print("连接正常保持了5秒钟")
    except Exception as e:
        print(f"发生错误: {e}")

# 运行测试
if __name__ == "__main__":
    asyncio.run(test_simple_connect())