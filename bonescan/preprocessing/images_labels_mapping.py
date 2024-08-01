# map image path with the labelling
# NOTE: label of metastasis
# 0: no metastasis (negative)
# 1: metastasis (positive)
# label_df of class containing the label and ACC
# image_folder: folder containing the images
# empty_folder: reserve folder for image+label.jpg

import os
import pandas as pd
import shutil
from bonescan.utils.common import log


class ImageLabelMapping:
    def __init__(self, imageFolder, emptyFolder, labelDf):
        self.__imageFolder = imageFolder
        self.__labelDf = labelDf
        self.__emptyFolder = emptyFolder
        self.__mappingList = []
        self.iamgeType = 'jpg'
        
    def get_mapping_dict_template(self):
        '''
        function to return the mapping dictionary template
        '''
        mappingDict = {
            "image_path": None,
            "image_path_with_label": None,
            "label": None
        }
        return mappingDict
        
    def map_image_label(self):
        '''
        function to map image with label
        '''
        numFoundMappingACC = 0
        numNotFoundMappingACC = 0
        for image in os.listdir(self.__imageFolder):
            if not image.endswith(self.iamgeType):
                continue
            tempDictMapping = self.get_mapping_dict_template()
            # example 2: 28226616_NMCT870DR.jpg -> 28226616
            tempACCimage = int(image.split('_')[0])
            # tempACCimage = int(image.split('.')[0])
            log(tempACCimage)
            label = self.__labelDf[self.__labelDf['ACC'] == tempACCimage]['metastasis'].values[0] if tempACCimage in self.__labelDf['ACC'].values else None
            # log(label)
            if label == 'positive':
                label = 1
            elif label == 'negative':
                label = 0
            else:
                log('ACC not found in labelDf')
                log('ACC: ', tempACCimage)
                numNotFoundMappingACC += 1
                continue
            # duplicate the image to the empty folder
            src = os.path.join(self.__imageFolder, image)
            dst = os.path.join(self.__emptyFolder, f"{image.split('_')[0]}_{label}.jpg")
            shutil.copyfile(src, dst)
            tempDictMapping['image_path'] = os.path.join(self.__imageFolder, image)
            tempDictMapping['image_path_with_label'] = dst
            tempDictMapping['label'] = label
            self.__mappingList.append(tempDictMapping)
            numFoundMappingACC += 1
            # log('Mapping: ', tempDictMapping)
        log(self.__mappingList)
        log(numNotFoundMappingACC)
        log(numFoundMappingACC)
        
    def get_mapping_list(self):
        '''
        function to return the mapping list
        '''
        return self.__mappingList
    
    def get_mapping_df(self):
        '''
        function to return the mapping dataframe
        '''
        return pd.DataFrame(self.__mappingList)
            
        
    
    

if __name__ == "__main__":
    labelDf = pd.read_csv('./data/report/Merged_2024.csv')
    labelDf = labelDf.drop(['date', 'HN', 'age', 'cancer_type', 'degenerative', 'infection', 'bone_fracture', 'gender', 'BMI', 'device'], axis=1)
    labelDf = labelDf[labelDf['metastasis'] != 'not sure']
    labelDf = labelDf.drop(['Unnamed: 0'], axis=1)
    log(labelDf.head())
    imageFolder = 'data/AntPos/WBjpeg'
    emptyFolder = 'data/AntPos/WBjpegLabel'
    
    imageLabelMapping = ImageLabelMapping(imageFolder, emptyFolder, labelDf)
    imageLabelMapping.map_image_label()
    
    imageLabelMapping.get_mapping_df()
    log(imageLabelMapping.get_mapping_df())
    
    