# Image tools is a collection of functions that are used to manipulate an image

import cv2
import numpy as np
import matplotlib.pyplot as plt
from bonescan.utils.common import log

class ImageTools:
    def __init__(self):
        pass
    
    @staticmethod
    def crop_wholebody(image: np.ndarray, x: int, y: int, w: int, h: int):
        '''
        function that crop the whole body of the image
        '''
        return image[y:y+h, x:x+w]
    
    def remove_midline(image: np.ndarray, columnWidth: int, columnColor):
        '''
        function that remove the midline of the image
        '''
        centerCol = image.shape[1] // 2
        for row in range(image.shape[0]):
            for col in range(centerCol - columnWidth, centerCol + columnWidth):
                image[row, col] = columnColor
        return image
    
    def draw_ractangle(image: np.ndarray, x: int, y: int, w: int, h: int, color):
        '''
        function to draw a rectangle without outline on the image
        '''
        cv2.rectangle(image, (x, y), (x+w, y+h), color, -1)
        return image
    
    


if __name__ == "__main__":
    img1 = cv2.imread('./data/images/1.jpg', 0)
    img2 = cv2.imread('./data/images/2.jpg', 0)
    img3 = cv2.imread('./data/images/3.jpg', 0)
    img4 = cv2.imread('./data/images/4.jpg', 0)
    img5 = cv2.imread('./data/images/5.jpg', 0)
    height1, width1 = img1.shape
    height2, width2 = img2.shape
    height3, width3 = img3.shape
    height4, width4 = img4.shape
    height5, width5 = img5.shape
    log(height1, width1)
    log(height2, width2)
    log(height3, width3)
    log(height4, width4)
    log(height5, width5)
    # log(height1, width1)
    # log(height2, width2)
    # log(height3, width3)
    # log(height4, width4)
    # log(height5, width5)
    # -- [ ]: find height and width of the images
    ### -- [ ]: Original == 1830*1635 ;img2, img3, img5
    ### x = 52, y = 400, w = 760, h = 1098 
    
    ### -- [ ]: Original == 514*611 ;img1, img4
    # plt.imshow(img1, cmap='gray')
    # plt.show()
    
    # -- [ ]: case handle black and white background