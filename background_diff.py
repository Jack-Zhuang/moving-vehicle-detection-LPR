import cv2
import numpy as np
from config import *


def background_diff(videopath):
    camera = cv2.VideoCapture(videopath)
    while True:
        ret, frame = camera.read()
        fgmask = bs.apply(frame)
        th = cv2.threshold(fgmask.copy(), 244, 255, cv2.THRESH_BINARY)[1]
        # th = cv2.adaptiveThreshold(src=fgmask,maxValue=255,adaptiveMethod=1,thresholdType=0,blockSize=3,C=10)
        th_erode = cv2.erode(th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3)), iterations = 2)
        dilated = cv2.dilate(th_erode, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8,3)), iterations = 2)
        # print(dilated)
        # return dilated
        contours, hier = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # print(contours)
        for c in contours:
            if cv2.contourArea(c) > 1000:
                (x,y,w,h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 255, 0), 2)

        cv2.imshow("mog", fgmask)
        cv2.imshow("thresh", th)
        cv2.imshow("diff", frame & cv2.cvtColor(fgmask, cv2.COLOR_GRAY2BGR))
        cv2.imshow("detection", frame)
        cv2.imshow('erode', th_erode)
        cv2.imshow('dilated', dilated)
        if cv2.waitKey(33) & 0xFF == ord('q'):
            break
    camera.release()
    cv2.destroyAllWindows()



if __name__ == '__main__':
    background_diff(videopath)
