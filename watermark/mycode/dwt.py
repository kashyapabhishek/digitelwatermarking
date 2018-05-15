import cv2
import pywt
import numpy as np
from django.core.files.storage import FileSystemStorage


def DWT(cover, watermark):
    cover = 'C:/Users/saumy/PycharmProjects/Dwt watermark/src/media/'+str(cover)
    print(cover)
    watermark = 'C:/Users/saumy/PycharmProjects/Dwt watermark/src/media/'+str(watermark)
    print(watermark)
    cover = cv2.imread(cover, 0)
    watermark = cv2.imread(watermark, 0)
    cover = cv2.resize(cover, (300, 300))
    watermark = cv2.resize(watermark, (150, 150))

    # DWT on cover image
    cover = np.float32(cover)
    cover /= 255;
    channel = pywt.dwt2(cover, 'haar')
    cA, (cH, cV, cD) = channel

    watermark = np.float32(watermark)
    watermark /= 255;

    # Embedding
    channel = (0.4 * cA + 0.1 * watermark, (cH, cV, cD))
    watermarked = pywt.idwt2(channel, 'haar')
    cv2.imwrite('C:/Users/saumy/PycharmProjects/Dwt watermark/src/media/marked.jpg', watermarked)

    return 'C:/Users/saumy/PycharmProjects/Dwt watermark/src/media/marked.jpg'


def extract_dwt(cover, watermark):
    cover = 'C:/Users/saumy/PycharmProjects/Dwt watermark/src/media/' + str(cover)
    watermark = 'C:/Users/saumy/PycharmProjects/Dwt watermark/src/media/' + str(watermark)
    cover = cv2.imread(cover, 0)
    watermark = cv2.imread(watermark, 0)

    #cover = cv2.resize(cover, (300, 300))
    #watermark = cv2.resize(watermark, (150, 150))

    # DWT on cover image
    cover = np.float32(cover)
    cover /= 255;
    channel = pywt.dwt2(cover, 'haar')
    cA, (cH, cV, cD) = channel

    # Extraction
    coeffWM = pywt.dwt2(watermark, 'haar')
    hA, (hH, hV, hD) = coeffWM

    extracted = (hA - 0.4 * cA) / 0.1
    extracted *= 255
    extracted = np.uint8(extracted)
    cv2.imwrite('C:/Users/saumy/PycharmProjects/Dwt watermark/src/media/extracted.jpg', extracted)


