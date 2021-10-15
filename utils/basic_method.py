import os
import subprocess
import shutil
import soundfile as sf
from utils.feature import VAD
from utils import thinkdsp


def high_pass_filter(file_path, output_path, cutoff=100, factor=0):
    """
    高通滤波器，滤掉阈值之下的波

    :param file_path: 输入文件
    :param output_path: 输出文件
    :param cutoff: 阈值，默认100
    :param factor: 滤波参数，指阈值之下的频率所乘的系数，默认0
    :return: None

    Examples
    --------
    high_pass_filter('./record/origin/record1.wav', './record/after_filtering/record1.wav', cutoff=500, factor=0)
    """
    wave = thinkdsp.read_wave(file_path)
    # wave.plot()
    # plt.show()  # 显示波形图

    spectrum = wave.make_spectrum()
    # spectrum.plot()
    # thinkplot.show()  # 显示频谱图

    spectrum.high_pass(cutoff, factor)  # 高通滤波
    # spectrum.plot()
    # thinkplot.show()
    wave = spectrum.make_wave()
    wave.write(output_path)


def high_pass_filter__for_folder(input_folder_path, output_folder_path, cutoff=1000, factor=0):
    """
    对整个文件夹进行高通滤波

    :param input_folder_path: 输入文件夹
    :param output_folder_path: 输出文件夹
    :param cutoff: 阈值，默认100
    :param factor: 滤波参数，指阈值之下的频率所乘的系数，默认0
    :return: None

    Examples
    --------
    high_pass_filter('./record/origin/', './record/after_filtering/', cutoff=500, factor=0)
    """
    for file_name in [x for x in os.listdir(input_folder_path) if x.endswith('.wav')]:
        file_path = os.path.join(input_folder_path, file_name)
        wave = thinkdsp.read_wave(file_path)
        # wave.plot()
        # plt.show()  # 显示波形图

        spectrum = wave.make_spectrum()
        # spectrum.plot()
        # thinkplot.show()  # 显示频谱图

        spectrum.high_pass(cutoff, factor)  # 高通滤波
        # spectrum.plot()
        # thinkplot.show()
        wave = spectrum.make_wave()
        wave.write(output_folder_path + file_name)


def low_pass_filter(file_path, output_path, cutoff=100, factor=0):
    """
    低通滤波器，滤掉阈值之上的波

    :param file_path: 输入文件
    :param output_path: 输出文件
    :param cutoff: 阈值，默认100
    :param factor: 滤波参数，指阈值之上的频率所乘的系数，默认0
    :return: None

    Examples
    --------
    low_pass_filter('./record/origin/record1.wav', './record/after_filtering/record1.wav', cutoff=500, factor=0)
    """
    wave = thinkdsp.read_wave(file_path)
    # wave.plot()
    # plt.show()  # 显示波形图

    spectrum = wave.make_spectrum()
    # spectrum.plot()
    # thinkplot.show()  # 显示频谱图

    spectrum.low_pass(cutoff, factor)  # 低通滤波
    # spectrum.plot()
    # thinkplot.show()
    wave = spectrum.make_wave()
    wave.write(output_path)


def low_pass_filter__for_folder(input_folder_path, output_folder_path, cutoff=1000, factor=0):
    """
    对整个文件夹进行低通滤波

    :param input_folder_path: 输入文件夹
    :param output_folder_path: 输出文件夹
    :param cutoff: 阈值，默认100
    :param factor: 滤波参数，指阈值之上的频率所乘的系数，默认0
    :return: None

    Examples
    --------
    low_pass_filter__for_folder('./record/origin/', './record/after_filtering/', cutoff=500, factor=0)
    """
    for file_name in [x for x in os.listdir(input_folder_path) if x.endswith('.wav')]:
        file_path = os.path.join(input_folder_path, file_name)
        wave = thinkdsp.read_wave(file_path)
        # wave.plot()
        # plt.show()  # 显示波形图

        spectrum = wave.make_spectrum()
        # spectrum.plot()
        # thinkplot.show()  # 显示频谱图

        spectrum.low_pass(cutoff, factor)  # 低通滤波
        # spectrum.plot()
        # thinkplot.show()
        wave = spectrum.make_wave()
        wave.write(output_folder_path + file_name)


def band_stop_filter(file_path, output_path, low_cutoff=100, high_cutoff=500, factor=0):
    """
    带阻滤波器，滤掉高低阈值之间的波

    :param file_path: 输入文件
    :param output_path: 输出文件
    :param low_cutoff: 低阈值，默认100
    :param high_cutoff: 高阈值，默认500
    :param factor: 滤波参数，指阈值之内的频率所乘的系数，默认0
    :return: None

    Examples
    --------
    band_stop_filter('./record/origin/record1.wav', './record/after_filtering/record1.wav',
                     low_cutoff=100, high_cutoff=500, factor=0)
    """
    wave = thinkdsp.read_wave(file_path)
    # wave.plot()
    # plt.show()  # 显示波形图

    spectrum = wave.make_spectrum()
    # spectrum.plot()
    # thinkplot.show()  # 显示频谱图

    spectrum.band_stop(low_cutoff, high_cutoff, factor)  # 带阻滤波
    # spectrum.plot()
    # thinkplot.show()
    wave = spectrum.make_wave()
    wave.write(output_path)


def band_stop_filter__for_folder(input_folder_path, output_folder_path, low_cutoff=100, high_cutoff=500, factor=0):
    """
    对整个文件夹带阻滤波

    :param input_folder_path: 输入文件夹
    :param output_folder_path: 输出文件夹
    :param low_cutoff: 低阈值，默认100
    :param high_cutoff: 高阈值，默认500
    :param factor: 滤波参数，指阈值之内的频率所乘的系数，默认0
    :return: None

    Examples
    --------
    band_stop_filter__for_folder('./record/origin/', './record/after_filtering/',
                                 low_cutoff=100, high_cutoff=500, factor=0)
    """
    for file_name in [x for x in os.listdir(input_folder_path) if x.endswith('.wav')]:
        file_path = os.path.join(input_folder_path, file_name)
        wave = thinkdsp.read_wave(file_path)
        # wave.plot()
        # plt.show()  # 显示波形图

        spectrum = wave.make_spectrum()
        # spectrum.plot()
        # thinkplot.show()  # 显示频谱图

        spectrum.band_stop(low_cutoff, high_cutoff, factor)  # 带阻滤波
        # spectrum.plot()
        # thinkplot.show()
        wave = spectrum.make_wave()
        wave.write(output_folder_path + file_name)


'''---------------------------------------下面是端点检测相关---------------------------------------'''


def save_wave_file(filename, wave_data, sampling_rate=16000, subtype="PCM_16"):
    """
    将原始数据存储为wav格式文件

    :param filename: 文件路径+文件名
    :param wave_data: 数组形式数据原始数据
    :param sampling_rate: 采样率，默认16kHz
    :param subtype: 声音文件类型，默认"PCM_16"
    :return: None
    """
    sf.write(filename, wave_data, sampling_rate, subtype)


def audio_split_single(path_input,
                       audio_type="wav",
                       frame_len=(400, 240),
                       min_interval=(20, 20),
                       e_low_multifactor=(1.0, 0.5),
                       zcr_multifactor=(0.8, 1.0),
                       ):
    """
    对单个文件进行端点检测(只支持wav格式)，在音频所在的路径建立一个文件夹

    :param path_input: 输入的文件路径
    :param audio_type: 输出音频文件格式
    :param frame_len: 一帧时长，单位采样点数，默认为400/240，包括第一次端点检测[0]和之后的再次端点检测[1]
    :param min_interval: 最小浊音间隔，默认都为20帧
    :param e_low_multifactor: 能量低阈值倍乘因子，默认第一次1.0，第二次0.5
    :param zcr_multifactor: 过零率阈值倍乘因子，默认第一次0.8，第二次1.0
    :return: None
    """
    filename_with_type = os.path.basename(path_input)   # 带有格式的文件名
    if filename_with_type.endswith('.wav'):
        file_folder, mid, tail = path_input.partition('.wav')   # 为之后创建文件夹做准备
        filename, mid, tail = filename_with_type.partition('.wav')  # 不带有格式的文件名，方便给之后的文件命名
        if os.path.exists(file_folder):
            shutil.rmtree(file_folder)  # 有大文件夹或有占用就给删了
        os.mkdir(file_folder)   # 大文件夹，储存之后端点检测所有的数据
        save_path1 = os.path.join(file_folder, 'save_path_split1')
        save_path2 = os.path.join(file_folder, 'output')
        os.mkdir(save_path1)
        os.mkdir(save_path2)  # 两次端点检测之后的数据的文件夹
        save_path1 = save_path1 + '/'
        save_path2 = save_path2 + '/'   # 方便文件命名
        # print("音频数据处理中...")
        # 调用ffmpeg，将任意格式音频文件转换为.wav文件，pcm有符号16bit,1：单通道,16kHz，不显示打印信息
        # subprocess.run("ffmpeg -loglevel quiet -y -i %s -acodec pcm_s16le -ac 1 -ar 16000 %s" % (audio_raw, audio_path))
        # print("---------- STEP1: 总体端点检测，分割长音频----------")
        vad = VAD(path_input, frame_len=frame_len[0], min_interval=min_interval[0],
                  e_low_multifactor=e_low_multifactor[0], zcr_multifactor=zcr_multifactor[0])  # 语音端点检测
        # vad.plot()
        # print("共生成{}段语音".format(len(vad.wav_dat_split)))
        # print("---------- STEP2: 对分割后的音频再次进行端点检测----------")
        wave_num = 0
        for index in range(len(vad.wav_dat_split)):
            file_name = save_path1 + filename + \
                        "_%03d.%s" % (index, audio_type)  # 000_000-999_999.wav式命名
            save_wave_file(file_name, vad.wav_dat_split[index])
            _vad = VAD(file_name, frame_len=frame_len[1], min_interval=min_interval[1],
                       e_low_multifactor=e_low_multifactor[1], zcr_multifactor=zcr_multifactor[1], pt=False)  # 语音端点检测
            wave_num += len(_vad.wav_dat_split)
            for i in range(len(_vad.wav_dat_split)):  # 依次保存端点检测后语音文件中所有的有效语音段
                if i == 0:  # 若仅分割成一段，直接保存
                    file_name = save_path2 + filename + \
                                "_%03d.%s" % (index, audio_type)  # 000_000-999_999.wav式命名
                else:  # 否则按名_序号保存
                    file_name = save_path2 + filename + \
                                "_%03d_%d.%s" % (index, i, audio_type)  # 000_000_0-999_999_9.wav式命名
                save_wave_file(file_name, _vad.wav_dat_split[i])
        # print("最终共{}段语音保存完毕".format(wave_num))
    else:
        print("请输入wav格式的音频")


audio_path_raw = './point_check/origin/'  # 原始音频文件夹
audio_path_wav = './point_check/convert2wav/'  # 原始音频转换为.wav文件 文件夹
save_path_split1 = './point_check/detected_split1/'  # 第一次分割后音频保存目录
save_path_split2 = './point_check/detected_split2/'  # 第二次分割后音频保存目录
save_path_duration = './point_check/duration_limit/'  # 限制语音时长后保存目录


def audio_split(input_file_folder=audio_path_raw,
                output_file_folder=audio_path_wav,
                save_chunks_file_folder=(save_path_split1, save_path_split2),
                audio_type="wav",
                frame_len=(400, 240),
                min_interval=(20, 20),
                e_low_multifactor=(1.0, 0.5),
                zcr_multifactor=(0.8, 1.0),
                ):
    """
    音频转换与分割

    :param input_file_folder: 音频输入文件夹
    :param output_file_folder: 音频转换输出文件夹
    :param save_chunks_file_folder: 分割后音频保存文件夹:第一次和第二次
    :param audio_type: 输出音频文件格式
    :param frame_len: 一帧时长，单位采样点数，默认为400/240，包括第一次端点检测[0]和之后的再次端点检测[1]
    :param min_interval: 最小浊音间隔，默认都为20帧
    :param e_low_multifactor: 能量低阈值倍乘因子，默认第一次1.0，第二次0.5
    :param zcr_multifactor: 过零率阈值倍乘因子，默认第一次0.8，第二次1.0
    :return: None
    """
    if os.path.exists(output_file_folder):
        shutil.rmtree(output_file_folder)  # 先删除输出文件夹
    os.mkdir(output_file_folder)  # 重新创建
    if os.path.exists(save_chunks_file_folder[0]):
        shutil.rmtree(save_chunks_file_folder[0])  # 先删除输出文件夹
    os.mkdir(save_chunks_file_folder[0])  # 重新创建
    if os.path.exists(save_chunks_file_folder[1]):
        shutil.rmtree(save_chunks_file_folder[1])  # 先删除输出文件夹
    os.mkdir(save_chunks_file_folder[1])  # 重新创建
    for each_file in os.listdir(input_file_folder):  # 遍历原始音频文件
        audio_raw = os.path.join(input_file_folder, each_file)  # 原始音频文件相对路径
        audio_path = output_file_folder + each_file.split(".")[0] + "." + audio_type  # 转换后存储路径，文件名
        print(each_file + "音频数据处理中...")
        # 调用ffmpeg，将任意格式音频文件转换为.wav文件，pcm有符号16bit,1：单通道,16kHz，不显示打印信息
        subprocess.run("ffmpeg -loglevel quiet -y -i %s -acodec pcm_s16le -ac 1 -ar 16000 %s" % (audio_raw, audio_path))
        print("----------{} STEP1: 总体端点检测，分割长音频----------".format(each_file))
        vad = VAD(audio_path, frame_len=frame_len[0], min_interval=min_interval[0],
                  e_low_multifactor=e_low_multifactor[0], zcr_multifactor=zcr_multifactor[0])  # 语音端点检测
        # vad.plot()
        print("共生成{}段语音".format(len(vad.wav_dat_split)))
        print("----------{} STEP2: 对分割后的音频再次进行端点检测----------".format(each_file))
        wave_num = 0
        for index in range(len(vad.wav_dat_split)):
            file_name = save_chunks_file_folder[0] + each_file.split(".")[0] + \
                        "_%03d.%s" % (index, audio_type)  # 000_000-999_999.wav式命名
            save_wave_file(file_name, vad.wav_dat_split[index])
            _vad = VAD(file_name, frame_len=frame_len[1], min_interval=min_interval[1],
                       e_low_multifactor=e_low_multifactor[1], zcr_multifactor=zcr_multifactor[1], pt=False)  # 语音端点检测
            wave_num += len(_vad.wav_dat_split)
            for i in range(len(_vad.wav_dat_split)):  # 依次保存端点检测后语音文件中所有的有效语音段
                if i == 0:  # 若仅分割成一段，直接保存
                    file_name = save_chunks_file_folder[1] + each_file.split(".")[0] + \
                        "_%03d.%s" % (index, audio_type)  # 000_000-999_999.wav式命名
                else:  # 否则按名_序号保存
                    file_name = save_chunks_file_folder[1] + each_file.split(".")[0] + \
                        "_%03d_%d.%s" % (index, i, audio_type)  # 000_000_0-999_999_9.wav式命名
                save_wave_file(file_name, _vad.wav_dat_split[i])
        print("最终共{}段语音保存完毕".format(wave_num))


def audio_duration_limit(input_file_folder=save_path_split2, output_file_folder=save_path_duration,
                         min_dura=200, max_dura=1500):
    """
    通过变速，限制音频时长

    :param input_file_folder: 输入音频文件夹
    :param output_file_folder: 输出音频文件夹
    :param min_dura: 最小音频时长，默认200ms
    :param max_dura: 最大音频时长，默认1500ms
    :return: None
    """
    if input_file_folder == output_file_folder:
        print("输入和输出路径相同，请选择不同的输出文件路径")
        return
    empty = True  # 当前输入路径是否存在非音频文件
    if os.path.exists(output_file_folder):
        shutil.rmtree(output_file_folder)  # 先删除输出文件夹
    os.mkdir(output_file_folder)  # 重新创建
    try:
        for each_file in os.listdir(input_file_folder):  # 遍历原始音频文件
            audio_raw = os.path.join(input_file_folder, each_file)  # 原始音频文件相对路径
            shutil.copy(audio_raw, output_file_folder)  # 复制原始音频至输出路径
            _input = output_file_folder + each_file  # ffmpeg输入文件
            audio_duration_original = len(sf.read(_input)[0]) / sf.read(_input)[1] * 1000  # 原始音频时长
            i = 0  # 每次加减速编号
            while len(sf.read(_input)[0]) / sf.read(_input)[1] * 1000 > max_dura:  # 当输入音频超过max_dura ms时
                _output = output_file_folder + each_file.split(".")[0] + "_%03d.%s" % (i, each_file.split(".")[1])
                # 每次1.2倍速度加快音频，不显示打印信息
                subprocess.run("ffmpeg -loglevel quiet -y -i %s -af atempo=%s %s" % (_input, 1.2, _output))
                os.remove(_input)  # 删除原音频文件
                os.rename(_output, output_file_folder + each_file)  # 重新命名已倍速音频文件名为原文件名
                i += 1  # 编号递增
            while len(sf.read(_input)[0]) / sf.read(_input)[1] * 1000 < min_dura:  # 当输入音频低于min_dura ms时
                _output = output_file_folder + each_file.split(".")[0] + "_%03d.%s" % (i, each_file.split(".")[1])
                # 每次0.8倍速度减缓音频，不显示打印信息
                subprocess.run("ffmpeg -loglevel quiet -y -i %s -af atempo=%s %s" % (_input, 0.8, _output))
                os.remove(_input)  # 删除原音频文件
                os.rename(_output, output_file_folder + each_file)  # 重新命名已倍速音频文件名为原文件名
                i += 1  # 编号递增
            audio_duration_now = len(sf.read(_input)[0]) / sf.read(_input)[1] * 1000  # 变速后音频时长
            print("{}: {}ms -> {}ms".format(each_file, audio_duration_original, audio_duration_now))
        empty = False
    except PermissionError:
        pass
    else:
        print("----------已完成----------")
    finally:
        if empty:
            print("当前输入路径存在非音频文件或格式错误")


def delete_unusable_wav(input_file_folder=save_path_duration, time=500):
    """
    删除不可用音频

    :param input_file_folder: 输入文件夹
    :param time: 时间阈值，时间低于阈值的音频被删除
    :return: None
    """
    for each_file in os.listdir(input_file_folder):  # 遍历原始音频文件
        audio_raw = os.path.join(input_file_folder, each_file)  # 原始音频文件相对路径
        _input = input_file_folder + each_file  # ffmpeg输入文件
        audio_duration_original = len(sf.read(_input)[0]) / sf.read(_input)[1] * 1000  # 原始音频时长
        if audio_duration_original < time:
            os.remove(audio_raw)


"""if __name__ == "__main__":
    audio_split(input_file_folder=audio_path_raw,
                output_file_folder=audio_path_wav,
                save_chunks_file_folder=(save_path_split1, save_path_split2),
                audio_type="wav")
    print("----------STEP3: 限制最终的音频时长为0ms ~ 1500ms----------")
    audio_duration_limit(input_file_folder=save_path_split2)"""


"""下面一段用于多级文件夹的多语音端点检测"""
'''if __name__ == "__main__":
    total_folders = ['E:\Procedure\python\\timing_machine_pycharm\\test_data\\', 'E:\Procedure\python\\timing_machine_pycharm\\training_data\\']
    for total_folder in total_folders:
        for folder in os.listdir(total_folder):
            folder_path = os.path.join(total_folder, folder)
            if not os.path.isdir(folder_path):
                continue
            audio_path_raw = None
            audio_path_wav = None
            save_path_split1 = None
            save_path_split2 = None
            save_path_duration = None
            for subfolder in [x for x in os.listdir(folder_path)]:
                subfolder_path = os.path.join(folder_path, subfolder)
                if not os.path.isdir(subfolder_path):
                    continue
                if subfolder == folder + '_after_filtering':
                    audio_path_raw = subfolder_path + '\\'
                elif subfolder == 'convert2wav':
                    audio_path_wav = subfolder_path + '\\'
                elif subfolder == 'detected_split1':
                    save_path_split1 = subfolder_path + '\\'
                elif subfolder == 'detected_split2':
                    save_path_split2 = subfolder_path + '\\'
                elif subfolder == 'duration_limit':
                    save_path_duration = subfolder_path + '\\'
            print(audio_path_raw, audio_path_wav, save_path_split1, save_path_split2, save_path_duration)
            audio_split(input_file_folder=audio_path_raw,
                        output_file_folder=audio_path_wav,
                        save_chunks_file_folder=(save_path_split1, save_path_split2),
                        audio_type="wav",
                        frame_len=(400, 240),
                        min_interval=(15, 15),
                        e_low_multifactor=(1.0, 0.5),
                        zcr_multifactor=(0.8, 0.8))
            print("----------STEP3: 限制最终的音频时长为0ms ~ 1500ms----------")
            delete_unusable_wav(input_file_folder=save_path_duration, time=200)
            audio_duration_limit(input_file_folder=save_path_split2,
                                 output_file_folder=save_path_duration,
                                 min_dura=0,
                                 max_dura=1500)
            print("----------------------全部结束----------------------")'''
