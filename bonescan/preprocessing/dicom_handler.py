# need to clean dicom folder first

import pydicom as dicom
import os
import cv2
from bonescan.utils.common import log
from bonescan.utils.imagetools import ImageTools


class DicomHandler:
    def __init__(self):
        pass
    
    @staticmethod        
    def rename_dicom_files(dicomFolder):
        '''
        function to rename all dicom files in the folder
        '''
        dicomFiles = os.listdir(dicomFolder)
        for dicomFile in dicomFiles:
            try:
                ds = dicom.dcmread(os.path.join(dicomFolder, dicomFile))
                ACC = ds.AccessionNumber
                ACC = str(ACC)
                os.rename(os.path.join(dicomFolder, dicomFile), f'./data/ScreenCap/{ACC}.dcm')
            except Exception as e:
                print('Error: ', e)
    
    @staticmethod
    def save_as_jpg(dicomFolder):
        '''
        function to save dicom files as jpg
        '''
        dicomFiles = os.listdir(dicomFolder)
        for image in dicomFiles:
            try:
                ds = dicom.dcmread(os.path.join(dicomFolder, image))
                pixelArray = ds.pixel_array
                image = image.split('.')[0]
                cv2.imwrite(f'./data/ScreenCap/{image}.jpg', pixelArray)
            except Exception as e:
                print('Error: ', e)
                
    @staticmethod
    def crop_image(imageFolder, imageType = 'jpg'):
        '''
        function to crop the image
        '''
        for image in os.listdir(imageFolder):
            if not image.endswith(imageType):
                continue
            tempImg = cv2.imread(os.path.join(imageFolder, image), 0)
            height, width = tempImg.shape
            log(height, width)
            tempColor = 255
            if height == 1200 and width == 1640:
                # 1st rectangle: x = 270, y = 55, w = 150, h = 35
                tempImg = ImageTools.draw_ractangle(tempImg, 270, 55, 100, 38, tempColor)
                # 2nd rectangle: x = 305, y = 75, w = 15, h = 35
                tempImg = ImageTools.draw_ractangle(tempImg, 305, 75, 15, 35, tempColor)
                # 3rd rectangle: x = 2, y = 1150, w = 58, h = 40
                tempImg = ImageTools.draw_ractangle(tempImg, 2, 1150, 58, 40, tempColor)
                # 4th rectangle: x = 675, y = 55, w = 50, h = 45
                tempImg = ImageTools.draw_ractangle(tempImg, 675, 55, 50, 45, tempColor)
                # 5th rectangle: x = 755, y = 75, w = 15, h = 35
                tempImg = ImageTools.draw_ractangle(tempImg, 755, 75, 18, 35, tempColor)
                # 6th rectangle: x = 410, y = 1150, w = 60, h = 15
                tempImg = ImageTools.draw_ractangle(tempImg, 410, 1150, 60, 15, tempColor)
                # crop the image x = 10, y = 60, w = 790, h = 1120
                tempImg = ImageTools.crop_wholebody(tempImg, 10, 60, 790, 1120)
                # remove the midline
                tempImg = ImageTools.remove_midline(tempImg, 12, tempColor)
            elif height == 1080 and width == 1640:
                # 1st rectangle: x = 370, y = 55, w = 45, h = 35
                tempImg = ImageTools.draw_ractangle(tempImg, 370, 55, 45, 35, tempColor)
                # 2nd rectangle: x = 345, y = 70, w = 20, h = 30
                tempImg = ImageTools.draw_ractangle(tempImg, 345, 70, 20, 30, tempColor)
                # 3rd rectangle: x = 5, y =1050, w =30, h = 20
                tempImg = ImageTools.draw_ractangle(tempImg, 5, 1035, 55, 30, tempColor)
                # 4th rectangle: x = 670, y =55, w = 55, h = 35
                tempImg = ImageTools.draw_ractangle(tempImg, 670, 55, 55, 35, tempColor)
                # 5th rectangle: x = 750, y = 70, w = 20, h = 25
                tempImg = ImageTools.draw_ractangle(tempImg, 750, 70, 25, 30, tempColor)
                # 6th rectangle: x = 410, y = 1040, w = 40, h = 30
                tempImg = ImageTools.draw_ractangle(tempImg, 410, 1035, 58, 35, tempColor)
                tempImg = ImageTools.draw_ractangle(tempImg, 270, 55, 35, 15, tempColor)
                # crop the image x = 10 , y =60, w = 790, h = 1000
                tempImg = ImageTools.crop_wholebody(tempImg, 10, 60, 790, 1000)
                # remove the midline
                tempImg = ImageTools.remove_midline(tempImg, 12, tempColor)
            else:
                log('Image size not supported')
                continue
            cv2.imwrite(os.path.join(imageFolder, image), tempImg)
            log('Image cropped: ', image)
    


if __name__ == '__main__':
    # !! need to clean dicom folder first: run >> bash clean_dicom.sh
    # --[ ]: test rename all dicom
    dicomFolder = './data/ScreenCap'
    DicomHandler.rename_dicom_files(dicomFolder)
    
    # --[ ]: test save as jpg
    DicomHandler.save_as_jpg(dicomFolder)
    
    # --[ ]: test crop image and remove rectangle
    imageFolder = './data/ScreenCap'
    DicomHandler.crop_image(imageFolder)
    