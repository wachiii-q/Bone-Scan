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
            "label": None,
            "date": None,
            "HN": None,
            "age": None,
            "gender": None,
            "cancer_type": None,
            "degenerative": None,
            "infection": None,
            "bone_fracture": None,
            "modality": None,
            "crystal_thickness": None,
            "collimeter_type": None
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
            image = image.split('.')[0]
            tempImageFileData = image.split('_')
            log('ACC', tempImageFileData[0])
            if tempImageFileData[0] == '':
                continue
            tempImageFileACC = int(tempImageFileData[0])
            tempImageFileModality = tempImageFileData[1]
            tempImageFileCrystalThickness = tempImageFileData[2]
            tempImageFileCollimeterType = tempImageFileData[3]
            tempAge = tempImageFileData[4]
            tempGender = tempImageFileData[5]
            
            if tempImageFileACC in self.__labelDf['ACC'].values:
                tempLabelDf = self.__labelDf[self.__labelDf['ACC'] == tempImageFileACC]
                tempLabel = tempLabelDf['metastasis'].values[0]
                log('Found Label: ', tempLabel)
                if tempLabel == 'positive':
                    tempLabel = 1
                elif tempLabel == 'negative':
                    tempLabel = 0
                else:
                    continue
                tempDictMapping['date'] = tempLabelDf['date'].values[0]
                tempDictMapping['HN'] = tempLabelDf['HN'].values[0]
                # tempDictMapping['age'] = tempLabelDf['age'].values[0]
                tempDictMapping['age'] = tempAge
                tempDictMapping['gender'] = tempGender
                tempDictMapping['cancer_type'] = tempLabelDf['cancer_type'].values[0]
                tempDictMapping['degenerative'] = tempLabelDf['degenerative'].values[0]
                tempDictMapping['infection'] = tempLabelDf['infection'].values[0]
                tempDictMapping['bone_fracture'] = tempLabelDf['bone_fracture'].values[0]
                tempDictMapping['modality'] = tempImageFileModality
                tempDictMapping['crystal_thickness'] = tempImageFileCrystalThickness
                tempDictMapping['collimeter_type'] = tempImageFileCollimeterType
                tempDictMapping['label'] = tempLabel
                # duplicate the image to the empty folder
                src = os.path.join(self.__imageFolder, f"{image}.{self.iamgeType}")
                dst = os.path.join(self.__emptyFolder, f"{image}_{tempLabel}.jpg")
                shutil.copyfile(src, dst)
                tempDictMapping['image_path'] = src
                tempDictMapping['image_path_with_label'] = dst            
                self.__mappingList.append(tempDictMapping)
                numFoundMappingACC += 1
            else:
                numNotFoundMappingACC += 1
                continue
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
    labelDf = pd.read_csv('./data/report/Extracted_Bone_2023.csv')
    # labelDf = labelDf.drop(['date', 'HN', 'age', 'cancer_type', 'degenerative', 'infection', 'bone_fracture', 'gender', 'BMI', 'device'], axis=1)
    labelDf = labelDf[labelDf['metastasis'] != 'not sure']
    # labelDf = labelDf.drop(['Unnamed: 0'], axis=1)
    log(labelDf.head())
    imageFolder = 'data/2023/WBjpeg'
    emptyFolder = 'data/2023/WBjpegLabel'
    
    imageLabelMapping = ImageLabelMapping(imageFolder, emptyFolder, labelDf)
    imageLabelMapping.map_image_label()
    
    imageLabelMapping.get_mapping_df()
    log(imageLabelMapping.get_mapping_df())
    
    # save as csv
    imageLabelMapping.get_mapping_df().to_csv('data/2023/mapping.csv', index=False)
    
    