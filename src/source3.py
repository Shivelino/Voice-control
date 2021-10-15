import librosa
import numpy as np
import torch


def load_audio(audio_path, mode='train', win_length=400, sr=16000, hop_length=160, n_fft=512, spec_len=65):
    """
    神经网络输入预加载音频数据
    
    :param audio_path: 音频路径(str)
    :param mode: 模式(str)
    :param win_length: 窗口长度(int)
    :param sr: 采样率(int)
    :param hop_length: 跳跃长度(int)
    :param n_fft: 快速傅里叶变换窗口(int)
    :param spec_len: 音频最低长度(int)
    :return: 谱图(array)
    """
    # 读取音频数据
    wav, sr_ret = librosa.load(audio_path, sr=sr)
    # 数据拼接
    if mode == 'train':
        extended_wav = np.append(wav, wav)
        if np.random.random() < 0.3:
            extended_wav = extended_wav[::-1]
    else:
        extended_wav = np.append(wav, wav[::-1])
    # 计算短时傅里叶变换
    linear = librosa.stft(extended_wav, n_fft=n_fft, win_length=win_length, hop_length=hop_length)
    linear_T = linear.T
    mag, _ = librosa.magphase(linear_T)
    mag_T = mag.T
    freq, freq_time = mag_T.shape
    assert freq_time >= spec_len, "非静音部分长度不能低于0.3s"  # 主要防止突然性噪声
    if mode == 'train':
        # 随机裁剪
        rand_time = np.random.randint(0, freq_time - spec_len)
        spec_mag = mag_T[:, rand_time:rand_time + spec_len]
    else:
        spec_mag = mag_T[:, :spec_len]
    mean = np.mean(spec_mag, 0, keepdims=True)
    std = np.std(spec_mag, 0, keepdims=True)
    spec_mag = (spec_mag - mean) / (std + 1e-5)
    spec_mag = spec_mag[np.newaxis, :]
    return spec_mag


def infer(model, input_shape, device, audio_path):
    """
    网络推理
    
    :param model: 网络模型(torch.jit._script.RecursiveScriptModule)
    :param input_shape: 输入尺寸(tuple)
    :param device: 运行设备(str)
    :param audio_path: 待测音频路径(str)
    :return: 特征向量(array)
    """
    data = load_audio(audio_path, mode='infer', spec_len=input_shape[2])
    data = data[np.newaxis, :]
    data = torch.tensor(data, dtype=torch.float32, device=device)
    # 执行预测
    feature = model(data)
    return feature.data.cpu().numpy()


def cmp_similarity__bool(model, input_shape, device, thres, PATH1, PATH2):
    """对比相似度(Not used)"""
    feature1 = infer(model, input_shape, device, PATH1)[0]
    feature2 = infer(model, input_shape, device, PATH2)[0]
    # 对角余弦值
    dist = np.dot(feature1, feature2) / (np.linalg.norm(feature1) * np.linalg.norm(feature2))
    if dist > thres:
        print("1，相似度为：{}".format(dist))
        return True
    else:
        print("0，相似度为：{}".format(dist))
        return False


if __name__ == '__main__':
    # 每次都加载模型的话，速度cpu>cuda,如果长时间用，挂着cuda还是比cpu快很多
    pass
