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
        self.__numCases = self.__reportDf.shape[0]
        self.__reportPropList = []
        self.__numSplitWords = 15
        with open('./bonescan/utils/keywords.json') as f:
            temp = json.load(f)
            self.__kwBoneMetastasis = temp['kw_bone_metastasis']
            self.__kwBoneReport = temp["kw_bone_report"]
            
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
            "degenerative": None,
            "bone_fracture": None
        }
        return reportPropDict
    
    def check_metastasis(self, text = "Improvement of bony metastasis , however bony metastasis remained at right upper cervical spine, thoracic spines, right lateral aspect of 6th, 7th ribs, sacrum, right iliac bone, pubic symphysis, right femoral head and bilateral upper femurs"):
        '''
        check for bone metastasis in the text; input test must be split between "IMPRESSION" and "end of report"
        '''
        if text is None:
            print('<check_metastasis> Error: text is None')
            return None
        # [ ]: split text before and after the related word, key == 'main' in self.__kwBoneMetastasis
        splitedText = TextTools.word_search_and_split_both(text, self.__kwBoneMetastasis['main'], self.__numSplitWords)
        # [ ]: handle case when no word found
        # log(splitedText)
        if splitedText is None:
            log(text)
            log(splitedText)
            print("No word found in the text")
            return "not sure"
            # return "not sure"
        text = text.lower()
        # [ ]: check for all keys in self.__kwBoneMetastasis['___']
        for key in self.__kwBoneMetastasis['negative']:
            if key in splitedText:
                # log('Negative case')
                return "negative"
            if "no" in splitedText:
                if "evidence" in splitedText:
                    # log('Negative case')
                    return "negative"
        
        for key in self.__kwBoneMetastasis['positive']:
            if key in splitedText:
                # log('Positive case')
                return "positive"
        # log('Not sure')
        return "not sure"
    
    def check_degenerative_infection(self, text):
        '''
        check for degenerative infection in the text; input test must be split between "IMPRESSION" and "end of report"
        '''
        # TODO: run check for misspelling, positive and negative cases
        if text is None:
            print('<check_degenerative_infection> Error: text is None')
            return None
        if "degenerative" in text:
            # log(text, "degenerative found")
            return "positive"
        return "negative"
    
    def check_bone_fracture(self, text):
        '''
        check for bone fracture in the text; input test must be split between "IMPRESSION" and "end of report"
        '''
        # TODO: run check for misspelling, positive and negative cases
        if text is None:
            print('<check_bone_fracture> Error: text is None')
            return None
        if "fracture" in text:
            # log(text, "fracture found")
            return "positive"
        return "negative"    
    
    def extract_properties(self):
        if self.__reportDf is None:
            log('Error: report file is empty')
            return None
        i = 0
        numMetNegative = 0
        numMetPositive = 0
        numMetNotSure = 0
        numDegenerative = 0
        numFracture = 0
        for i in range(self.__numCases):
            # --[ ]: get history section
            tmpDictResult = self.get_properties_dict_template()
            tempText = self.__reportDf.loc[i, 'Report']
            tempText = str(tempText)
            historyText = TextTools.split_text(tempText, self.__kwBoneReport['history'], self.__kwBoneReport['findings'])
            # --[ ]: scan for gender: can be found in HISTORY section
            tmpGender = TextTools.search_gender(historyText)
            # --[ ]: scan for age: can be found in HISTORY section
            tmpAge = TextTools.search_age(historyText)
            # --[ ]: scan for cancer type: can be found in HISTORY section
            tmpCancerType = TextTools.search_cancer_type(historyText)
            impressionText = TextTools.split_text(tempText, self.__kwBoneReport['impression'], self.__kwBoneReport['end of report'])
            # --[ ]: check for metastasis
            tmpMetastasis = self.check_metastasis(impressionText)
            if tmpMetastasis == "negative":
                numMetNegative = numMetNegative + 1
                i = i + 1
                pass
            elif tmpMetastasis == "positive":
                numMetPositive = numMetPositive + 1
                i = i + 1
                pass
            elif tmpMetastasis == "not sure":
                numMetNotSure = numMetNotSure + 1
                i = i + 1
                pass
            elif tmpMetastasis == None:
                log('no evidence of metastasis found in the text')
            # --[ ]: check degenerative infection
            tmpDegenerative = self.check_degenerative_infection(impressionText)
            if tmpDegenerative == "positive":
                numDegenerative = numDegenerative + 1
            tmpFracture = self.check_bone_fracture(impressionText)
            if tmpFracture == "positive":
                numFracture = numFracture + 1
            tmpDictResult["index"] = i
            tmpDictResult["gender"] = tmpGender
            tmpDictResult["age"] = tmpAge
            tmpDictResult["cancer_type"] = tmpCancerType
            tmpDictResult["metastasis"] = tmpMetastasis
            tmpDictResult["degenerative"] = tmpDegenerative
            tmpDictResult["bone_fracture"] = tmpFracture
            self.__reportPropList.append(tmpDictResult)
            i = i + 1
        log(numMetNegative, numMetPositive, numMetNotSure, numDegenerative, numFracture)
    
    def get_report_df(self):
        return self.__reportDf
    
    def get_reportPropList(self):
        return self.__reportPropList
    
    def get_reportPropList_df(self):
        return pd.DataFrame(self.__reportPropList)
    

if __name__ == '__main__':
    # --[/]: test open file
    reportFilePath = './data/BoneReport_2018.xlsx'
    reportFileType = 'xlsx'
    labelExtraction = LabelExtraction(reportFilePath, reportFileType)
    labelExtraction.extract_properties()
    # log(labelExtraction.get_reportPropList())
    log(labelExtraction.get_reportPropList_df())
    # save to csv file
    labelExtraction.get_reportPropList_df().to_csv('./data/reportPropList.csv', index=False)
    
    # save add to bone report file
    reportDf = labelExtraction.get_report_df()
    reportPropDf = labelExtraction.get_reportPropList_df()
    
    # merge two dataframes
    reportDf['index'] = reportDf.index
    reportPropDf['index'] = reportPropDf.index
    reportDf = pd.merge(reportDf, reportPropDf, on='index', how='left')
    reportDf.drop(columns=['index'], inplace=True)
    reportDf.to_csv('./data/BoneReport_2018_with_prop.csv', index=False)
    
        
    # reportDf = labelExtraction.get_report_df()
    
    # --[/]: test check metastasis
    #   --[ ]: split before and after the related word
    
    # --[/]: test json file
    # with open('./bonescan/utils/keywords.json') as f:
    #     keysDict = json.load(f)
    # log(keysDict)
    # key_met = keysDict['kw_bone_metastasis']
    # log(key_met)