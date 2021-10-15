import pyaudio
import wave
import numpy as np
from scipy import fftpack
from utils.basic_method import *


def record_second(_filename, _record_second=5):
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

    frames = []    # 每一帧的数据列表
    fa_datas = []
    print("Start!")
    for i in range(0, int(RATE/CHUNK*RECORD_SECONDS)):
        data = stream.read(CHUNK)
        rt_data = np.frombuffer(data, np.dtype(np.int32))
        # 傅里叶变换
        fft_temp_data = fftpack.fft(rt_data, rt_data.size, overwrite_x=True)
        fft_data = np.abs(fft_temp_data)[0:fft_temp_data.size // 2 + 1]
        fa_data = np.sum(fft_data) // len(fft_data)
        frames.append(data)   # 将输入流每一帧的信息写入
        fa_datas.append(fa_data)
    print("Over!")   # 其实就是采样结束，还没有真正写入文件

    stream.stop_stream()   # 停止输入流
    stream.close()   # 关闭输入流
    p.terminate()   # 终止使用PyAudio

    wf = wave.open(WAVE_OUT_FILE, 'wb')   # 打开要写入的wave文件，也就是要录指出的wave文件
    wf.setnchannels(CHANNELS)   # 设置录制，即写入的声道数
    wf.setsampwidth(p.get_sample_size(FORMAT))   # 写入录制基本格式的宽度，传入的数据由前面设置的FORMAT格式决定
    wf.setframerate(RATE)   # 设置写入的采样率
    wf.writeframes(b''.join(frames))   # 写入frames中储存的数据，到这里终于把采集到的数据写入成了wave文件
    wf.close()    # 关闭文件
    return np.average(np.array(fa_datas))
    

def record_auto(filename, start_thres=80000000, end_thres=40000000):
    CHUNK = 1024  # wave文件以chunk为基本单位存储
    FORMAT = pyaudio.paInt16  # wave文件录制的基本格式
    CHANNELS = 2  # 声道数
    RATE = 16000  # 采样率
    WAVE_OUT_FILE = filename  # 录制的文件名

    p = pyaudio.PyAudio()

    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK)

    print("Start!")
    frames = []
    fa_datas = []
    start_record = False
    break_record = False
    while not break_record:
        data = stream.read(CHUNK)
        rt_data = np.frombuffer(data, np.dtype(np.int32))
        # 傅里叶变换
        fft_temp_data = fftpack.fft(rt_data, rt_data.size, overwrite_x=True)
        fft_data = np.abs(fft_temp_data)[0:fft_temp_data.size // 2 + 1]
        fa_data = np.sum(fft_data) // len(fft_data)
        # print(fa_data)
        if fa_data > start_thres:
            # print("start")
            start_record = True
        if start_record:
            frames.append(data)
            fa_datas.append(fa_data)
            if len(fa_datas) < 8:
                continue
            else:
                break_record = True
                for x in fa_datas[-5:]:
                    if x >= end_thres:
                        break_record = False
                        break
                
    print("Over!")
    # print(len(frames))

    stream.stop_stream()  # 停止输入流
    stream.close()  # 关闭输入流
    p.terminate()  # 终止使用PyAudio

    wf = wave.open(WAVE_OUT_FILE, 'wb')  # 打开要写入的wave文件，也就是要录指出的wave文件
    wf.setnchannels(CHANNELS)  # 设置录制，即写入的声道数
    # 写入录制基本格式的宽度，传入的数据由前面设置的FORMAT格式决定
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)  # 设置写入的采样率
    wf.writeframes(b''.join(frames))  # 写入frames中储存的数据，到这里终于把采集到的数据写入成了wave文件


def pretreatment(path_origin,
                 path_after_filtering,
                 factor_filter1=100,
                 factor_filter2=0,
                 ):
    """
    简单预处理，经过滤波后端点检测
    （因为不知道一段长语音中有几小段，这里不统一时间，训练时可以把此预处理和时间统一写在一起）

    :param path_origin: 原始语音路径
    :param path_after_filtering: 滤波后语音路径
    :param factor_filter1:  滤波参数1，阈值，默认100
    :param factor_filter2:  滤波参数2，指阈值之下的频率所乘的系数，默认0
    :return: None
    """
    high_pass_filter(path_origin, path_after_filtering, factor_filter1, factor_filter2)
    audio_split_single(path_after_filtering)
    os.remove(path_after_filtering)
