from fastapi import FastAPI, HTTPException
from datetime import datetime
import sqlite3
from pydantic import BaseModel
from typing import List, Dict
from conversation import stream_chat
from fastapi.middleware.cors import CORSMiddleware
from 文字转语音 import async_play_audio
import asyncio
from 录音生成文字 import record_and_transcribe


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许的源列表
    allow_credentials=True,
    allow_methods=["*"],  # 允许的 HTTP 方法
    allow_headers=["*"],  # 允许的请求头
)
# 数据库配置
DB_NAME = "chat_history.db"


class ConditionResponse(BaseModel):
    date: str
    records: List[Dict[str, str]]  # 修改为包含 condition 和 emotion 的字典列表


def query_conditions_by_date(target_date: str) -> List[Dict[str, str]]:
    """根据日期查询所有 condition 和 emotion 记录"""
    try:
        datetime.strptime(target_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # 修改查询语句获取两个字段
        cursor.execute('''
            SELECT condition, emotion 
            FROM chat_history
            WHERE DATE(timestamp) = ?
            ORDER BY timestamp
        ''', (target_date,))

        results = cursor.fetchall()
        print(f"查询结果: {results}")

        # 转换为字典列表
        return [
            {
                "condition": row[0] if row[0] else "",
                "emotion": row[1] if row[1] else "neutral"  # 默认值处理
            }
            for row in results
            if row[0] or row[1]  # 过滤空记录
        ]

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if conn:
            conn.close()


@app.post("/talk")
async def talk():
    """
    对话接口 - 接收用户问题并返回智能体回复
    返回：
    - answer: 回答内容
    - emoji: 对应表情符号
    """
    try:
        API_TOKEN = "pat_nQfjpT0I7Hvn9nWjJk4cCQ7C72ST50ZXKP9PNDrN8PPR9sh8MW7s9dRpU002itCo"
        # 模拟调用对话核心方法
        result = stream_chat(record_and_transcribe(
            duration=3,  # 录音5秒
            token=API_TOKEN
        )['text'])

        if not result:
            raise HTTPException(status_code=500, detail="对话服务暂时不可用")
        print(result)
        # 启动音频播放线程
        async_play_audio(result.get("answer"))

        # 异步等待3秒（不阻塞事件循环）
        await asyncio.sleep(3)

        # 延迟返回结果
        return {
            "answer": result.get("answer"),
            "emoji": result.get("emoji")
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"对话处理失败: {str(e)}"
        )

@app.get("/conditions/{date}", response_model=ConditionResponse)
async def get_conditions_by_date(date: str):
    """
    获取指定日期的所有记录（包含 condition 和 emotion）

    - **date**: 查询日期 (格式: YYYY-MM-DD)
    """
    records = query_conditions_by_date(date)
    return {
        "date": date,
        "records": records
    }


# 示例测试请求
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)