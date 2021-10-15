# 概述

此源代码是一个内嵌了基于声纹识别的语音命令和输入程序。本项目参考了Autoencoder原理，使用数据集训练出了一个声纹提取模型，其泛化能力较好（理论上数据集越强，泛化能力越好），同时结合了ASR和OCR等技术。

# 使用环境

 - Win10(有些依赖库只能在Windows10下运行)
 - Python 3.8
 - Pytorch 1.8.1
 - Pyaudio 0.2.11

# 安装环境
1. 安装Pytorch
```shell
conda install pytorch==1.8.1 torchvision==0.9.1 torchaudio==0.8.1 cudatoolkit=10.2 -c pytorch
```
2. 安装Pyaudio
```shell
conda install pyaudio
```
3. 安装其他依赖库
```shell
pip install -r requirements.txt
```

