# Image preprocessing tool for cleaning and cropping images
import cv2
import os
import numpy as np
from bonescan.utils.common import log
from bonescan.utils.imagetools import ImageTools

class ImagePreprocessing:
    def __init__(self, imageFolderPath):
        self.__midlineWidth = 10
        self.__imgCropX = 52
        self.__imgCropY = 400
        self.__imgCropWidth = 760
        self.__imgCropHeight = 1098
        self.__imageFolderPath = imageFolderPath
        
    def check_image_color_scheme(self, imagePath):
        '''
        function to check the color scheme of the image
        '''
        img = cv2.imread(imagePath, 0)
        if np.mean(img) > 127:
            return 'black_on_white'
        else:
            return 'white_on_black'
        
    def image_inverse(self, image: np.ndarray):
        '''
        function to inverse the image
        '''
        return cv2.bitwise_not(image)
    
    def preprocess_image(self):
        '''
        function to preprocess the image
        '''
        for imageFile in os.listdir(self.__imageFolderPath):
            log('Processing image: ', imageFile)
            if not imageFile.endswith('.jpg'):
                continue
            imgPath = os.path.join(self.__imageFolderPath, imageFile)
            img = cv2.imread(imgPath, 0)
            colorScheme = self.check_image_color_scheme(imgPath)
            if colorScheme == 'black_on_white':
                columnColor = 254
            else:
                columnColor = 1
            img = ImageTools.crop_wholebody(img, self.__imgCropX, self.__imgCropY, self.__imgCropWidth, self.__imgCropHeight)
            img = ImageTools.remove_midline(img, self.__midlineWidth, columnColor)
            
            # save the image as imageFile: normal and invert
            imageFileName = imageFile.split('.')[0]
            imageFileName = imageFileName
            # imgInverse = self.image_inverse(img)
            # imageFileNameInverse = imageFileName + '_inverse'
            cv2.imwrite(os.path.join(self.__imageFolderPath, imageFileName + '.jpg'), img)
            # cv2.imwrite(os.path.join(self.__imageFolderPath, imageFileNameInverse + '.jpg'), imgInverse)
            
    
if __name__ == "__main__":
    imageFolderPath = './data/images'
    imagePreprocessing = ImagePreprocessing(imageFolderPath)
    imagePreprocessing.preprocess_image()
    log('Image preprocessing completed')