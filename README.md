# moving-vehicle-detection-LPR
The project aims to detect the moving vehicles and extract their license plates for the further recognition
## FAQ  
* `imread error`: error: (-215) ssize.width > 0 && ssize.height > 0 in function cv::resize
  * try to use relative path instead of absolute path which means to put your image into the project file
* `numpy error`: The truth value of an array with more than one element is ambiguous
  * This error is caused by the ambiguous return value of imread and the error can be solved by using the method a.any()/a.all() to give an exact return value, for example:
```python
      if(image_gray.any() == None):
        print("can't read the image")
      else:
        image_binary = cv2.threshold(image_gray, 200, 255, cv2.THRESH_BINARY)[1]
        cv2.imshow("original_image", image_binary)
        cv2.waitKey(0)
```
