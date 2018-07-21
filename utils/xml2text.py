import xml.etree.ElementTree as ET
import glob
import pickle
import os
from os import listdir, getcwd
from os.path import join


classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]

root_path = "/media/baiyu/A2FEE355FEE31FF1/VOCdevkit (2)/VOC2012"
annotation_path = os.path.join(root_path, 'Annotations')
label_path = os.path.join(root_path, 'labels')

def convert(size, box):
    """Convert a xmin, xmax, ymin, ymax format box
    to x, y, w, h format box
    Args:
        size: size of the image
        box: xmin, xmax, ymin, ymax format box
    
    Returns:
        (x, y, w, h): a tuple of x y w h format box
    """
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(xml_path):
    """Given an anotation xml file, write a txt file
    in directory labels with the same name
    as images

    Args: 
        xml_path: path to annotation xml file
    """

    xml_name = os.path.basename(xml_file)
    image_id = os.path.splitext(xml_name)[0]

    in_file = open(xml_file)
    out_file = open(os.path.join(label_path, image_id + '.txt'), 'w')

    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), 
             float(xmlbox.find('xmax').text), 
             float(xmlbox.find('ymin').text), 
             float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


for xml_file in glob.iglob(os.path.join(annotation_path, '*.xml')):
    convert_annotation(xml_file)