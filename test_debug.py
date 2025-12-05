import asyncio
import websockets
import json
import logging

# 配置日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_websocket_debug():
    uri = "ws://localhost:9876"
    try:
        logger.info(f"尝试连接到 {uri}")
        async with websockets.connect(uri) as websocket:
            logger.info("WebSocket连接成功！")
            
            # 创建登录消息
            login_message = {
                "type": "login",
                "nickname": "test_user",
                "server_address": uri
            }
            
            # 发送登录消息
            message_str = json.dumps(login_message)
            logger.info(f"准备发送登录消息: {message_str}")
            await websocket.send(message_str)
            logger.info("登录消息已发送")
            
            # 尝试接收响应
            logger.info("等待服务器响应...")
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=5)
                logger.info(f"收到服务器响应: {response}")
            except asyncio.TimeoutError:
                logger.warning("没有收到服务器响应，5秒超时")
            
            # 保持连接一小段时间
            logger.info("等待1秒...")
            await asyncio.sleep(1)
            
    except websockets.exceptions.ConnectionClosedError as e:
        logger.error(f"连接关闭错误: {e}, code={e.code}, reason={e.reason}")
    except websockets.exceptions.ConnectionClosedOK as e:
        logger.warning(f"连接正常关闭: {e}, code={e.code}, reason={e.reason}")
    except Exception as e:
        logger.error(f"发生错误: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

# 运行测试
if __name__ == "__main__":
    asyncio.run(test_websocket_debug())