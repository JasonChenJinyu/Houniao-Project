import os
import requests
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import tempfile


def record_and_transcribe(
        duration=5,
        sample_rate=16000,
        token="your_api_token_here"
):
    """
    录音并转文字的完整流程

    参数：
    - duration: 录音时长(秒)
    - sample_rate: 采样率(Hz)
    - token: API认证令牌

    返回：
    - text: 识别出的文字
    - logid: 请求日志ID
    """
    try:
        # 第一步：录音
        print(f"▶️ 开始录音，剩余 {duration}秒...")
        recording = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype=np.int16
        )
        sd.wait()  # 等待录音完成
        print("✅ 录音完成")

        # 第二步：保存临时文件
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_wav:
            write(tmp_wav.name, sample_rate, recording)
            tmp_path = tmp_wav.name

        # 第三步：调用API转文字
        url = "https://api.coze.cn/v1/audio/transcriptions"
        headers = {
            "Authorization": f"Bearer {token}"
        }

        with open(tmp_path, "rb") as audio_file:
            files = {"file": (tmp_path.split('/')[-1], audio_file, "audio/mpeg")}
            response = requests.post(url, headers=headers, files=files)

        # 第四步：处理响应
        if response.status_code == 200:
            result = response.json()
            return {
                "text": result.get("data", {}).get("text", ""),
                "logid": result.get("detail", {}).get("logid", "")
            }
        else:
            print(f"❌ 请求失败，状态码：{response.status_code}")
            print("响应内容：", response.text)
            return None

    except Exception as e:
        print(f"❌ 发生异常：{str(e)}")
        return None
    finally:
        # 清理临时文件
        if 'tmp_path' in locals():
            try:
                os.remove(tmp_path)
            except:
                pass


# 使用示例
if __name__ == "__main__":
    # 替换为你的API令牌
    API_TOKEN = "***"

    result = record_and_transcribe(
        duration=5,  # 录音5秒
        token=API_TOKEN
    )

    if result:
        print("\n识别结果：")
        print(f"日志ID：{result['logid']}")
        print(f"识别文本：{result['text']}")
    else:
        print("识别失败")