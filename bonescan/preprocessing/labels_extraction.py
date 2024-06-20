# extract labels and properties of the samples from bone scan report
# the report is typically consists of 3 main sections; HISTORY, FINDINGS, IMPRESSION
# labels and properties to be extracted are:
# 1. gender
# 2. age
# 3. type of cancer
# 4. is_metastasis
# 5. is degenerative infection
# 6. is fracture

# -- Data Structure: list of dictionaries
# note: key & value = snake_case
# each dictionary contains the following
#       "index": int,
#       "gender": "Male" or "Female",
#       "age": int,
#       "cancer_type": str
#       "metastasis": "Positive" / "Negative" / "Not Sure,
#       "degenerative_infection": "Positive" / "Negative" / "Not Sure,
#       "bone_fracture": "Positive" / "Negative" / "Not Sure,

import pandas as pd
from bonescan.utils.common import log
from bonescan.utils.texttools import TextTools
import json

# --TODO: improve efficiency of searching properties

# class result(Enum):
#     NO_METASTASIS = 1
#     NOT_SURE = 2
#     METASTASIS = 3

class LabelExtraction:
    def __init__(self, reportFilePath, reportFileType):
        self.__reportFilePath = reportFilePath
        self.__reportFileType = reportFileType
        self.__reportDf = self.read_report_file()
        self.__numCase = self.__reportDf.shape[0]
        self.__reportPropList = []
        self.__numSplitWords = 15
        with open('./bonescan/utils/keywords.json') as f:
            temp = json.load(f)
            self.__kwBoneMetastasis = temp['kw_bone_metastasis']
            
    def read_report_file(self):
        try: 
            if self.__reportFileType == 'xlsx':
                df = pd.read_excel(self.__reportFilePath)
        except Exception as e:
            df = None
            print('Error reading file: ', e)
        return df
    
    def get_properties_dict_template(self):
        reportPropDict = {
            "index": None,
            "gender": None,
            "age": None,
            "cancer_type": None,
            "metastasis": None,
            "degenerative_infection": None,
            "bone_fracture": None
        }
        return reportPropDict
    
    def check_metastasis(self, text = "Improvement of bony metastasis , however bony metastasis remained at right upper cervical spine, thoracic spines, right lateral aspect of 6th, 7th ribs, sacrum, right iliac bone, pubic symphysis, right femoral head and bilateral upper femurs"):
        '''
        check for bone metastasis in the text; input test must be split between "IMPRESSION" and "end of report"
        '''
        i = 0
        numNegative = 0
        numPositive = 0
        text = text.lower()
        # [ ]: split text before and after the related word, key == 'main' in self.__kwBoneMetastasis
        splitedText = TextTools.word_search_and_split_both(text, self.__kwBoneMetastasis['main'], self.__numSplitWords)
        log(splitedText)
        # [ ]: check for all keys in self.__kwBoneMetastasis['___']
        for key in self.__kwBoneMetastasis['negative']:
            if key in splitedText:
                log('Negative case')
                return "negative"
        
        for key in self.__kwBoneMetastasis['positive']:
            if key in splitedText:
                log('Positive case')
                return "positive"
        log('Not sure')
        return "not sure"
        
       
            
            
        
        
    
    def extract_properties(self):
        if self.__reportDf is None:
            log('Error: report file is empty')
            return None
        for i in range(self.__numSamples):
            # get history section
            tempText = self.__reportDf.loc[i, 'Report']
            tempText = str(tempText)
            historyText = TextTools.split_text(tempText, 'HISTORY', 'FINDINGS')
            # scan for gender: can be found in HISTORY section
            tmpGender = TextTools.search_gender(historyText)
            log(tmpGender)
            # scan for age: can be found in HISTORY section
            tmpAge = TextTools.search_age(historyText)
            log(tmpAge)
            # scan for cancer type: can be found in HISTORY section
            tmpCancerType = TextTools.search_cancer_type(historyText)
            log(tmpCancerType)
            impressionText = TextTools.split_text(tempText, 'IMPRESSION', 'end of report')
            log(impressionText)        
    
    def get_report_df(self):
        return self.__reportDf
    

if __name__ == '__main__':
    # --[/]: test json file
    # with open('./bonescan/utils/keywords.json') as f:
    #     keysDict = json.load(f)
    # log(keysDict)
    # key_met = keysDict['kw_bone_metastasis']
    # log(key_met)
    
    # --[/]: test open file
    reportFilePath = './data/BoneReport_2018.xlsx'
    reportFileType = 'xlsx'
    labelExtraction = LabelExtraction(reportFilePath, reportFileType)
    labelExtraction.check_metastasis()
    # reportDf = labelExtraction.get_report_df()
    
    # --[/]: test check metastasis
    #   --[ ]: split before and after the related word
    