import requests
import os
import tempfile
import threading
from fastapi import FastAPI, HTTPException

app = FastAPI()


def async_play_audio(answer: str):
    """异步播放音频的线程函数"""
    def _play_audio():
        try:
            url = "https://api.coze.cn/v1/audio/speech"
            data = {
                "input": answer,
                "voice_id": "7426720361732980745",
                "response_format": "wav"
            }
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer ***"
            }

            response = requests.post(url, json=data, headers=headers)

            if response.status_code == 200:
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                    f.write(response.content)
                    temp_file = f.name

                try:
                    if os.name == 'nt':
                        import winsound
                        winsound.PlaySound(temp_file, winsound.SND_FILENAME)
                    else:
                        import subprocess
                        subprocess.run(
                            ["afplay" if os.uname().sysname == "Darwin" else "aplay", temp_file]
                        )
                finally:
                    os.remove(temp_file)
            else:
                print(f"音频请求失败：{response.status_code}")
                print("响应内容：", response.text)
        except Exception as e:
            print(f"音频播放异常：{str(e)}")

    # 启动线程
    thread = threading.Thread(target=_play_audio)
    thread.start()