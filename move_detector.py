import numpy as np
import cv2
import copy
from itertools import product

background_subtractor = cv2.bgsegm.createBackgroundSubtractorMOG()

def move_detector(frame, first_iteration_indicator, accum_image):
    # If first frame
    if first_iteration_indicator == 1:
        height, width = frame.shape[:2]
        accum_image = np.zeros((height, width), np.uint8)
    else:
        filter = background_subtractor.apply(frame)  # remove the background
        filter = cv2.GaussianBlur(filter, (5, 5), 0)

        threshold = 2
        maxValue = 2
        ret, th1 = cv2.threshold(filter, threshold, maxValue, cv2.THRESH_BINARY)
        # Пороговая фильтрация
        th1[th1 < 2] = 0

        kernel = np.ones((5, 5), np.uint8)
        th1 = cv2.erode(th1, kernel, iterations=2)
        th1 = cv2.dilate(th1, kernel, iterations=1)

        # Добавляем в аккум
        accum_image = cv2.add(accum_image, th1)
        accum_image = cv2.GaussianBlur(accum_image, (5, 5), 0)

        kernel = np.ones((2, 2), np.uint8)
        accum_image = cv2.erode(accum_image, kernel, iterations=1)
        accum_image[accum_image < 2] = 0  # Пороговая фильтрация

        # Поиск контуров
        cnts = cv2.findContours(accum_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        # Создаем список для хранения прямоугольников, ограничивающих контуры
        rects = []
        for c in cnts:
            x, y, w, h = cv2.boundingRect(c)
            rects.append((x, y, w, h))
        return rects
