import requests
import time
from checkerbot_gui.utils import extract_text_from_word

# API 配置
BOT_ID = "7442709222326501386"
# API_TOKEN = "pat_yAx5UFur58gr8ILl6aNbWNJeXlA4gxqbTDm1S3FvtOzybUOPXatiYI4NiqPn9ot9"
API_TOKEN = None
BASE_URL = "https://api.coze.cn/v3"
PROXY = None  # 默认为无代理

def change_api_token(api_token):
    global API_TOKEN
    if api_token:
        API_TOKEN = api_token
    else:
        API_TOKEN = None

def change_proxy(proxy):
    global PROXY
    if proxy:
        PROXY = {
            "http": proxy,
            "https": proxy
        }
    else:
        PROXY = None

# 发送聊天请求
def send_chat_request(question):
    try:
        url = f"{BASE_URL}/chat"
        print(API_TOKEN)

        headers = {
            "Authorization": f"Bearer {API_TOKEN}",
            "Content-Type": "application/json"
        }
        data = {
            "bot_id": BOT_ID,
            "user_id": "8494821141",  # 可以使用任意用户ID
            "stream": False,
            "auto_save_history": True,
            "additional_messages": [
                {
                    "role": "user",
                    "content": question,
                    "content_type": "text"
                }
            ]
        }

        
        print(PROXY)

        response = requests.post(url, headers=headers, json=data, proxies=PROXY)
        response.raise_for_status()  # 如果请求失败，抛出HTTPError
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"发送聊天请求失败: {str(e)}") from e

# 获取聊天消息
def get_chat_messages(chat_id, conversation_id):
    try:
        url = f"{BASE_URL}/chat/message/list?chat_id={chat_id}&conversation_id={conversation_id}"
        
        
        headers = {
            "Authorization": f"Bearer {API_TOKEN}",
            "Content-Type": "application/json"
        }


        response = requests.get(url, headers=headers, proxies=PROXY)
        response.raise_for_status()  # 如果请求失败，抛出HTTPError
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"获取聊天消息失败: {str(e)}") from e
