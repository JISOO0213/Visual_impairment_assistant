import xml.etree.ElementTree as ET
from collections import defaultdict
from glob import glob
from sklearn.model_selection import train_test_split
import os
from tqdm import tqdm
import shutil

def _pretty_print(current, parent=None, index=-1, depth=0):
    for i, node in enumerate(current):
        _pretty_print(node, current, i, depth + 1)
    if parent is not None:
        if index == 0:
            parent.text = '\n' + ('\t' * depth)
        else:
            parent[index - 1].tail = '\n' + ('\t' * depth)
        if index == len(parent) - 1:
            current.tail = '\n' + ('\t' * (depth - 1))

label_dic = {'person' : 1, 'person on vehicle' : 2, 'car' : 3, 'bicycle' : 4, 'motorbike' : 5, 'non motorized vehicle' : 6, 'static person' : 7, 'distractor' : 8, 'occluder' : 9, 'occluder on the ground' : 10, 'occluder full' : 11, 'reflection' : 12, 'bus' : 13, 'scooter' : 14, 'bench' : 15, 'traffic_light' : 16, 'bollard' : 17, 'truck' : 18}

xml_list = glob('./xmls/*.xml')

#resizing
dw = 1./1920
dh = 1./1080
dic_li = defaultdict(list)
for xmls in xml_list:
    filepath = xmls
    tree = ET.parse(filepath)
    for img in (tree.getroot()).findall('image'):
        boxes = img.findall('box')
        for box in boxes:
            label = box.attrib.get('label')
            for key, idx in label_dic.items():
                if label == key:
                    name = img.attrib.get('name')
                    xbr = int(float(box.attrib.get('xbr')))
                    ybr = int(float(box.attrib.get('ybr')))
                    xtl = int(float(box.attrib.get('xtl')))
                    ytl = int(float(box.attrib.get('ytl')))
                    w = xbr - xtl
                    h = ybr - ytl
                    x = round((xbr - w / 2) * dw, 6)
                    y = round((ybr - h / 2) * dh, 6)
                    w = round(w * dw, 6)
                    h = round(h * dh, 6)
                    if x > 1:
                        x = 1
                    elif x < 0:
                        x = 0
                    if y > 1:
                        y = 1
                    elif y < 0:
                        y = 0
                    if w > 1:
                        w = 1
                    elif w < 0:
                        w = 0
                    if h > 1:
                        h = 1
                    elif h < 0:
                        h = 0
                    dic_li[name].append([str(label_dic[label]) + ' ' + str(x) + ' ' + str(y) + ' ' + str(w) + ' ' + str(h)])

xml_key = dic_li.keys()



train_xml_list, valid_xml_list = train_test_split(list(xml_key), test_size = 0.2, random_state = 1173)


# 1. xml_to_txt 파일로 옮기기
for tr in train_xml_list:
    with open('./xml_to_txt/train/' + tr[:-4] + '.txt', 'w', encoding = 'utf-8') as f:
        for k in dic_li[tr]:
            f.write(' '.join(k) + '\n')

for vr in valid_xml_list:
    with open('./xml_to_txt/valid/' + vr[:-4] + '.txt', 'w', encoding = 'utf-8') as f:
        for k in dic_li[vr]:
            f.write(' '.join(k) + '\n')

# 2. imgs 파일로 옮기기
for tr in tqdm(train_xml_list):
    with open('./imgs/' + tr[:-4] + '.txt', 'w', encoding = 'utf-8') as f:
        for k in dic_li[tr]:
            f.write(' '.join(k) + '\n')

for vr in tqdm(valid_xml_list):
    with open('./imgs/' + vr[:-4] + '.txt', 'w', encoding = 'utf-8') as f:
        for k in dic_li[vr]:
            f.write(' '.join(k) + '\n')