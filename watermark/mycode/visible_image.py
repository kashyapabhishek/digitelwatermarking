from imutils import paths
import numpy as np
import cv2


class VisibleImage:

    def imageMark(self,watermarkimage, mainimage ):
        print(watermarkimage)
        print(mainimage)
        print(watermarkimage)
        wfile = 'C:/Users/saumy/PycharmProjects/Dwt watermark/src/media/'+str(watermarkimage)
        print('wfile : '+wfile)
        watermark = cv2.imread(wfile, cv2.IMREAD_UNCHANGED)
        (wH, wW) = watermark.shape[:2]

        (B, G, R, A) = cv2.split(watermark)
        B = cv2.bitwise_and(B, B, mask=A)
        G = cv2.bitwise_and(G, G, mask=A)
        R = cv2.bitwise_and(R, R, mask=A)
        watermark = cv2.merge([B, G, R, A])
        image = cv2.imread('C:/Users/saumy/PycharmProjects/Dwt watermark/src/media/'+str(mainimage))
        (h, w) = image.shape[:2]
        image = np.dstack([image, np.ones((h, w), dtype="uint8") * 255])
        overlay = np.zeros((h, w, 4), dtype="uint8")
        overlay[h - wH - 10:h - 10, w - wW - 10:w - 10] = watermark
        output = image.copy()
        cv2.addWeighted(overlay, 0.5, output, 1.0, 0, output)

        cv2.imwrite('C:/Users/saumy/PycharmProjects/Dwt watermark/src/media/' + str(mainimage), output)



