import pygame
import jieba
import jieba.posseg as psg
import pyautogui
import numpy as np
import torch
import easyocr
import cv2
import difflib
import re
import Levenshtein as lev  # 计算字符串相似度
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "True"
use_gpu = torch.cuda.is_available()
# print(use_gpu)


def sentences_to_order(sentences):
    """
    完整语句转化为命令
    
    :param sentences: 语句(list)
    :return: 命令(list)
    """
    sentence = sentences[0]
    words = [(x.word, x.flag) for x in psg.cut(sentence)]
    orders = []
    for i, word in enumerate(words):
        if word[1] == "v":
            ck = 0
            for j in range(i+1, len(words)):
                if words[j][1] == "v":
                    ck = -0.5
                    break
                elif words[j][1] == "n" or words[j][1] == "vn":
                    ck = j
                    break
            if ck == -0.5:
                continue
            order = (words[i][0], words[ck][0])
            orders.append(order)
    return orders


def order_to_pic(order, pic_path, font_="../data/fonts/microsoft_yahei.ttf", back_color=(0, 0, 0),
                 color=(255, 255, 255)):
    """
    命令转图片
    将获取到的命令转化成图片形式

    :param order: 命令(tuple)
    :param pic_path: 图片保存路径(str)
    :param font_: 字体(str)
    :param back_color: rgb背景颜色(tuple)
    :param color: rgb字体颜色(tuple)
    :return: None
    """
    pygame.init()  # pygame初始化
    font = pygame.font.Font(font_, 64)  # 设置字体和字号，自定义。问题在于无法确定屏幕字体和大小
    ftext = font.render(order[1], True, back_color, color)  # 渲染图片，设置背景颜色和字体样式, 前面的颜色是字体颜色
    pygame.image.save(ftext, pic_path)  # 保存图片


def find_pic_location(pic_path):
    """
    找寻图片在屏幕截屏上的位置中心
    limit: 只有图像与截屏中一部分100%相同才能用

    :param pic_path: 图片路径
    :return: 中心位置(tuple)
    """
    word_location = pyautogui.locateOnScreen(pic_path, grayscale=True, confidence=.5)  # 传入要识别的图片,返回屏幕所在位置
    x, y = pyautogui.center(word_location)  # 转化为 x,y坐标
    return (x, y)


def str_sim(str1, str2, method=5):
    """
    字符串相似度

    :param str1: 字符串1(str)
    :param str2: 字符串2(str)
    :param method: 距离计算方式(int):
                    0, difflib距离(python自带)
                    1, 编辑距离
                    2, 莱文斯坦比
                    3, jaro距离
                    4, jaro-winkler距离
    :return: 相似度(float)
    """
    if method == 1:
        sim = lev.distance(str1, str2)
    elif method == 2:
        sim = lev.ratio(str1, str2)
    elif method == 3:
        sim = lev.jaro(str1, str2)
    elif method == 4:
        sim = lev.jaro_winkler(str1, str2)
    elif method == 5:
        if lev.distance(str1, str2) == 0:
            return 1
        else:
            sim = difflib.SequenceMatcher(None, str1, str2).quick_ratio() * lev.ratio(str1, str2) \
                  * lev.jaro(str1, str2) * lev.jaro_winkler(str1, str2) / lev.distance(str1, str2)
    else:
        sim = difflib.SequenceMatcher(None, str1, str2).quick_ratio()
    return sim


def ocr(pic_path, OCR_THRES=0.1):
    """
    屏幕取词

    :param pic_path: 图片路径
    :return: 所有文字包括其坐标(array)
    """
    # 创建reader对象
    # reader = easyocr.Reader(['ch_sim', 'en'])
    reader = easyocr.Reader(['ch_sim'])
    result = reader.readtext(pic_path)  # 读取图像
    # print(result)
    for res in result[:]:
        if bool(re.search(r"[*~ ^@()%\"]", res[1])):
            result.remove(res)
        elif res[2] < OCR_THRES:
            result.remove(res)
    # print(result)
    out = []
    for res in result[:]:
        anchor = []
        four_location = res[0]
        x = (four_location[0][0] + four_location[2][0]) // 2
        y = (four_location[0][1] + four_location[2][1]) // 2  # 计算框中心位置
        anchor.append((x, y))
        anchor.append(res[1])
        anchor.append(res[2])
        out.append(anchor)
    return out


def act(order, OCR_THRES=0.1, STR_SIM_THRES=0.1):
    """
    执行具体动作

    :param order: 命令(tuple)
    :return: None
    """
    list_ = ['单击', '打开', '左击', '右击', '双击']  # 操作列表
    action = order[0]
    target = order[1]
    im_rgb = np.array(pyautogui.screenshot())
    im_bgr = im_rgb[..., ::-1]  # rgb转bgr
    cv2.imwrite("./tmp.png", im_bgr)
    try:
        locations = ocr("./tmp.png", OCR_THRES=OCR_THRES)
    except Exception:
        raise Exception("现在图像检测算法还很不稳定")
    
    # print(locations)
    for loc in locations[:]:
        tmp_sim = str_sim(target, loc[1], 5)
        if tmp_sim < STR_SIM_THRES:
            locations.remove(loc)  # 匹配相似度
        else:
            loc[2] = tmp_sim
    assert (len(locations) > 0)
    max_loc = []
    simi = 0
    for loc in locations[:]:
        if loc[2] > simi:
            max_loc = loc
            simi = loc[2]
    # print(simi)
    x, y = max_loc[0]
    
    if action == list_[0] or action == list_[2]:
        pyautogui.click(x, y)
    elif action == list_[3]:
        pyautogui.rightClick(x, y)
    elif action == list_[1] or action == list_[4]:
        pyautogui.doubleClick(x, y)
    os.remove("./tmp.png")


if __name__ == "__main__":
    pass
