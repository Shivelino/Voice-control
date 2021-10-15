import pyaudio
import wave
import matplotlib.pyplot as plt  # 用于可视化
import librosa  # 填充，默认频率为22050，可以改变频率
import librosa.display
from pydub import AudioSegment   # 用于音频的相加
import os


'''-----------------------------------------------------------------------------------------------'''


def record(_filename, _record_second=5):
    r"""
    用于录制音频的函数，在指定路径生成一个录制wav文件

    :param _filename: 文件路径
    :param _record_second: 录制时间，默认5s
    :return: None

    Examples
    --------
    record('./record.wav', _record_second=3)
    """
    CHUNK = 1024  # wave文件以chunk为基本单位存储
    FORMAT = pyaudio.paInt16   # wave文件录制的基本格式
    CHANNELS = 2   # 声道数
    RATE = 16000   # 采样率
    RECORD_SECONDS = _record_second   # 录音时间
    WAVE_OUT_FILE = _filename   # 录制的文件名

    p = pyaudio.PyAudio()   # 初始化

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)    # 初始化输入流

    print("开始录音")

    frames = []    # 每一帧的数据列表

    for i in range(0, int(RATE/CHUNK*RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)   # 将输入流每一帧的信息写入

    print("结束录音")   # 其实就是采样结束，还没有真正写入文件

    stream.stop_stream()   # 停止输入流
    stream.close()   # 关闭输入流
    p.terminate()   # 终止使用PyAudio

    wf = wave.open(WAVE_OUT_FILE, 'wb')   # 打开要写入的wave文件，也就是要录指出的wave文件
    wf.setnchannels(CHANNELS)   # 设置录制，即写入的声道数
    wf.setsampwidth(p.get_sample_size(FORMAT))   # 写入录制基本格式的宽度，传入的数据由前面设置的FORMAT格式决定
    wf.setframerate(RATE)   # 设置写入的采样率
    wf.writeframes(b''.join(frames))   # 写入frames中储存的数据，到这里终于把采集到的数据写入成了wave文件
    wf.close()    # 关闭文件


def player(_filename):
    r"""
    用于播放wav音频的函数

    :param _filename: 文件路径
    :return: None

    Examples
    --------
     player('./record.wav')
    """
    CHUNK = 1024
    wf = wave.open(_filename, 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)

    while data != b'':
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()

    p.terminate()   # 跟上面的类似，注释就不写了


def display(_filename):
    r"""
    下面的函数用于可视化

    :param _filename: 文件路径
    :return: None

    Examples
    --------
    display('./record.wav')
    """
    data1, sample_rate = librosa.load(_filename)   # 加载文件
    plt.figure(figsize=(14, 5))   # 可视化的图片尺寸
    librosa.display.waveplot(data1, sample_rate)   # 自动可视化
    plt.show()   # 展示可视化


def mixing(standard_time_wave_path, wavepath, output_path):
    r"""
    用于将两个音频合并在一起的函数

    :param standard_time_wave_path: 基础语音路径
    :param wavepath: 添加语音路径
    :param output_path: 输出路径
    :return: None

    Examples
    --------
    mixing('./record1.wav', './record2.wav', './record3.wav')
    """
    sound1 = AudioSegment.from_wav(standard_time_wave_path)
    sound2 = AudioSegment.from_wav(wavepath)
    output = sound1.overlay(sound2)  # 混音，实现音频的时间统一
    output.export(output_path, format="wav")
    
    
def remove(file_path):
    """删除文件"""
    os.remove(file_path)


if __name__ == "__main__":
    pass
