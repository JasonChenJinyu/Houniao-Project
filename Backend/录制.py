import pyaudio
import wave


# 录音参数设置
CHUNK = 1024  # 每次采集的音频块大小
FORMAT = pyaudio.paInt16  # 音频格式
CHANNELS = 1  # 单声道
RATE = 16000  # 采样率，每秒样本数
RECORD_SECONDS = 5  # 录音时长
WAVE_OUTPUT_FILENAME = "output.wav"  # 输出文件名

# 初始化PyAudio
p = pyaudio.PyAudio()

# 打开流
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("开始录音...")

frames = []  # 用于存储录音数据

# 开始录音
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("录音结束.")

# 停止并关闭流
stream.stop_stream()
stream.close()
p.terminate()

# 写入WAV文件
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

print(f"音频已保存为: {WAVE_OUTPUT_FILENAME}")

