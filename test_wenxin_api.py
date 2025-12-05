import requests
import json

# 测试文心一言API的access_token获取
def test_wenxin_access_token():
    api_key = "cs-sk-8019b0e1-3a7b-4eb4-805a-c36e881492c6"
    secret_key = "your_wenxin_secret_key"  # 这里需要填写正确的secret_key
    
    print(f"使用API Key: {api_key}")
    print(f"使用Secret Key: {secret_key}")
    
    # 调用百度API获取access_token
    url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={api_key}&client_secret={secret_key}"
    print(f"请求URL: {url}")
    
    try:
        response = requests.get(url)
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        response_data = response.json()
        if 'access_token' in response_data:
            print(f"成功获取access_token: {response_data['access_token'][:10]}...")
            return response_data['access_token']
        else:
            print(f"获取失败: {response_data}")
            return None
    except Exception as e:
        print(f"请求出错: {e}")
        return None

# 测试调用文心一言API
def test_wenxin_api_call(access_token):
    if not access_token:
        print("没有有效的access_token，无法调用API")
        return
    
    base_url = "https://open.bigmodel.cn/api/paas/v4/"
    model = "ernie-bot"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": "你好吗？"}
        ]
    }
    
    url = f"{base_url}chat/completions"
    print(f"调用API URL: {url}")
    print(f"请求头: {headers}")
    print(f"请求数据: {json.dumps(data)}")
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        response_data = response.json()
        if 'choices' in response_data and len(response_data['choices']) > 0:
            print(f"成功获取回答: {response_data['choices'][0]['message']['content']}")
        else:
            print(f"API调用失败: {response_data}")
    except Exception as e:
        print(f"调用API出错: {e}")

if __name__ == "__main__":
    print("开始测试文心一言API...")
    access_token = test_wenxin_access_token()
    if access_token:
        print("\n开始测试API调用...")
        test_wenxin_api_call(access_token)