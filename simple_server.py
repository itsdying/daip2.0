import asyncio
import websockets
import json
import logging

# 配置详细日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

connected_clients = set()
user_info_map = {}
logged_in_users = set()

async def handle_client(websocket, path):
    connected_clients.add(websocket)
    logger.info(f"新客户端连接，当前连接数: {len(connected_clients)}")
    
    try:
        async for message in websocket:
            logger.info(f"收到消息: {message}")
            
            try:
                # 尝试解析消息
                data = json.loads(message)
                logger.info(f"解析后的数据: {data}")
                
                # 处理登录消息
                if data.get('type') == 'login':
                    nickname = data.get('nickname', '未知用户')
                    logger.info(f"登录请求，昵称: {nickname}")
                    
                    # 简单响应
                    response = {
                        'type': 'login_response',
                        'success': True,
                        'message': '登录成功',
                        'user_info': {'nickname': nickname}
                    }
                    
                    response_str = json.dumps(response)
                    logger.info(f"准备发送响应: {response_str}")
                    await websocket.send(response_str)
                    logger.info("响应已发送")
                else:
                    logger.warning(f"未知消息类型: {data.get('type')}")
            except json.JSONDecodeError as e:
                logger.error(f"JSON解析错误: {e}")
                await websocket.send(json.dumps({'type': 'error', 'content': 'JSON格式错误'}))
            except Exception as e:
                logger.error(f"处理消息错误: {e}", exc_info=True)
                await websocket.send(json.dumps({'type': 'error', 'content': '处理错误'}))
    
    except websockets.exceptions.ConnectionClosed as e:
        logger.info(f"连接关闭: {e}")
    except Exception as e:
        logger.error(f"客户端处理异常: {e}", exc_info=True)
    finally:
        connected_clients.remove(websocket)
        logger.info(f"客户端断开，当前连接数: {len(connected_clients)}")

async def main():
    logger.info("启动简单WebSocket服务器...")
    server = await websockets.serve(handle_client, "0.0.0.0", 9876)
    logger.info("服务器已启动，监听端口9876")
    await server.serve_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("服务器已停止")
    except Exception as e:
        logger.error(f"服务器异常: {e}", exc_info=True)