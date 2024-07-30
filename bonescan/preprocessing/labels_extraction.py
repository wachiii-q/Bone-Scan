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
        '''
        function to read the report file, and return a dataframe to private variable __reportDf
        '''
        try: 
            if self.__reportFileType == 'xlsx':
                df = pd.read_excel(self.__reportFilePath)
        
        #TODO: drop nan temp df 
        except Exception as e:
            df = None
            print('Error reading file: ', e)
        return df
    
    def get_properties_dict_template(self):
        '''
        function to return a dictionary template for properties of the report
        '''
        reportPropDict = {
            "index": None,
            "date": None,
            "HN": None,
            "ACC": None,
            "gender": None,
            "age": None,
            "cancer_type": None,
            "metastasis": None,
            "degenerative": None,
            "infection": None,
            "bone_fracture": None
        }
        return reportPropDict
    
    def check_metastasis(self, text):
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
    
    def check_degenerative(self, text):
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
    
    def check_infection(self, text):
        '''
        check for infection in the text; input test must be split between "IMPRESSION" and "end of report"
        '''
        #TODO: run check for misspelling, positive and negative cases
        if text is None:
            print('<check_infection> Error: text is None')
            return None
        if "infection" in text:
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
        '''
        function to extract properties of the report
        '''
        if self.__reportDf is None:
            log('Error: report file is empty')
            return None
        i = 0
        numMetNegative = 0
        numMetPositive = 0
        numMetNotSure = 0
        numDegenerative = 0
        numFracture = 0
        numInfection = 0
        for i in range(self.__numCases):
            # --[ ]: get history section
            tmpDictResult = self.get_properties_dict_template()
            # --[ ]: get HN and date
            tempHN = self.__reportDf.loc[i, 'PID']
            tempDate = self.__reportDf.loc[i, 'InsertDate']
            tempACC = self.__reportDf.loc[i, 'StudyKey']
            # tempDate = tempDate.replace("/", "")
            tempText = self.__reportDf.loc[i, 'Report']
            tempText = str(tempText)
            historyText = TextTools.split_text(tempText, self.__kwBoneReport['history'], self.__kwBoneReport['findings'])
            if historyText is None:
                print('Error: historyText is None')
                continue
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
            tmpDegenerative = self.check_degenerative(impressionText)
            if tmpDegenerative == "positive":
                numDegenerative = numDegenerative + 1
            tmpFracture = self.check_bone_fracture(impressionText)
            tmpInfection = self.check_infection(impressionText)
            if tmpInfection == "positive":
                numInfection = numInfection + 1
            if tmpFracture == "positive":
                numFracture = numFracture + 1
            tmpDictResult["index"] = i
            tmpDictResult["HN"] = str(tempHN)
            tmpDictResult["date"] = str(tempDate)
            tmpDictResult["ACC"] = str(tempACC)
            tmpDictResult["gender"] = tmpGender
            tmpDictResult["age"] = tmpAge
            tmpDictResult["cancer_type"] = tmpCancerType
            tmpDictResult["metastasis"] = tmpMetastasis
            tmpDictResult["degenerative"] = tmpDegenerative
            tmpDictResult["infection"] = tmpInfection
            tmpDictResult["bone_fracture"] = tmpFracture
            self.__reportPropList.append(tmpDictResult)
            i = i + 1
        # log(self.__reportPropList)
        log(tmpDictResult)
        log(numMetNegative, numMetPositive, numMetNotSure, numDegenerative, numInfection, numFracture)
    
    def get_report_df(self):
        '''
        return the report dataframe
        '''
        return self.__reportDf
    
    def get_reportPropList(self):
        '''
        return the list of properties dict of the report
        '''
        return self.__reportPropList
    
    def get_reportPropList_df(self):
        '''
        return the list of properties dict of the report in dataframe format
        '''
        return pd.DataFrame(self.__reportPropList)
    

if __name__ == '__main__':
    # -- [/]: Drop NaN in report column
    # path = './data/report/Bone_2024.xlsx'
    # fileType = 'xlsx'
    # # open file
    # df = pd.read_excel(path)
    # df_report = df['Report'][0]
    # df = df.dropna(subset=['Report'])
    # # save to xlsx
    # df.to_excel('./data/report/Modified_Bone_2024.xlsx', index=False)
    # log(df.head())    
    
    # --[/]: test label extraction <main>
    # reportFilePath = './data/report/Modified_Bone_2024.xlsx'
    # reportFileType = 'xlsx'
    # labelExtraction = LabelExtraction(reportFilePath, reportFileType)
    # labelExtraction.extract_properties()
    # log(labelExtraction.get_reportPropList_df())
    # labelExtraction.get_reportPropList_df().to_csv('./data/report/Extracted_Bone_2024.csv', index=False)
    
    # --[/]: test label extraction < 7 years >
    report2016 = './data/ExportNM_Bone/ExportNM2016_Bone.xlsx'
    report2017 = './data/ExportNM_Bone/ExportNM2017_Bone.xlsx'
    report2018 = './data/ExportNM_Bone/ExportNM2018_Bone.xlsx'
    report2019 = './data/ExportNM_Bone/ExportNM2019_Bone.xlsx'
    report2020 = './data/ExportNM_Bone/ExportNM2020_Bone.xlsx'
    report2021 = './data/ExportNM_Bone/ExportNM2021_Bone.xlsx'
    report2022 = './data/ExportNM_Bone/ExportNM2022_Bone.xlsx'
    reportFileType = 'xlsx'
    LabelExtraction2016 = LabelExtraction(report2016, reportFileType)
    LabelExtraction2017 = LabelExtraction(report2017, reportFileType)
    LabelExtraction2018 = LabelExtraction(report2018, reportFileType)
    LabelExtraction2019 = LabelExtraction(report2019, reportFileType)
    LabelExtraction2020 = LabelExtraction(report2020, reportFileType)
    LabelExtraction2021 = LabelExtraction(report2021, reportFileType)
    LabelExtraction2022 = LabelExtraction(report2022, reportFileType)
    
    LabelExtraction2016.extract_properties()
    LabelExtraction2016.get_reportPropList_df().to_csv('./data/report/Extracted_Bone_2016.csv', index=False)
    
    LabelExtraction2017.extract_properties()
    LabelExtraction2017.get_reportPropList_df().to_csv('./data/report/Extracted_Bone_2017.csv', index=False)
    
    LabelExtraction2018.extract_properties()
    LabelExtraction2018.get_reportPropList_df().to_csv('./data/report/Extracted_Bone_2018.csv', index=False)
    
    LabelExtraction2019.extract_properties()
    LabelExtraction2019.get_reportPropList_df().to_csv('./data/report/Extracted_Bone_2020.csv', index=False)
    
    LabelExtraction2020.extract_properties()
    LabelExtraction2020.get_reportPropList_df().to_csv('./data/report/Extracted_Bone_2020.csv', index=False)
    
    LabelExtraction2021.extract_properties()
    LabelExtraction2021.get_reportPropList_df().to_csv('./data/report/Extracted_Bone_2021.csv', index=False)
    
    LabelExtraction2022.extract_properties()
    LabelExtraction2022.get_reportPropList_df().to_csv('./data/report/Extracted_Bone_2022.csv', index=False)
    
    

    # log(labelExtraction.get_report_df().groupby('cancer_type').count())
    # labelExtraction.get_reportPropList_df().to_csv('./data/reportPropList.csv', index=False)
    
    # save add to bone report file
    # reportDf = labelExtraction.get_report_df()
    # reportPropDf = labelExtraction.get_reportPropList_df()
    
    # merge two dataframes
    # reportDf['index'] = reportDf.index
    # reportPropDf['index'] = reportPropDf.index
    # reportDf = pd.merge(reportDf, reportPropDf, on='index', how='left')
    # reportDf.drop(columns=['index'], inplace=True)
    # reportDf.to_csv('./data/BoneReport_2018_with_prop.csv', index=False)
    
        
    # reportDf = labelExtraction.get_report_df()
    
    # --[/]: test check metastasis
    #   --[ ]: split before and after the related word
    
    # --[/]: test json file
    # with open('./bonescan/utils/keywords.json') as f:
    #     keysDict = json.load(f)
    # log(keysDict)
    # key_met = keysDict['kw_bone_metastasis']
    # log(key_met)