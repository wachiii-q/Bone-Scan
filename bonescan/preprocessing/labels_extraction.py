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
#       "gender": "Male" or "Female",
#       "age": int,
#       "cancer_type": str
#       "metastasis": "True" or "False",
#       "degenerative_infection": "True" or "False",
#       "bone_fracture": "True" or "False"

import pandas as pd
from bonescan.utils.common import log
from bonescan.utils.texttools import TextTools

# --TODO: improve efficiency of searching properties

class LabelExtraction:
    def __init__(self, reportFilePath, reportFileType):
        self.__reportFilePath = reportFilePath
        self.__reportFileType = reportFileType
        self.__reportDf = self.read_report_file()
        self.__numSamples = 1
        self.__reportPropList = []
            
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
            "gender": None,
            "age": None,
            "cancer_type": None,
            "metastasis": None,
            "degenerative_infection": None,
            "bone_fracture": None
        }
        return reportPropDict

    def search_metastasis(self, text):
        pass
    
    def search_degenerative_infection(self, text):
        pass
    
    def search_bone_fracture(self, text):
        pass
    
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
            
        # pass
        
    
    def get_report_df(self):
        return self.__reportDf
    

if __name__ == '__main__':
    # --[/]: test open file
    reportFilePath = './data/BoneReport_2018.xlsx'
    reportFileType = 'xlsx'
    labelExtraction = LabelExtraction(reportFilePath, reportFileType)
    reportDf = labelExtraction.get_report_df()
    
    # --[ ]: test split_text function in extract_properties
    labelExtraction.extract_properties()
    
    # count = 0
    # for i in range(3802):
    #     tmp = temp.loc[i, 'Report']
    #     # split the text after IMPRESSION
    #     text_imp = tmp.split('IMPRESSION')[1]
    #     log(text_imp)
    #     print(type(text_imp))
    #     # search for "no definite evidence of metastasis" in IMPRESSION section
    #     if ('metastasis' in text_imp):
    #         count += 1
        
    # print(count)
    
    # temp = ,
        
    # --[ ]: test get_properties_dict_template
    
    
    
    
    
        
        
