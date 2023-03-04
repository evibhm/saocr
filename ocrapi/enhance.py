import cv2
import numpy as np
from scipy import signal
import base64
import logging


# 固定尺寸
def resizeImg(image, height=900):
    h, w = image.shape[:2]
    pro = height / h
    size = (int(w * pro), int(height))
    img = cv2.resize(image, size)
    return img


# 边缘检测
def getCanny(image):
    # 高斯滤波
    binary = cv2.GaussianBlur(image, (3, 3), 2, 2)
    # 边缘检测
    binary = cv2.Canny(binary, 60, 240, apertureSize=3)
    # 膨胀操作，尽量使边缘闭合
    kernel = np.ones((3, 3), np.uint8)
    binary = cv2.dilate(binary, kernel, iterations=1)
    return binary


# 求出面积最大的轮廓
def findMaxContour(image):
    # 寻找边缘
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # 计算面积
    max_area = 0.0
    max_contour = []
    for contour in contours:
        currentArea = cv2.contourArea(contour)
        if currentArea > max_area:
            max_area = currentArea
            max_contour = contour
    return max_contour, max_area


# 多边形拟合凸包的四个顶点
def getBoxPoint(contour):
    # 多边形拟合凸包
    hull = cv2.convexHull(contour)
    epsilon = 0.02 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(hull, epsilon, True)
    approx = approx.reshape((len(approx), 2))
    return approx


# 适配原四边形点集
def adaPoint(box, pro):
    box_pro = box
    if pro != 1.0:
        box_pro = box/pro
    box_pro = np.trunc(box_pro)
    return box_pro


# 四边形顶点排序，[top-left, top-right, bottom-right, bottom-left]
def orderPoints(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect


# 计算长宽
def pointDistance(a, b):
    return int(np.sqrt(np.sum(np.square(a - b))))


# 透视变换
def warpImage(image, box):
    w, h = pointDistance(box[0], box[1]), \
           pointDistance(box[1], box[2])
    dst_rect = np.array([[0, 0],
                         [w - 1, 0],
                         [w - 1, h - 1],
                         [0, h - 1]], dtype='float32')
    M = cv2.getPerspectiveTransform(box, dst_rect)
    warped = cv2.warpPerspective(image, M, (w, h))
    return warped

def adaptive_thres(img, win=9, beta=0.9):
    if win % 2 == 0: win = win - 1
    # 边界的均值有点麻烦
    # 这里分别计算和和邻居数再相除
    kern = np.ones([win, win])
    sums = signal.correlate2d(img, kern, 'same')
    cnts = signal.correlate2d(np.ones_like(img), kern, 'same')
    means = sums // cnts
    # 如果直接采用均值作为阈值，背景会变花
    # 但是相邻背景颜色相差不大
    # 所以乘个系数把它们过滤掉
    img = np.where(img < means * beta, 0, 255)
    return img.astype(np.float32)


def enhance(img_b64):
    try:
        img_b64 = img_b64.split("base64,")[1]
    except:
        pass
    try:
        image = cv2.imdecode(np.frombuffer(base64.b64decode(img_b64), dtype=np.uint8), cv2.IMREAD_COLOR)
        ratio = 900 / image.shape[0]
        img = resizeImg(image)
        binary_img = getCanny(img)
        max_contour, max_area = findMaxContour(binary_img)
        boxes = getBoxPoint(max_contour)
        boxes = adaPoint(boxes, ratio)
        boxes = orderPoints(boxes)
        warped = warpImage(image, boxes)
        thre = adaptive_thres(cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY), win=9, beta=0.9)
    except Exception as e:
        logging.error("增强错误" + str(e))
        return "增强错误"
    output = cv2.imencode(".jpg", thre)[1]
    out_b64 = str(base64.b64encode(output))[2:-1]
    return out_b64
