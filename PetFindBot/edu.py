import cv2
import numpy as np
from dbase import choice_human_finder, choice_human_owner


def selection(person):
    if person.status == 1:
        all = choice_human_finder(person.city, person.type_pet)
    else:
        all = choice_human_owner(person.city, person.type_pet)

    idx = 0
    for hum in all:
        if hum.sex_pet != person.sex_pet or hum.sex_pet == None:
            if hum.name_pet != person.name_pet or hum.name_pet == None:
                del all[idx]
        idx += 1

    return all


def calculate_similarity(image_path1, image_path2):
    img1 = cv2.imread(image_path1)
    img2 = cv2.imread(image_path2)

    # преобразование изображения в цветовое пространство HSV
    hsv1 = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
    # вычисление гистограммы
    hist1 = cv2.calcHist([hsv1], [0, 1], None, [180, 256], [0, 180, 0, 256])
    hist2 = cv2.calcHist([hsv2], [0, 1], None, [180, 256], [0, 180, 0, 256])
    # нормализация гистограммы
    cv2.normalize(hist1, hist1, alpha=0, beta=1, norm_type=cv2.NORM_L1)
    cv2.normalize(hist2, hist2, alpha=0, beta=1, norm_type=cv2.NORM_L1)
    # сравнение гистограммы
    similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    # процент
    similarity_percentage = similarity * 100

    return similarity_percentage


def selection2(person):
    x = 75
    true = []
    image_true = selection(person)
    for i in image_true:
        percent = calculate_similarity(person.photo, i.photo)
        if percent > x:
            true.append(i)

    return true
