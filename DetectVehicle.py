import cv2
import numpy as np
from config import *


def detectVehicle(videopath):
    cap = cv2.VideoCapture(videopath)
    if (cap.isOpened() == False):
        print("Error opening video stream or file")
    frameNum = 0
    # Read until video is completed
    while (cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
        frameNum += 1
        if ret == True:
            tempframe = frame
            if (frameNum == 1):
                firstframe = cv2.cvtColor(tempframe, cv2.COLOR_BGR2GRAY)
                secondframe = cv2.cvtColor(tempframe, cv2.COLOR_BGR2GRAY)
            if (frameNum == 2):
                secondframe = cv2.cvtColor(tempframe, cv2.COLOR_BGR2GRAY)
                median = cv2.medianBlur(secondframe, 3)
                secondresult = cv2.absdiff(median, first_median)
                threshold_frame = cv2.threshold(secondresult, 20, 255, cv2.THRESH_BINARY)[1]
                gauss_image = cv2.GaussianBlur(threshold_frame, (3, 3), 0)
                # cv2.imshow('原图', frame)
                # cv2.imshow('Frame', secondframe)
                # cv2.imshow('median', median)
                # cv2.imshow('result', gauss_image)
            if (frameNum >= 3):
                thirdframe = cv2.cvtColor(tempframe, cv2.COLOR_BGR2GRAY)
                third_median = cv2.medianBlur(thirdframe, 3)
                secondresult = cv2.absdiff(second_median, first_median)
                second_threshold_frame = cv2.threshold(secondresult, 20, 255, cv2.THRESH_BINARY)[1]
                second_gauss_image = cv2.GaussianBlur(second_threshold_frame, (3, 3), 0)
                thirdresult = cv2.absdiff(third_median, second_median)
                third_threshold_frame = cv2.threshold(thirdresult, 20, 255, cv2.THRESH_BINARY)[1]
                third_gauss_image = cv2.GaussianBlur(third_threshold_frame, (3, 3), 0)
                diff_result = cv2.bitwise_and(second_gauss_image, third_gauss_image)
                # return diff_result
                fgmask = bs.apply(tempframe)
                th = cv2.threshold(fgmask.copy(), 244, 255, cv2.THRESH_BINARY)[1]
                # th = cv2.adaptiveThreshold(src=fgmask,maxValue=255,adaptiveMethod=1,thresholdType=0,blockSize=3,C=10)
                th_erode = cv2.erode(th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=2)
                dilated = cv2.dilate(th_erode, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 3)), iterations=2)
                combine_result = cv2.bitwise_or(diff_result, dilated)

                contours, hier = cv2.findContours(combine_result, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                # print(contours)
                detect = tempframe.copy()
                for c in contours:
                    if cv2.contourArea(c) > 1000:
                        (x, y, w, h) = cv2.boundingRect(c)
                        cv2.rectangle(detect, (x, y), (x + w, y + h), (255, 255, 0), 2)
                # Display the resulting frame
                cv2.imshow('原图', frame)
                # cv2.imshow('Frame', thirdframe)
                # cv2.imshow('median1', second_median)
                # cv2.imshow('median2', third_median)
                cv2.imshow('diff_result', diff_result)
                cv2.imshow('bg_result', dilated)
                cv2.imshow('combine_result', combine_result)
                cv2.imshow('detect', detect)


                # Press Q on keyboard to  exit
                if cv2.waitKey(33) & 0xFF == ord('q'):
                    break
            firstframe = secondframe
            first_median = cv2.medianBlur(firstframe, 3)
            secondframe = cv2.cvtColor(tempframe, cv2.COLOR_BGR2GRAY)
            second_median = cv2.medianBlur(secondframe, 3)

        # Break the loop
        else:
            break

    # When everything done, release the video capture object
    cap.release()
    # Closes all the frames
    cv2.destroyAllWindows()

if __name__ == '__main__':
    detectVehicle(videopath)