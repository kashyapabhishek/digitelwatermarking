import os
import re
import cv2
import time
import pywt
import argparse
import pygame
import numpy as np
from io import StringIO
from PIL import Image

pygame.init()

ORIGIN_RATE = 0.4
WATERMARK_RATE = 0.4
TMP_PATH = "word2pic.png"


def opencv_image_from_stringio(watermark_word):
    img = Image.new("RGB", (512, 512), (255, 255, 255))
    font = pygame.font.Font("msyh.ttf", 100)
    rtext = font.render(watermark_word, True, (0, 0, 205), (255, 255, 255))
    sio = StringIO.StringIO()
    pygame.image.save(rtext, sio)
    sio.seek(0)
    line = Image.open(sio)
    img.paste(line, (200, 200))
    img.save(TMP_PATH)
    return cv2.imread(TMP_PATH)


def dwt2_single(img):
    coeffs_1 = pywt.dwt2(img, 'haar', mode='reflect')
    coeffs_2 = pywt.dwt2(coeffs_1[0], 'haar', mode='reflect')
    coeffs_3 = pywt.dwt2(coeffs_2[0], 'haar', mode='reflect')
    return coeffs_1, coeffs_2, coeffs_3


def dwt2(img1, img2):
    coeffs1_1, coeffs1_2, coeffs1_3 = dwt2_single(img1)
    coeffs2_1, coeffs2_2, coeffs2_3 = dwt2_single(img2)
    return coeffs1_1, coeffs1_2, coeffs1_3, coeffs2_3


def idwt2(img, coeffs1_1_h, coeffs1_2_h, coeffs1_3_h):
    cf3 = (img, coeffs1_3_h)
    img = pywt.idwt2(cf3, 'haar', mode='reflect')

    cf2 = (img, coeffs1_2_h)
    img = pywt.idwt2(cf2, 'haar', mode='reflect')

    cf1 = (img, coeffs1_1_h)
    img = pywt.idwt2(cf1, 'haar', mode='reflect')
    return img


def channel_embedding(origin_image_chan, watermark_img_chan):
    coeffs1_1, coeffs1_2, coeffs1_3, coeffs2_3 = dwt2(origin_image_chan, watermark_img_chan)
    embedding_image = cv2.add(cv2.multiply(ORIGIN_RATE, coeffs1_3[0]), cv2.multiply(WATERMARK_RATE, coeffs2_3[0]))
    embedding_image = idwt2(embedding_image, coeffs1_1[1], coeffs1_2[1], coeffs1_3[1])
    np.clip(embedding_image, 0, 255, out=embedding_image)
    embedding_image = embedding_image.astype('uint8')
    return embedding_image


def get_watermark(args, flag):
    if flag == "image":
        return cv2.imread(args.watermark)
    else:
        return opencv_image_from_stringio(args.watermark_word)


def img_segment_embedding(watermark_img, origin_image):
    origin_size = origin_image.shape[:2]
    watermark_img = cv2.resize(watermark_img, (origin_size[1], origin_size[0]))
    origin_image_r, origin_image_g, origin_image_b = cv2.split(origin_image)
    watermark_img_r, watermark_img_g, watermark_img_b = cv2.split(watermark_img)

    embedding_image_r = channel_embedding(origin_image_r, watermark_img_r)
    embedding_image_g = channel_embedding(origin_image_g, watermark_img_g)
    embedding_image_b = channel_embedding(origin_image_b, watermark_img_b)

    embedding_image = cv2.merge([embedding_image_r, embedding_image_g, embedding_image_b])
    return embedding_image


def split_img_segments(image, num):
    segments = []
    if num <= 1:
        segments.append(image)
        return segments
    ratio = 1.0 / float(num)
    height = image.shape[0]
    width = image.shape[1]
    pHeight = int(ratio * height)
    pHeightInterval = (height - pHeight) / (num - 1)
    pWidth = int(ratio * width)
    pWidthInterval = (width - pWidth) / (num - 1)
    for i in range(num):
        for j in range(num):
            x = pWidthInterval * i
            y = pHeightInterval * j
            segments.append(image[y:y + pHeight, x:x + pWidth, :])
    return segments


def merge_img_segments(segments, num, shape):
    if num <= 1:
        return segments[0]
    ratio = 1.0 / float(num)
    height = shape[0]


    width = shape[1]
    channel = shape[2]
    image = np.empty([height, width, channel], dtype=int)

    pHeight = int(ratio * height)
    pHeightInterval = (height - pHeight) / (num - 1)
    pWidth = int(ratio * width)
    pWidthInterval = (width - pWidth) / (num - 1)
    cnt = 0
    for i in range(num):
        for j in range(num):
            x = pWidthInterval * i
            y = pHeightInterval * j
            image[y:y + pHeight, x:x + pWidth, :] = segments[cnt]
            cnt += 1
    return image


def embedding(origin_image, watermark_img):
    origin_image = 'C:/Users/saumy/PycharmProjects/Dwt watermark/src/media/'+str(origin_image)
    watermark_img = 'C:/Users/saumy/PycharmProjects/Dwt watermark/src/media/'+str(watermark_img)
    print('original image'+origin_image)
    num = 1
    print("hi")
    origin_image = cv2.imread(origin_image)
    # watermark_img = get_watermark(args, flag)
    watermark_img = cv2.imread(watermark_img)
    origin_img_segments = split_img_segments(origin_image, num)
    embedding_img_segments = []
    for segment in origin_img_segments:
        print(segment)
        embedding_img_segments.append(img_segment_embedding(watermark_img, segment))
    embedding_image = merge_img_segments(embedding_img_segments, num, origin_image.shape)
    cv2.imwrite('C:/Users/saumy/PycharmProjects/Dwt watermark/src/media/watermarked.jpg', embedding_image)
    return '/media/watermarked.jpg'



def channel_extracting(origin_image_chan, embedding_image_chan):
    coeffs1_1, coeffs1_2, coeffs1_3, coeffs2_3 = dwt2(origin_image_chan, embedding_image_chan)
    extracting_img = cv2.divide(cv2.subtract(coeffs2_3[0], cv2.multiply(ORIGIN_RATE, coeffs1_3[0])), WATERMARK_RATE)
    extracting_img = idwt2(extracting_img, (None, None, None), (None, None, None), (None, None, None))
    return extracting_img


def img_segment_extracting(origin_image, embedding_image, num):
    origin_image_r, origin_image_g, origin_image_b = cv2.split(origin_image)
    embedding_image_r, embedding_image_g, embedding_image_b = cv2.split(embedding_image)
    extracting_img_r = channel_extracting(origin_image_r, embedding_image_r)
    extracting_img_g = channel_extracting(origin_image_g, embedding_image_g)
    extracting_img_b = channel_extracting(origin_image_b, embedding_image_b)
    extracting_img = cv2.merge([extracting_img_r, extracting_img_g, extracting_img_b])
    return extracting_img


def extracting(embedding_image, origin_image):
    embedding_image = 'C:/Users/saumy/PycharmProjects/Dwt watermark/src/media/' + str(embedding_image)
    origin_image = 'C:/Users/saumy/PycharmProjects/Dwt watermark/src/media/' + str(origin_image)
    num = 1
    embedding_image = cv2.imread(embedding_image)
    origin_image = cv2.imread(origin_image)
    origin_size = origin_image.shape[:2]
    embedding_image = cv2.resize(embedding_image, (origin_size[1], origin_size[0]))

    origin_img_segments = split_img_segments(origin_image, num)
    embedding_img_segments = split_img_segments(embedding_image, num)
    extracting_img_segments = []
    for i in range(0, num * num):
        extracting_img_segments.append(img_segment_extracting(origin_img_segments[i], embedding_img_segments[i], i))

    extracting_img = merge_img_segments(extracting_img_segments, num, origin_image.shape)
    cv2.imwrite("C:/Users/saumy/PycharmProjects/Dwt watermark/src/media/extrect.jpg", extracting_img)
    return '/media/extrect.jpg'





