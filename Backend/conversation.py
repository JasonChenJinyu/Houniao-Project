import requests
import json
import sqlite3
from datetime import datetime


# 初始化数据库（添加 emotion 字段）
def init_db():
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id TEXT,
            answer TEXT,
            condition TEXT,
            emotion TEXT,
            emoji TEXT,
            timestamp DATETIME
        )
    ''')
    conn.commit()
    conn.close()

# 插入数据（新增 emoji 参数）
def insert_chat_history(chat_id, answer, condition, emotion, emoji):  # 修改函数签名
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO chat_history 
        (chat_id, answer, condition, emotion, emoji, timestamp)
        VALUES (?, ?, ?, ?, ?, ?) 
    ''', (chat_id, answer, condition, emotion, emoji, datetime.now()))
    conn.commit()
    conn.close()


def stream_chat(question):
    conversation_id = "7476727330547777576"
    url = f"https://api.coze.cn/v3/chat?conversation_id={conversation_id}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer ***"
    }

    payload = {
        "bot_id": "7476679488836173836",
        "user_id": "123456789",
        "stream": True,
        "auto_save_history": True,
        "additional_messages": [
            {
                "role": "user",
                "content": question,
                "content_type": "text"
            }
        ]
    }

    try:
        requests.packages.urllib3.disable_warnings()

        with requests.post(url, headers=headers, json=payload, stream=True, verify=False) as response:
            response.raise_for_status()
            target_id = None

            for chunk in response.iter_lines():
                if chunk:
                    decoded_chunk = chunk.decode('utf-8').strip()
                    print("[DEBUG] 原始响应:", decoded_chunk)

                    if decoded_chunk.startswith("event:"):
                        event_type = decoded_chunk.split(":")[1].strip()
                        print(f"检测到事件类型: {event_type}")
                        continue


                    elif decoded_chunk.startswith("data:"):

                        json_str = decoded_chunk[5:].strip()

                        try:

                            data = json.loads(json_str)

                            if not isinstance(data, dict):
                                continue

                            # 捕获聊天完成事件

                            if event_type == "conversation.chat.completed" and "id" in data:
                                target_id = data["id"]

                                print("成功获取 Chat ID:", target_id)

                            # 处理回答数据

                            if data.get("type") == "answer":

                                content = data.get("content", "")

                                try:

                                    answer_data = json.loads(content)

                                    answer = answer_data.get("answer")

                                    condition = answer_data.get("condition")

                                    emotion = answer_data.get("emotion")

                                    emoji = answer_data.get("emoji")  # 新增字段提取

                                    # 存入数据库（新增 emoji）

                                    insert_chat_history(

                                        target_id,

                                        answer,

                                        condition,

                                        emotion,

                                        emoji

                                    )

                                    # 返回结果（新增 emoji）

                                    return {

                                        "answer": answer,

                                        "condition": condition,

                                        "emotion": emotion,

                                        "emoji": emoji[:2]

                                    }


                                except Exception as e:

                                    print(f"内容解析失败: {e}")


                        except json.JSONDecodeError:

                            continue

            return target_id

    except requests.exceptions.RequestException as e:
        print("请求失败:", e)
        return None

if __name__ == '__main__':
    # 初始化数据库并测试
    init_db()
    result = stream_chat("我好喜欢我隔壁班的男孩")
    print("API 返回结果:", result)
